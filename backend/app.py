from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Annotated

from tensorflow.keras.preprocessing.sequence import pad_sequences

from utils.text_preprocess import transform_text

import pickle
from pathlib import Path
BACKEND_DIR = Path(__file__).resolve().parent
MODEL_DIR = BACKEND_DIR / 'model'

#Import the Model (file-relative paths)
with open(MODEL_DIR / 'Siamese_LSTM_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open(MODEL_DIR / 'tokenizer.pkl', 'rb') as f:
    tokenizer = pickle.load(f)

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

@app.post('/predict')
def predict_plag(data: UserInput):
    
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
    


    
