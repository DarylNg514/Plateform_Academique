# Utiliser une image de base Python
FROM python:3.11-slim

# Installer les dépendances système nécessaires pour mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    && apt-get clean

# Mettre à jour pip
RUN pip install --upgrade pip

# Définir le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copier uniquement requirements.txt pour installer les dépendances
COPY requirements.txt /app/

# Installer les dépendances du projet
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers du projet vers le conteneur
COPY . /app/

# Collecter les fichiers statiques (nécessaire pour WhiteNoise ou le déploiement)
RUN python manage.py collectstatic --noinput

# Exposer le port sur lequel Django fonctionnera
EXPOSE 8001

# Lancer le serveur Django avec les migrations
CMD ["sh", "-c", "python manage.py migrate && gunicorn Projet_stage.wsgi:application --bind 0.0.0.0:8001"]
