import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from app.services.automation import FileOrganizer

app = FastAPI(title="Zenith OS")

# 1. Mount the static folder (for CSS/JS/HTML)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# 2. HOME PAGE: Redirects http://127.0.0.1:8000/ directly to the dashboard
@app.get("/")
async def root():
    return RedirectResponse(url="/dashboard")

# 3. DASHBOARD: Serves the HTML file
@app.get("/dashboard")
async def get_dashboard():
    # Make sure your file is at app/static/index.html
    return FileResponse("app/static/index.html")

# 4. API: The button on the HTML page calls this
@app.get("/organize")
async def start_organize():
    path = os.path.join(os.path.expanduser("~"), "Downloads")
    organizer = FileOrganizer(path)
    # This now returns the dictionary with 'count' and 'history'
    return organizer.clean()