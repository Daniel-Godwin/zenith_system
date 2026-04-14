import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.services.automation import FileOrganizer

class ZenithHandler(FileSystemEventHandler):
    def __init__(self, folder_to_track):
        # Normalize the path for Windows
        self.folder_to_track = os.path.normpath(folder_to_track)
        self.organizer = FileOrganizer(self.folder_to_track)
        self.last_run = 0

    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Ignore temp files from browsers
        if event.src_path.endswith(('.tmp', '.crdownload', '.part')):
            return

        current_time = time.time()
        if current_time - self.last_run < 2: 
            return
            
        self.last_run = current_time
        
        # INDUSTRIAL SLEEP: Give Windows time to release the file handle
        time.sleep(1) 
        
        print(f"🚀 Ghost Protocol: Activity detected in {os.path.basename(event.src_path)}. Scanning...")
        result = self.organizer.clean()
        print(f"✔️ {result}")

def start_ghost_service(target_path=None):
    # Use the path passed from main.py, or fallback to the default
    if target_path is None:
        target_path = os.path.abspath(os.path.join(os.path.expanduser("~"), "Downloads"))
    
    path = os.path.normpath(target_path)
    event_handler = ZenithHandler(path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()
    
    print(f"🚀 Zenith Ghost Protocol Active on: {path}")
    
    try:
        while True:
            time.sleep(1)
    except Exception:
        observer.stop()
    observer.join()