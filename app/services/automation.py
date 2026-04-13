import os
import shutil
from app.services.classifier import SmartClassifier 

class FileOrganizer:
    """
    Industrial Service to handle recursive file organization with history tracking.
    """
    def __init__(self, folder_path: str):
        self.folder_path = folder_path
        self.brain = SmartClassifier() 
        self.categories = {
            "Images": ['jpg', 'jpeg', 'png', 'gif'],
            "Documents": ['pdf', 'doc', 'docx', 'txt']
        }

    def clean(self) -> dict:
        moved_files_history = []
        
        # PRO PROTECTED LIST
        protected_folders = [
            "Images", "Documents", "Finance", "Work", "Education", 
            "Development", "Archives", "Media", "Health", "Legal", 
            "Personal", "Python_Env"
        ]

        for root, dirs, files in os.walk(self.folder_path):
            # GUARDRAIL 1: Skip internal dev folders
            if any(x in root for x in ["venv", ".venv", "__pycache__", "node_modules", ".git", ".pytest_cache"]):
                continue

            # GUARDRAIL 2: Don't organize folders we already created
            if any(x in root for x in protected_folders):
                continue

            for file in files:
                # GUARDRAIL 3: Skip compiled/binary system files
                if file.endswith(('.pyc', '.pyd', '.pyi', '.dll', '.exe', '.so', '.dylib')):
                    continue

                name, extension = os.path.splitext(file)
                ext_clean = extension[1:].lower()

                # SMART CLASSIFICATION
                smart_category = self.brain.predict(name)
                
                # Logic to determine the target folder
                if ext_clean in ["whl", "ipynb", "py"]:
                    target_folder_name = "Python_Env"
                elif smart_category != "Unclassified":
                    target_folder_name = smart_category
                else:
                    if ext_clean in ["zip", "rar", "7z", "tar"]:
                        target_folder_name = "Archives"
                    else:
                        target_folder_name = ext_clean

                # --- MOVE LOGIC ---
                target_folder = os.path.join(self.folder_path, target_folder_name)
                os.makedirs(target_folder, exist_ok=True)
                
                source_path = os.path.join(root, file)
                destination_path = os.path.join(target_folder, file)

                if source_path != destination_path:
                    try:
                        shutil.move(source_path, destination_path)
                        # Record the move for the dashboard history
                        moved_files_history.append({
                            "file": file, 
                            "dest": target_folder_name
                        })
                    except Exception as e:
                        print(f"DEBUG: Could not move {file}: {e}")

        # Return a structured dictionary for the FastAPI response
        return {
            "count": len(moved_files_history),
            "history": moved_files_history[-10:]  # Send the last 10 moves
        }