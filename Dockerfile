FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Encadenamos los tres scripts. 
# El operador && asegura que el siguiente script solo corra si el anterior fue exitoso.
CMD ["sh", "-c", "python scripts/normalize_dataset1.py && python scripts/normalize_dataset2.py && python scripts/normalize_dataset3.py"]