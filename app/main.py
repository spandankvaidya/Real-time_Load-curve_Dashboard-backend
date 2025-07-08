# In app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.responses import HTMLResponse
from app.dash_app import create_dash_app

# ---- REMOVE THIS SECTION ----
# from app.model import load_and_predict
# import threading
# -----------------------------

# ---- REMOVE app/globals.py, it is no longer needed ----

app = FastAPI()

# CORS setup remains the same
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For production, you might want to restrict this to your Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return HTMLResponse(content="<h3>✅ FastAPI backend with mounted Dash app is running.</h3>")

# ---- REMOVE THE /run-forecast ENDPOINT ----
# @app.get("/run-forecast") ...

# ---- MOUNT THE DASH APP CORRECTLY ----
dash_app = create_dash_app()
# The Dash app is mounted under the /dashboard prefix, which matches our frontend URL
app.mount("/dashboard", WSGIMiddleware(dash_app.server))

# ---- REMOVE THE THREADING LOGIC ----
# def run_dash(): ...
# threading.Thread(target=run_dash, daemon=True).start()
