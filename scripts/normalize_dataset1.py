import pandas as pd
import os
from utils import get_db_connection

def load_raw_data(filepath):
    print(f"-> Cargando datos desde {filepath}...")
    df = pd.read_csv(filepath)
    df.fillna('', inplace=True)
    return df

def extract_entity_table(df, column_name, id_prefix):
    all_values = df[column_name].str.split(',').explode().str.strip()
    unique_values = all_values[all_values != ''].unique()
    df_entity = pd.DataFrame({f'{id_prefix}_name': unique_values})
    df_entity.insert(0, f'{id_prefix}_id', range(1, 1 + len(df_entity)))
    return df_entity

def create_mapping_table(df, df_entity, df_col_name, entity_name_col, entity_id_col):
    df_exploded = df[['show_id', df_col_name]].copy()
    df_exploded[df_col_name] = df_exploded[df_col_name].str.split(', ')
    df_exploded = df_exploded.explode(df_col_name)
    df_exploded[df_col_name] = df_exploded[df_col_name].str.strip()
    df_exploded = df_exploded[df_exploded[df_col_name] != '']
    
    df_mapping = pd.merge(
        df_exploded, 
        df_entity, 
        left_on=df_col_name, 
        right_on=entity_name_col, 
        how='inner'
    )
    return df_mapping[['show_id', entity_id_col]]

def save_to_outputs(df, table_name, engine, output_dir):
    """Guarda el DataFrame en PostgreSQL y en un archivo CSV"""
    print(f"   Guardando tabla '{table_name}'...")
    
    # 1. Exportar a PostgreSQL
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    
    # 2. Exportar a CSV en la carpeta normalized
    csv_path = os.path.join(output_dir, f"{table_name}.csv")
    df.to_csv(csv_path, index=False)

if __name__ == '__main__':
    # 1. Calculamos la ruta absoluta del directorio donde vive este script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. Construimos las rutas de forma absoluta y a prueba de errores
    filepath = os.path.abspath(os.path.join(script_dir, '../data/raw/netflix_titles.csv'))
    output_dir = os.path.abspath(os.path.join(script_dir, '../data/normalized/dataset1'))
    
    # Crear directorio si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    df_raw = load_raw_data(filepath)
    engine = get_db_connection()
    
    print("\n--- Iniciando Normalización a 3FN ---")
    
    # 1. Extraer entidades independientes (Diccionarios)
    df_genres = extract_entity_table(df_raw, 'listed_in', 'genre')
    df_directors = extract_entity_table(df_raw, 'director', 'director')
    df_actors = extract_entity_table(df_raw, 'cast', 'actor')
    df_countries = extract_entity_table(df_raw, 'country', 'country')
    
    # 2. Crear tablas intermedias (Mappings)
    df_show_genres = create_mapping_table(df_raw, df_genres, 'listed_in', 'genre_name', 'genre_id')
    df_show_directors = create_mapping_table(df_raw, df_directors, 'director', 'director_name', 'director_id')
    df_show_actors = create_mapping_table(df_raw, df_actors, 'cast', 'actor_name', 'actor_id')
    df_show_countries = create_mapping_table(df_raw, df_countries, 'country', 'country_name', 'country_id')
    
    # 3. Crear Tabla Principal (Shows) limpia
    columnas_multivaluadas = ['director', 'cast', 'country', 'listed_in']
    df_shows = df_raw.drop(columns=columnas_multivaluadas)
    
    print("\n--- Exportando a PostgreSQL y CSV ---")
    
    # Guardar Entidades
    save_to_outputs(df_genres, 'genres', engine, output_dir)
    save_to_outputs(df_directors, 'directors', engine, output_dir)
    save_to_outputs(df_actors, 'actors', engine, output_dir)
    save_to_outputs(df_countries, 'countries', engine, output_dir)
    
    # Guardar Principal
    save_to_outputs(df_shows, 'shows', engine, output_dir)
    
    # Guardar Relaciones
    save_to_outputs(df_show_genres, 'show_genres', engine, output_dir)
    save_to_outputs(df_show_directors, 'show_directors', engine, output_dir)
    save_to_outputs(df_show_actors, 'show_actors', engine, output_dir)
    save_to_outputs(df_show_countries, 'show_countries', engine, output_dir)
    
    print("\n¡Proceso del Dataset 1 completado con éxito!")