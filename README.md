# 🌌 Zenith OS | v2.0 Industrial File Intelligence

Zenith OS is a localized, high-performance automation suite designed to manage digital clutter using the **Ghost Protocol**. It features a real-time dashboard, an AI-driven file classifier, and background observation services.

## 🚀 Key Features

* **Ghost Protocol (Real-time Observation):** A background thread that monitors your Downloads folder every 10 seconds and automatically organizes files.
* **Smart Classification:** Uses a custom keyword-based "Brain" to categorize files into logical sectors (Finance, Dev, Media, etc.) instead of just relying on extensions.
* **Desktop Purge & Vault:** A secondary cleanup system that sweeps old Desktop files into a secure "Zenith Vault" to maintain a clean workspace.
* **Industrial Dashboard:** A dark-mode control center built with FastAPI and modern CSS for manual overrides and activity tracking.

---

## 🛠️ System Architecture

* **Backend:** Python 3.x, FastAPI, Uvicorn
* **Frontend:** HTML5, CSS3 (Industrial Dark Theme), JavaScript (Async Fetch API)
* **Core Services:** * `FileOrganizer`: Recursive sorting logic with protection for system files.
    * `GhostService`: Multi-threaded watchdog for background tasks.
    * `SmartClassifier`: Keyword-weighted categorization engine.

---

## 📦 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/zenith_system.git](https://github.com/YOUR_USERNAME/zenith_system.git)
   cd zenith_system
