# Étape 1 : Utilise une image Python légère
FROM python:3.11-slim

# Étape 2 : Définir le dossier de travail
WORKDIR /app

# Étape 3 : Copier uniquement les requirements pour optimiser le cache
COPY crypto_forecast_ml/requirements.txt .

# Étape 4 : Installer les dépendances + watchdog pour --reload
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt watchdog

# Étape 5 : Copier le reste du code (code + structure)
COPY . .

# Étape 6 : Exposer le port
EXPOSE 8000

# Étape 7 : Par défaut (en prod), on pourrait mettre sans reload,
# mais ici, le CMD est redéfini dans docker-compose.yml
CMD ["uvicorn", "crypto_forecast_ml.predictor.serve_api:app", "--host", "0.0.0.0", "--port", "8000"]
