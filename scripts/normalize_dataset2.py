import pandas as pd
from utils import export_table, init_sql_files

def normalize_ecommerce():
    print("Iniciando normalización del Dataset 2 (E-commerce)...")
    
    # Inicializa y limpia los archivos SQL unificados para este dataset
    init_sql_files('dataset2')
    
    # ---------------------------------------------------------
    # REQUISITO 1: Lectura de datos originales y validación
    # ---------------------------------------------------------
    raw_path = 'data/raw/data.csv' 
    try:
        # Los datasets de e-commerce suelen requerir esta codificación
        df = pd.read_csv(raw_path, encoding='unicode_escape')
    except FileNotFoundError:
        print(f"[!] Error: No se encontró el archivo en {raw_path}")
        return

    # Limpieza: Eliminamos registros que rompen la integridad relacional
    # (No podemos tener ventas sin cliente o sin producto)
    df = df.dropna(subset=['InvoiceNo', 'StockCode', 'CustomerID']).copy()

    # ---------------------------------------------------------
    # REQUISITO 2 y 3: Transformaciones a 2FN y 3FN
    # ---------------------------------------------------------
    
    # 3FN: Catálogo Maestro de Clientes (Extraemos la dependencia transitiva del País)
    customers_df = df[['CustomerID', 'Country']].drop_duplicates(subset=['CustomerID'])
    
    # 2FN: Catálogo Maestro de Productos (Elimina dependencias parciales)
    products_df = df[['StockCode', 'Description', 'UnitPrice']].drop_duplicates(subset=['StockCode'])

    # 2FN/3FN: Tabla de Cabecera (Facturas - Transacción General)
    invoices_df = df[['InvoiceNo', 'InvoiceDate', 'CustomerID']].drop_duplicates(subset=['InvoiceNo'])

    # 1FN/2FN: Tabla de Detalle (Facturas_Productos - Relación M:N)
    # Usamos groupby para agrupar y sumar las cantidades si un cajero escaneó 
    # el mismo producto dos veces en el mismo ticket
    invoice_details_df = df.groupby(['InvoiceNo', 'StockCode'])['Quantity'].sum().reset_index()

    # ---------------------------------------------------------
    # REQUISITO 4: Exportación de resultados
    # ---------------------------------------------------------
    folder = 'dataset2'
    
    # Exportamos en orden lógico (primero catálogos, luego transacciones)
    export_table(customers_df, 'customers', folder)
    export_table(products_df, 'products', folder)
    export_table(invoices_df, 'invoices', folder)
    export_table(invoice_details_df, 'invoice_details', folder)

    print("--- Proceso Dataset 2 finalizado exitosamente ---")

if __name__ == "__main__":
    normalize_ecommerce()