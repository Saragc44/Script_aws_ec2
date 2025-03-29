# Usar la imagen base de Python 3.8
FROM python:3.8

# Establecer el directorio de trabajo en el contenedor
WORKDIR /code

# Copiar el archivo de requisitos al contenedor
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación al contenedor
COPY src/ .

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "./app.py"]
