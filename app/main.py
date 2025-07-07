from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.model import load_and_predict
from app.dash_app import create_dash_app
from fastapi.responses import JSONResponse, HTMLResponse
import threading
import os

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return HTMLResponse(content="<h3>✅ FastAPI backend is running.</h3>")

@app.get("/run-forecast")
def run_forecast(date: str):
    success = load_and_predict(date)
    if success:
        return JSONResponse(content={"status": "success", "date": date})
    else:
        return JSONResponse(content={"status": "error", "message": f"CSV not found for {date}"}, status_code=400)

# Launch Dash server on a separate port (e.g. 8050)
def run_dash():
    dash_app = create_dash_app()
    dash_app.run_server(host="0.0.0.0", port=8050)

# Background thread for Dash
threading.Thread(target=run_dash, daemon=True).start()
