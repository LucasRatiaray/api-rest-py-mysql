# Utiliser une image de base officielle Python
FROM python:3.9-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier de dépendances et installer les dépendances
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste de l'application dans le répertoire de travail
COPY . .

# Exposer le port sur lequel l'application tourne
EXPOSE 5000

# Définir la commande pour lancer l'application
CMD ["python", "run.py"]
