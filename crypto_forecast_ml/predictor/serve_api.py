# predictor/serve_api.py
#import logger
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
from datetime import datetime

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

@app.get("/load-data")
def load_data(
    symbol: str = Query(..., description="Crypto symbol, e.g. BTCUSDT"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD")
):
    try:
        logger.info(f"📥 /load-data called with: symbol={symbol}, start={start_date}, end={end_date}")
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")

        df = load_crypto_data_custom_range(symbol=symbol, start_date=start_date, end_date=end_date)
        result = df.to_dict(orient="records")
        return {"symbol": symbol, "start_date": start_date, "end_date": end_date, "data": result}

    except Exception as e:
        logger.error("🔥 Error in /load-data")
        traceback.print_exc()
        return {"error": str(e)}



