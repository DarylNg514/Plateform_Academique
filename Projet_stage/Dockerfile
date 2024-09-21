# Utiliser une image de base Python
FROM python:3.11-slim

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

# Exposer le port sur lequel Django fonctionnera
EXPOSE 8001

# Lancer le serveur Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
