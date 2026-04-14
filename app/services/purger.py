import os
import time
import shutil

def purge_desktop():
    # Paths
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    archive = os.path.join(desktop, "Zenith_Vault")
    
    if not os.path.exists(archive):
        os.makedirs(archive)

    now = time.time()
    two_days = 2 * 86400  # Seconds in 2 days
    count = 0

    for item in os.listdir(desktop):
        path = os.path.join(desktop, item)
        
        # Skip the Vault itself and system shortcuts
        if item == "Zenith_Vault" or item.endswith(".lnk") or os.path.isdir(path):
            continue
            
        # Check age
        if (now - os.path.getmtime(path)) > two_days:
            shutil.move(path, os.path.join(archive, item))
            count += 1
            
    return f"🧹 Desktop Purged: {count} old items moved to Vault."