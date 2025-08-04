# Usa una imagen estándar de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia requirements.txt primero
COPY requirements.txt .

# Instala dependencias con pip
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Expone el puerto (opcional, informativo)
EXPOSE 8000

# Comando de inicio
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py migrate && gunicorn personalblog.wsgi:application"]
