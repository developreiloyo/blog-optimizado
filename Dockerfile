# Imagen base de Python
FROM python:3.11-slim

# Configurar variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de la app
WORKDIR /app

# Instalar dependencias del sistema necesarias para Django + PostgreSQL + Pillow
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       build-essential \
       libpq-dev \
       gcc \
       python3-dev \
       musl-dev \
       libjpeg-dev \
       zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . /app/

# Exponer el puerto (el que usa Hostinger normalmente es 8000)
EXPOSE 8000

# Comando de inicio (Gunicorn con workers para producción)
CMD ["gunicorn", "blog_optimizado.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]

