# Uso de una imagen ligera de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de dependencias
COPY requirements.txt .

# Instalar dependencias (pandas, SQLAlchemy, pymysql, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la estructura del proyecto al contenedor
COPY . .

# Comando por defecto para ejecutar tu script principal de automatización
# Ajusta el nombre del script según con cuál desees iniciar
CMD ["python", "scripts/normalize_dataset1.py"]