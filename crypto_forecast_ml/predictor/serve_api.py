# predictor/serve_api.py
import logger
from fastapi import FastAPI, Query
from crypto_forecast_ml.data_loader import load_crypto_data
from crypto_forecast_ml.features.technical_indicators import add_technical_indicators
from crypto_forecast_ml.features.target_builder import build_targets
from crypto_forecast_ml.predictor.predict import predict_direction
from crypto_forecast_ml.data_loader import load_crypto_data_custom_range

import traceback
app = FastAPI()
import logging
import traceback
from datetime import datetime,timezone
from zoneinfo import ZoneInfo

# ✅ Initialise le logger proprement
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/predict-latest")
def predict_latest(symbol: str = Query("BTCUSDT", description="Crypto symbol")):
    try:
        logger.info(f"🔵 API called with symbol: {symbol}")
        df = load_crypto_data(symbol=symbol, days=3)
        df = add_technical_indicators(df)
        df = build_targets(df)
        df_pred = predict_direction(df)

        result = df_pred.tail(10).to_dict(orient="records")
        return {"symbol": symbol, "predictions": result}

    except Exception as e:
        logger.error("🔥 Exception occurred:")
        traceback.print_exc()  # Affiche la stack trace complète
        return {"error": str(e)}




paris = ZoneInfo("Europe/Paris")
FMT_IN = "%Y-%m-%dT%H:%M"           # 2025-07-06T09:15

@app.get("/load-data")
def load_data(
    symbol: str = Query(...),
    start_date: str = Query(..., description="YYYY-MM-DDTHH:MM 🇫🇷"),
    end_date:   str = Query(..., description="YYYY-MM-DDTHH:MM 🇫🇷")
):
    # 👉 parse + convert -> UTC
    start_utc = (datetime.strptime(start_date, FMT_IN)
                           .replace(tzinfo=paris)
                           .astimezone(timezone.utc))
    end_utc   = (datetime.strptime(end_date,   FMT_IN)
                           .replace(tzinfo=paris)
                           .astimezone(timezone.utc))

    df = load_crypto_data_custom_range(symbol=symbol,
                                       start_date=start_utc,
                                       end_date=end_utc)

    return {
        "symbol": symbol,
        "start_date": start_utc.isoformat(),
        "end_date":   end_utc.isoformat(),
        "data": df.to_dict(orient="records")
    }





#uvicorn crypto_forecast_ml.predictor.serve_api:app --port 8006 --reload
