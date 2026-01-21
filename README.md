# LSTM Plagiarism Detection

FastAPI backend (Siamese LSTM) + Streamlit frontend for plagiarism detection. Backend is intended for Render; frontend for Streamlit Cloud.

## Project Structure
- `backend/` – FastAPI app, model + tokenizer (`backend/model`), text preprocessing (`backend/utils/text_preprocess.py`)
- `frontend/` – Streamlit UI (`frontend/frontend.py`)
- `notebook/` – Training/experiments (`notebook/LSTM_Plag_Detection.ipynb`)
- `render.yaml` – Render service definition for the backend
- `requirements.txt` – Python dependencies

## Prerequisites
- Python 3.8+
- pip

## Local Setup
```bash
pip install -r requirements.txt
```

### Run backend (FastAPI)
```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```
Docs: http://localhost:8000/docs

### Run frontend (Streamlit)
In a new terminal:
```bash
cd frontend
export API_URL="http://localhost:8000"   # PowerShell: $env:API_URL="http://localhost:8000"
streamlit run frontend.py
```
UI: http://localhost:8501

### Quick API test
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d "{\"source_text\":\"hello world\",\"plag_text\":\"hello world\"}"
```

## Deployment

### Backend on Render
- Uses `render.yaml`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn backend.app:app --host 0.0.0.0 --port $PORT`
- Ensure `backend/model/Siamese_LSTM_model.pkl` and `backend/model/tokenizer.pkl` are present.

### Frontend on Streamlit Cloud
- App entry: `frontend/frontend.py`
- Set secret/environment `API_URL` to your Render backend URL (e.g., `https://<render-service>.onrender.com`)

## Environment Variables / Secrets
- `API_URL`: Base URL of the FastAPI backend (used by Streamlit).

## Notes
- First run may download NLTK resources (stopwords, punkt, etc.) defined in `backend/utils/text_preprocess.py`.
- Model and tokenizer files are required for predictions: `backend/model/Siamese_LSTM_model.pkl`, `backend/model/tokenizer.pkl`.

## Troubleshooting
- Backend not starting: check port 8000 availability, dependencies installed.
- Frontend cannot reach API: verify `API_URL` and that backend is running/reachable.
- Model not found: confirm model/tokenizer files exist under `backend/model/`.

