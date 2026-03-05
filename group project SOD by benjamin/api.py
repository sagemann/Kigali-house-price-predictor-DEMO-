from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

app = FastAPI(title="Kigali House Price Predictor")
model = joblib.load('kigali_house_model.pkl')

client = MongoClient("mongodb://localhost:27017/")
db = client['houseprices']
collection = db['predictions']

class House(BaseModel):
    neighborhood: str
    plot_size_sqm: float
    bedrooms: int
    bathrooms: int

@app.post("/predict")
def predict_price(house: House):

    input_df = pd.DataFrame([house.dict()])

    predicted = model.predict(input_df)[0]

    low = predicted * 0.9
    high = predicted * 1.1

    record = {
        "input": house.dict(),
        "predicted_price_millions_rwf": round(float(predicted), 1),
        "price_range": f"{round(low, 1)} - {round(high, 1)} million RWF",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "note": "Predicted by Random Forest uncles"
    }

    collection.insert_one(record)

    return {
        "status": "success",
        "predicted_price": round(float(predicted), 1),
        "range": f"{round(low, 1)} - {round(high, 1)} million RWF",
        "saved_to_db": True
    }

@app.get("/")
def root():
    return {"message": "Kigali House API running – hit /predict with POST"}
