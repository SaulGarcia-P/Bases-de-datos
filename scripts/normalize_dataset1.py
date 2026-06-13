import pandas as pd
from utils import export_table, create_bridge_table, init_sql_files

def normalize_netflix():
    print("Iniciando normalización del Dataset 1 (Netflix)...")
    
    # Inicializa y limpia los archivos SQL unificados para este dataset
    init_sql_files('dataset1')
    
    # ---------------------------------------------------------
    # REQUISITO 1: Lectura de datos originales y validación
    # ---------------------------------------------------------
    raw_path = 'data/raw/netflix_titles.csv'
    try:
        df = pd.read_csv(raw_path)
    except FileNotFoundError:
        print(f"[!] Error: No se encontró el archivo en {raw_path}")
        return

    # ---------------------------------------------------------
    # REQUISITO 2: Transformaciones a 3FN (Tablas Catálogo)
    # Extraemos 'type' y 'rating' para evitar redundancias
    # ---------------------------------------------------------
    
    # Catálogo de Tipos (Movie / TV Show)
    types_df = pd.DataFrame(df['type'].dropna().unique(), columns=['type_name'])
    types_df['type_id'] = range(1, len(types_df) + 1)
    
    # Catálogo de Clasificaciones (Ratings)
    ratings_df = pd.DataFrame(df['rating'].dropna().unique(), columns=['code'])
    ratings_df['rating_id'] = range(1, len(ratings_df) + 1)

    # ---------------------------------------------------------
    # REQUISITO 2: Transformaciones a 1FN/2FN (Multivaluados)
    # Extraemos actores, directores, países y categorías
    # ---------------------------------------------------------
    
    def extract_unique_catalog(col_name, new_col_name, id_col_name):
        """Extrae valores únicos de una columna separada por comas y genera un ID."""
        all_values = df[col_name].dropna().astype(str).str.split(', ').explode().str.strip()
        unique_values = all_values.unique()
        catalog_df = pd.DataFrame(unique_values, columns=[new_col_name])
        catalog_df[id_col_name] = range(1, len(catalog_df) + 1)
        return catalog_df

    actors_df = extract_unique_catalog('cast', 'full_name', 'actor_id')
    directors_df = extract_unique_catalog('director', 'full_name', 'director_id')
    countries_df = extract_unique_catalog('country', 'country_name', 'country_id')
    categories_df = extract_unique_catalog('listed_in', 'category_name', 'category_id')

    # ---------------------------------------------------------
    # REQUISITO 3: Generación de estructura (Tablas Puente M:N)
    # ---------------------------------------------------------
    show_actor_df = create_bridge_table(df, 'show_id', 'cast', actors_df, 'full_name', 'actor_id')
    show_director_df = create_bridge_table(df, 'show_id', 'director', directors_df, 'full_name', 'director_id')
    show_country_df = create_bridge_table(df, 'show_id', 'country', countries_df, 'country_name', 'country_id')
    show_category_df = create_bridge_table(df, 'show_id', 'listed_in', categories_df, 'category_name', 'category_id')

    # ---------------------------------------------------------
    # PREPARAR LA TABLA PRINCIPAL (shows)
    # Mapeamos los textos a sus respectivos IDs (Llaves Foráneas)
    # ---------------------------------------------------------
    shows_df = df.copy()
    
    # Reemplazar texto por IDs (3FN)
    shows_df = shows_df.merge(types_df, left_on='type', right_on='type_name', how='left')
    shows_df = shows_df.merge(ratings_df, left_on='rating', right_on='code', how='left')
    
    # Seleccionar solo las columnas finales para la tabla shows
    shows_final = shows_df[[
        'show_id', 'type_id', 'title', 'release_year', 
        'rating_id', 'duration', 'description', 'date_added'
    ]]

    # ---------------------------------------------------------
    # REQUISITO 4: Exportación de resultados
    # ---------------------------------------------------------
    folder = 'dataset1'
    
    # Exportar Catálogos
    export_table(types_df, 'show_types', folder)
    export_table(ratings_df, 'ratings', folder)
    export_table(actors_df, 'actors', folder)
    export_table(directors_df, 'directors', folder)
    export_table(countries_df, 'countries', folder)
    export_table(categories_df, 'categories', folder)
    
    # Exportar Tablas Puente
    export_table(show_actor_df, 'show_actor', folder)
    export_table(show_director_df, 'show_director', folder)
    export_table(show_country_df, 'show_country', folder)
    export_table(show_category_df, 'show_category', folder)
    
    # Exportar Tabla Principal
    export_table(shows_final, 'shows', folder)

    print("--- Proceso Dataset 1 finalizado exitosamente ---")

if __name__ == "__main__":
    normalize_netflix()