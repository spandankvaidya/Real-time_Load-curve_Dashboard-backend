from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.wsgi import WSGIMiddleware
from app.model import load_and_predict
from app.dash_app import create_dash_app

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"status": "FastAPI backend is running."}

@app.get("/run-forecast")
def run_forecast(date: str = Query(..., regex=r"\d{4}-\d{2}-\d{2}")):
    success = load_and_predict(date)
    if success:
        return {"status": "success", "date": date}
    return JSONResponse(status_code=404, content={"error": "CSV not found"})

# Mount Dash app
dash_app = create_dash_app(app)
app.mount("/dashboard", WSGIMiddleware(dash_app.server))
