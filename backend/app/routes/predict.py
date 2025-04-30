from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import joblib
from sqlalchemy.orm import Session
from app.models.model_phishingresult import PhishingResult
from app.db import get_db
import numpy as np

# Load models and vectorizers
model_phishing = joblib.load("./ml_model/svm_model_phishing.joblib")
vectorizer_phishing = joblib.load("./ml_model/svm_vectorizer_phishing.joblib")

class TextRequest(BaseModel):
    text: str

predict_router = APIRouter(tags=["Predict"])

@predict_router.post("/")
def predict_phishing(request: TextRequest, db: Session = Depends(get_db)):
    if not request.text:
        raise HTTPException(status_code=400, detail="No text provided")
    
    text_vectorized = vectorizer_phishing.transform([request.text])
    prediction = model_phishing.predict(text_vectorized)
    prediction_proba = model_phishing.predict_proba(text_vectorized)
    result = "Phishing" if prediction[0] == 1 else "Not Phishing"
    accuracy = float(max(prediction_proba[0]))  # Convert np.float64 to native Python float
    
    # Save the result to the database
    phishing_result = PhishingResult(
        textInput=request.text,
        accuracy=accuracy,
        verdict=result
    )
    db.add(phishing_result)
    db.commit()
    db.refresh(phishing_result)
    
    return {"prediction": result, "details": prediction_proba.tolist(), "phishingresultID": phishing_result.phishingresultID}