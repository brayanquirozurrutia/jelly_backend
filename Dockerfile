FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requerimientos y instalar dependencias
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación
COPY . .

# Definir variables de entorno
ENV PYTHONUNBUFFERED=1

# Instalar gunicorn y generar archivos estáticos
RUN pip install gunicorn
RUN python manage.py collectstatic --no-input

# Exponer el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "jelly_backend.wsgi:application", "--log-level", "debug"]
