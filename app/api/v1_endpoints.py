from fastapi import APIRouter
from app.services.automation import FileOrganizer

router = APIRouter()

@router.get("/automate/cleanup")
def trigger_cleanup():
    # Pointing to your specific Downloads folder
    worker = FileOrganizer(r"C:\Users\GODWIN DANIEL\Downloads")
    result = worker.clean()
    return {
        "status": "success",
        "system": "Zenith-V1",
        "detail": result
    }