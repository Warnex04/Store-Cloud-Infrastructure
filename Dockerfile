# Utiliser l'image officielle Python comme image de base.
FROM python:3.8

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers de l'application dans le conteneur
COPY . /app

# Exécuter l'application Python
CMD ["python", "./receipt.py"]
