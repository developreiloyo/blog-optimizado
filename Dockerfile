# Usa una imagen ligera de Python
FROM python:3.11-slim

LABEL maintainer="reinaldo@mikai.blog"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Dependencias del sistema (Pillow y compilaciones)
RUN apt-get update && apt-get install -y \
    build-essential \
    libjpeg-dev \
    libpng-dev \
    libwebp-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar requerimientos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Directorios estáticos y media
RUN mkdir -p staticfiles media

# Copiar el código del proyecto
COPY . .

RUN chmod -R 755 /app

# Puerto (usar 80 para producción en EasyPanel)
EXPOSE 80

# Comando final: migraciones, estáticos y gunicorn
CMD ["sh", "-c", "python manage.py migrate --noinput && \
                 python manage.py collectstatic --noinput && \
                 gunicorn personalblog.wsgi:application --bind 0.0.0.0:80 --workers 3"]
