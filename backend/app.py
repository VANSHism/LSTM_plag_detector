from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Annotated

from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
import logging

from utils.text_preprocess import transform_text

import pickle
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BACKEND_DIR = Path(__file__).resolve().parent
MODEL_DIR = BACKEND_DIR / 'model'

# Lazy loading of model and tokenizer to avoid startup issues
model = None
tokenizer = None

def load_model():
    """Load model and tokenizer with error handling."""
    global model, tokenizer
    if model is None or tokenizer is None:
        try:
            logger.info("Loading model and tokenizer...")
            model_path = MODEL_DIR / 'Siamese_LSTM_model.pkl'
            tokenizer_path = MODEL_DIR / 'tokenizer.pkl'
            
            if not model_path.exists():
                raise FileNotFoundError(f"Model file not found: {model_path}")
            if not tokenizer_path.exists():
                raise FileNotFoundError(f"Tokenizer file not found: {tokenizer_path}")
            
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            
            with open(tokenizer_path, 'rb') as f:
                tokenizer = pickle.load(f)
            
            logger.info("Model and tokenizer loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model/tokenizer: {e}")
            raise

# Load model at startup (but with error handling)
load_model()

app = FastAPI()

# Allow cross-origin requests from Streamlit / browsers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    source_text: Annotated[str, Field(..., description="Source text here")]
    plag_text: Annotated[str, Field(..., description="Plagiarized text here")]
    
max_len=50

@app.get('/')
def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "LSTM Plagiarism Detection API is running"}

@app.get('/health')
def health():
    """Health check endpoint with model status."""
    model_status = "loaded" if model is not None and tokenizer is not None else "not loaded"
    return {
        "status": "ok",
        "model_status": model_status,
        "message": "API is healthy"
    }

@app.post('/predict')
def predict_plag(data: UserInput):
    # Ensure model is loaded
    if model is None or tokenizer is None:
        load_model()
    
    #Transform text
    src_cleaned = transform_text(data.source_text)
    plag_cleaned = transform_text(data.plag_text)

    #Tokenize to sequence
    src_seq = tokenizer.texts_to_sequences([src_cleaned])
    plag_seq = tokenizer.texts_to_sequences([plag_cleaned])

    #Pad 
    src_pad = pad_sequences(src_seq, maxlen=max_len)
    plag_pad = pad_sequences(plag_seq, maxlen=max_len)

    #Predict
    pred = model.predict([src_pad, plag_pad], verbose=0)[0][0]
    result = int(round(pred))
    confidence = float(pred)
    
    #display
    return JSONResponse(status_code=200, content = {'predicted_category': result, 'confidence_score': confidence})
    


    
