from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from app.model import load_and_predict
from app.dash_app import launch_dash_app
import threading
from fastapi.responses import HTMLResponse
app = FastAPI()

@app.get("/")
def root():
    return HTMLResponse(content="<h3>✅ FastAPI backend is running.</h3>")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Launch Dash app in background
threading.Thread(target=launch_dash_app, daemon=True).start()

@app.get("/run-forecast")
def run_forecast(date: str = Query(..., regex=r"\d{4}-\d{2}-\d{2}")):
    success = load_and_predict(date)
    if success:
        return JSONResponse(content={"status": "success", "date": date})
    else:
        return JSONResponse(content={"status": "error", "message": f"CSV not found for {date}"}, status_code=400)
