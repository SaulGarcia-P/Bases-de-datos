import pandas as pd
from utils import export_table, init_sql_files

def normalize_hospital():
    print("Iniciando normalización del Dataset 3 (Hospital)...")
    
    # Inicializa y limpia los archivos SQL unificados para este dataset
    init_sql_files('dataset3')
    
    # ---------------------------------------------------------
    # REQUISITO 1: Lectura de datos originales y validación
    # ---------------------------------------------------------
    raw_path = 'data/raw/dataset.csv' 
    try:
        df = pd.read_csv(raw_path)
    except FileNotFoundError:
        print(f"[!] Error: No se encontró el archivo en {raw_path}")
        return

    # ---------------------------------------------------------
    # REQUISITO 2 y 3: Transformaciones a 2FN y 3FN
    # ---------------------------------------------------------
    
    # 2FN: Catálogo Maestro de Pacientes (Evita repetición demográfica)
    patients_df = df[['patient_id', 'age', 'gender', 'ethnicity', 'height']].drop_duplicates(subset=['patient_id'])

    # 3FN: Catálogo de Hospitales (Extracción de dependencia transitiva)
    hospitals_df = pd.DataFrame(df['hospital_id'].dropna().unique(), columns=['hospital_id'])
    
    # 3FN: Catálogo de Unidades de Cuidados Intensivos (UCIs)
    icus_df = df[['icu_id', 'icu_type', 'icu_stay_type']].drop_duplicates(subset=['icu_id'])

    # Tabla Principal Transaccional (Encuentros / Ingresos)
    # Retiramos los atributos descriptivos para dejar únicamente las FKs y las métricas vitales atómicas
    cols_to_drop = ['age', 'gender', 'ethnicity', 'height', 'icu_type', 'icu_stay_type']
    
    # Solo eliminamos las columnas si existen en el DataFrame original para evitar errores
    cols_to_drop_existing = [col for col in cols_to_drop if col in df.columns]
    encounters_df = df.drop(columns=cols_to_drop_existing)

    # ---------------------------------------------------------
    # REQUISITO 4: Exportación de resultados
    # ---------------------------------------------------------
    folder = 'dataset3'
    
    # Exportamos los catálogos primero para respetar la integridad referencial lógica
    export_table(patients_df, 'patients', folder)
    export_table(hospitals_df, 'hospitals', folder)
    export_table(icus_df, 'icus', folder)
    
    # Finalmente exportamos la tabla transaccional pesada
    export_table(encounters_df, 'encounters', folder)

    print("--- Proceso Dataset 3 finalizado exitosamente ---")

if __name__ == "__main__":
    normalize_hospital()