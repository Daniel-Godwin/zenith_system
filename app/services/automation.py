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
        
        # PRO PROTECTED LIST: Zenith ignores these to avoid moving its own folders
        protected_folders = [
            "Images", "Documents", "Finance", "Work", "Education", 
            "Development", "Archives", "Media", "Health", "Legal", 
            "Personal", "Python_Env"
        ]

        for root, dirs, files in os.walk(self.folder_path):
            # GUARDRAIL 1: Skip dev environments
            if any(x in root for x in ["venv", ".venv", "__pycache__", "node_modules", ".git"]):
                continue

            # GUARDRAIL 2: Skip folders we already organized
            if any(folder in root for folder in protected_folders):
                continue

            for file in files:
                # 1. SKIP SYSTEM FILES
                if file.endswith(('.pyc', '.pyd', '.pyi', '.dll', '.exe', '.so', '.dylib')):
                    continue

                # 2. DEFINE NAME AND EXTENSION
                name, extension = os.path.splitext(file)
                ext_clean = extension[1:].lower()

                # 3. SMART CLASSIFICATION
                smart_category = self.brain.predict(name)
                
                # 4. DECIDE TARGET FOLDER
                if ext_clean in ["whl", "ipynb", "py"]:
                    target_folder_name = "Python_Env"
                elif smart_category != "Unclassified":
                    target_folder_name = smart_category
                else:
                    # Fallback logic
                    if ext_clean in ["zip", "rar", "7z", "tar"]:
                        target_folder_name = "Archives"
                    elif ext_clean in ["jpg", "jpeg", "png", "gif"]:
                        target_folder_name = "Images"
                    elif ext_clean in ["pdf", "doc", "docx", "txt"]:
                        target_folder_name = "Documents"
                    else:
                        target_folder_name = ext_clean if ext_clean else "Misc"

                # 5. EXECUTE MOVE
                target_folder = os.path.join(self.folder_path, target_folder_name)
                os.makedirs(target_folder, exist_ok=True)
                
                source_path = os.path.join(root, file)
                destination_path = os.path.join(target_folder, file)

                if source_path != destination_path:
                    try:
                        shutil.move(source_path, destination_path)
                        moved_files_history.append({
                            "file": file, 
                            "dest": target_folder_name
                        })
                    except Exception as e:
                        print(f"DEBUG Error moving {file}: {e}")

        return {
            "count": len(moved_files_history),
            "history": moved_files_history[-10:] 
        }