# 👻 IoT Ghost Hunter

> **Enterprise-Grade Network Anomaly Detection System**
> *Built with Django, Scapy, Celery, Redis, and Scikit-Learn.*

![Project Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![Redis](https://img.shields.io/badge/Redis-Event%20Broker-red)

## 📖 Overview
**IoT Ghost Hunter** is a real-time network monitoring dashboard designed to identify devices on a local network and detect anomalous behavior using Machine Learning.

Unlike standard scanners that block the web interface while scanning, this project uses an **Event-Driven Architecture**. It offloads network scanning to background workers (Celery), streams data via an in-memory message broker (Redis), and pushes updates to the frontend instantly over WebSockets (Django Channels).

### 📸 Dashboard Preview
![Dashboard Screenshot]([https://github.com/user-attachments/assets/5c55ac54-2e4f-4f16-a992-001c724e6866])


---

## ✨ Key Features
* **🕵️ Real-Time Discovery:** Scans the local network (ARP) to identify active devices (IP, MAC, Vendor).
* **⚡ Asynchronous Engine:** Uses **Celery** to perform heavy network operations without freezing the UI.
* **📡 Live Updates:** Pushes scan results to the browser instantly via **WebSockets** (no page refresh required).
* **🧠 Anomaly Detection:** Integrated **Isolation Forest (ML)** algorithm that learns "normal" network patterns and alerts on suspicious spikes in device activity.
* **📊 Dynamic Visualization:** Interactive time-series traffic graph using **Chart.js**.

---

## 🏗️ Architecture

The application follows a distributed architecture to handle high-latency network operations:

1.  **Network Layer (Scapy):** Performs ARP broadcasting to discover devices.
2.  **Task Queue (Celery + Redis):** Manages asynchronous scanning tasks.
3.  **Intelligence Layer (Scikit-Learn):** Analyzes historical data to flag anomalies.
4.  **Real-Time Layer (Django Channels):** Pushes alerts to the browser via ASGI/WebSockets.
5.  **Presentation (Bootstrap 5):** A dark-mode, responsive dashboard.

---

## 🛠️ Technical Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python, Django | Core application logic and API. |
| **Network Engine** | Scapy | Raw packet manipulation and ARP scanning. |
| **Async Processing** | Celery | Background task scheduling and execution. |
| **Message Broker** | Redis | Communication between Django, Celery, and WebSockets. |
| **Real-Time** | Django Channels (Daphne) | WebSocket protocol handling (ASGI). |
| **ML Engine** | Scikit-Learn | Unsupervised Anomaly Detection (Isolation Forest). |
| **Database** | PostgreSQL | Persistent storage for device logs and history. |
| **Frontend** | Bootstrap 5, Chart.js | Responsive UI and Data Visualization. |

---

## 🚀 Setup & Installation

### Prerequisites
* Python 3.10+
* PostgreSQL
* Redis Server (Local or Docker)
* **Windows Users:** Must install [Npcap](https://npcap.com/) (Ensure "Install Npcap in WinPcap API-compatible Mode" is checked).

### 1. Clone the Repo
```bash
git clone [https://github.com/gokuls2253/iot-ghost-hunter.git]
cd iot-ghost-hunter
```

### 2. Environment Setup
```
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install Dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a .env file in the root directory:
```
# .env
DEBUG=True
SECRET_KEY=your_secret_key_here
# Database (Simple Setup)
DB_NAME=ghost_hunter
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
# Redis (Defaults are usually fine for local)
REDIS_HOST=localhost
REDIS_PORT=6379
#VirusTotal API Key
VT_API_KEY=your_api_key
```

### 4. Database Initialization
```
# Create the database in Postgres first, then run:
python manage.py migrate
```

🏃‍♂️ Running the System
This project requires three separate terminal processes to function fully.

Terminal 1: Redis & Celery Worker (The Engine)
Windows users must use --pool=solo due to OS limitations.
```
celery -A config worker -l info --pool=solo
```
Terminal 2: Celery Beat (The Scheduler)
Runs the scan automatically every 5 minutes.
```
celery -A config beat -l info
```
Terminal 3: Django Web Server (The UI)
```
python manage.py runserver
```
Access the dashboard at: http://127.0.0.1:8000

🧪 Testing & Usage
Manual Scan Trigger
To force a scan immediately without waiting for the scheduler:
```
python manage.py shell
```
```python
from network.tasks import scan_network
scan_network.delay()
```
Simulating an Anomaly
The ML model requires about 10-20 "normal" scans to train. To see the Red Alert UI immediately, you can force the flag in network/tasks.py or connect multiple new devices to your network simultaneously.

⚠️ Troubleshooting
1. "Permission Denied" / Scapy Errors:
  - Ensure you are running your terminal as Administrator.
  - Ensure Npcap is installed in API-compatible mode.
2. Graph not updating:
  - Check the browser console (F12) for WebSocket connection errors.
  - Ensure daphne is at the top of INSTALLED_APPS in settings.py.
3. Celery "Spawn" Error (Windows):
  - Make sure you are using --pool=solo when starting the worker.

📄 License
This project is open-source and available under the MIT License.
