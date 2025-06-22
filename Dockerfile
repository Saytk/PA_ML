# Étape 1 : Utilise une image de base Python légère
FROM python:3.11-slim

# Étape 2 : Définit le répertoire de travail
WORKDIR /app

# Étape 3 : Copie les fichiers de ton projet dans le conteneur
COPY . /app

# Étape 4 : Installe les dépendances
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r crypto_forecast_ml/requirements.txt

# Étape 5 : Expose le port utilisé par uvicorn (8000 par défaut)
EXPOSE 8000

# Étape 6 : Commande de lancement de l’API
CMD ["uvicorn", "crypto_forecast_ml.predictor.serve_api:app", "--host", "0.0.0.0", "--port", "8000"]
