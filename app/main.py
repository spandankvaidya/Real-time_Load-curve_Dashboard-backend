from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.wsgi import WSGIMiddleware
from app.model import load_and_predict
from app.dash_app import server as dash_wsgi_app  # This is the WSGI app from Dash

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root
@app.get("/")
def root():
    return HTMLResponse("<h3>✅ FastAPI backend is running.</h3><p>Visit <a href='/dashboard'>/dashboard</a> to view the graph.</p>")

# Forecast API
@app.get("/run-forecast")
def run_forecast(date: str = Query(..., regex=r"\d{4}-\d{2}-\d{2}")):
    success = load_and_predict(date)
    if success:
        return JSONResponse(content={"status": "success", "date": date})
    else:
        return JSONResponse(content={"status": "error", "message": f"CSV not found for {date}"}, status_code=400)

# ✅ Mount Dash app at /dashboard
app.mount("/dashboard", WSGIMiddleware(dash_wsgi_app))

# 🟡 Local run only
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
