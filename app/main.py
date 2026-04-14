import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from app.services.automation import FileOrganizer
import threading
from app.services.observer import start_ghost_service

app = FastAPI(title="Zenith OS")

# Get the absolute path to Downloads once
DOWNLOADS_PATH = os.path.abspath(os.path.join(os.path.expanduser("~"), "Downloads"))

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard")

@app.get("/dashboard")
async def get_dashboard():
    return FileResponse("app/static/index.html")

@app.get("/organize")
async def start_organize():
    # Use the normalized path
    organizer = FileOrganizer(DOWNLOADS_PATH)
    return organizer.clean()

@app.on_event("startup")
async def startup_event():
    # Pass the normalized path to the ghost service
    threading.Thread(target=start_ghost_service, args=(DOWNLOADS_PATH,), daemon=True).start()