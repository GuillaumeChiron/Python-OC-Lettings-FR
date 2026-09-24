FROM python:3.13-slim

# Pas de fichiers .pyc, logs affichés immédiatement (sans mise en tampon)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dépendances copiées seules en premier pour profiter du cache Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Clé temporaire limitée à cette commande : settings.py exige une SECRET_KEY,
# mais aucune clé ne doit rester dans l'image
RUN SECRET_KEY=build-only python manage.py collectstatic --noinput

EXPOSE 8000

# PORT est fourni par l'hébergeur, 8000 par défaut en local
CMD ["sh", "-c", "exec gunicorn oc_lettings_site.wsgi:application --bind 0.0.0.0:${PORT:-8000}"]
