from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.wsgi import WSGIMiddleware

from app.model import load_and_predict, predicted_values, actual_values, time_ticks
from app.dash_app import dash_app  # <- import Dash app instance here

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Mount Dash app at /dashboard
app.mount("/dashboard", WSGIMiddleware(dash_app.server))

# Root route
@app.get("/")
def root():
    return HTMLResponse(content="<h3>✅ FastAPI backend is running.</h3>")

# Forecast route
@app.get("/run-forecast")
def run_forecast(date: str = Query(..., regex=r"\d{4}-\d{2}-\d{2}")):
    success = load_and_predict(date)
    if success:
        return JSONResponse(content={"status": "success", "date": date})
    else:
        return JSONResponse(content={"status": "error", "message": f"CSV not found for {date}"}, status_code=400)
