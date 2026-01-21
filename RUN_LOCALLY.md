# How to Run the Project Locally

## Prerequisites
1. Python 3.8+ installed
2. All dependencies installed (see requirements.txt)

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Start the Backend Server

Open a terminal and run:

```bash
cd backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at: `http://localhost:8000`

You can test it by visiting: `http://localhost:8000/docs` (FastAPI auto-generated docs)

## Step 3: Start the Frontend (Streamlit)

Open a **new terminal** (keep the backend running) and run:

**On Windows (PowerShell):**
```powershell
$env:API_URL="http://localhost:8000"
cd frontend
streamlit run frontend.py
```

**On Windows (CMD):**
```cmd
set API_URL=http://localhost:8000
cd frontend
streamlit run frontend.py
```

**On Linux/Mac:**
```bash
export API_URL=http://localhost:8000
cd frontend
streamlit run frontend.py
```

The frontend will open automatically in your browser at: `http://localhost:8501`

## Step 4: Test the Application

1. Enter a source text in the first text area
2. Enter text to check for plagiarism in the second text area
3. Click "🔍 Predict" button
4. View the prediction result

## Troubleshooting

- **Backend won't start**: Make sure port 8000 is not in use
- **Frontend can't connect**: Verify API_URL is set correctly and backend is running
- **Model not found**: Ensure `backend/model/Siamese_LSTM_model.pkl` and `backend/model/tokenizer.pkl` exist

## Quick Test Commands

Test backend directly:
```bash
curl -X POST "http://localhost:8000/predict" -H "Content-Type: application/json" -d "{\"source_text\":\"hello world\",\"plag_text\":\"hello world\"}"
```

