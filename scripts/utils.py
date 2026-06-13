import os
import pandas as pd
from sqlalchemy import create_engine

def get_db_engine():
    db_user = os.environ.get('DB_USER', 'root')
    db_pass = os.environ.get('DB_PASSWORD', 'hola1938')
    db_host = os.environ.get('DB_HOST', 'db') 
    db_port = os.environ.get('DB_PORT', '3306')
    db_name = os.environ.get('DB_NAME', 'normalizacion_db')
    connection_string = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
    return create_engine(connection_string)

def init_sql_files(dataset_name):
    """
    Prepara un único archivo unificado para DDL y otro para DML por cada dataset.
    Se debe llamar al inicio de cada script de normalización.
    """
    os.makedirs("sql/ddl", exist_ok=True)
    os.makedirs("sql/dml", exist_ok=True)
    
    # Limpiamos los archivos (o los creamos vacíos si no existen)
    open(f"sql/ddl/{dataset_name}_schema.sql", "w", encoding='utf-8').close()
    open(f"sql/dml/{dataset_name}_data.sql", "w", encoding='utf-8').close()

def export_table(df, table_name, dataset_folder):
    """
    Exporta un DataFrame a CSV, MySQL y anexa a los archivos físicos DDL/DML.
    """
    engine = get_db_engine()
    
    # 1. Exportar a CSV (Modificado para ir directo a la raíz del proyecto)
    csv_dir = f"normalized/{dataset_folder}"
    os.makedirs(csv_dir, exist_ok=True)
    df.to_csv(os.path.join(csv_dir, f"{table_name}.csv"), index=False)

    # 2. Exportar directamente a la Base de Datos MySQL
    try:
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        print(f"[*] Tabla '{table_name}' insertada en MySQL.")
    except Exception as e:
        print(f"[!] Error en MySQL para '{table_name}': {e}")

    # 3. Generar Script DDL (Create Table) físicamente - Anexando al archivo consolidado
    ddl_file = f"sql/ddl/{dataset_folder}_schema.sql"
    ddl_statement = pd.io.sql.get_schema(df, table_name, con=engine)
    with open(ddl_file, "a", encoding='utf-8') as f:
        f.write(ddl_statement + ";\n\n")

    # 4. Generar Script DML (Insert) físicamente - Anexando al archivo consolidado
    dml_file = f"sql/dml/{dataset_folder}_data.sql"
    with open(dml_file, "a", encoding='utf-8') as f:
        f.write(f"-- Inserciones de ejemplo para la tabla: {table_name}\n")
        # Generar las primeras 5 líneas de ejemplo DML
        for index, row in df.head(5).iterrows():
            valores = ", ".join(["'" + str(x).replace('"', '').replace("'", "") + "'" for x in row.values])
            f.write(f"INSERT INTO {table_name} VALUES ({valores});\n")
        f.write("\n")
            
def create_bridge_table(df, id_col_main, col_to_split, entity_df, entity_name_col, entity_id_col):
    """
    Función auxiliar para normalizar columnas multivaluadas.
    """
    temp_df = df[[id_col_main, col_to_split]].dropna().copy()
    
    temp_df[col_to_split] = temp_df[col_to_split].astype(str).str.split(', ')
    exploded_df = temp_df.explode(col_to_split)
    
    exploded_df[col_to_split] = exploded_df[col_to_split].str.strip()
    
    bridge_df = exploded_df.merge(
        entity_df, 
        left_on=col_to_split, 
        right_on=entity_name_col, 
        how='left'
    )
    
    return bridge_df[[id_col_main, entity_id_col]].drop_duplicates()