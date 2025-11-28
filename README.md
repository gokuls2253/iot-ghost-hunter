# 👻 IoT Ghost Hunter

> **Enterprise-Grade Network Operations (NetOps) Console**
> *Real-time Network Monitoring, Anomaly Detection, and Threat Intelligence System.*

![Project Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge&logo=statuspage)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-Broker-DC382D?style=for-the-badge&logo=redis&logoColor=white)

## 📖 Overview
**IoT Ghost Hunter** is a sophisticated, event-driven network analysis tool designed to visualize local network traffic and detect security threats in real-time.

Unlike traditional scanners, this system uses an asynchronous architecture to perform **Passive Packet Sniffing** and **Active ARP Discovery** simultaneously without blocking the user interface. It integrates Machine Learning for anomaly detection and external Threat Intelligence APIs to flag connections to malicious global endpoints.

---

## ✨ Key Features

### 🛡️ Core Security
* **Real-Time Discovery:** Instantly identifies devices (IP, MAC, Vendor) entering the network using ARP broadcasting.
* **🧠 Anomaly Detection:** Uses **Scikit-Learn (Isolation Forest)** to learn baseline network behavior and alert on suspicious device spikes.
* **⛔ Threat Intelligence:** Integrates with **VirusTotal API** to check destination IPs against a global malware database.

### 🗺️ Visualization & Ops
* **🌍 Geo-Location Mapping:** traces outgoing traffic and visualizes destination servers on an interactive **Leaflet.js World Map**.
* **🏭 Vendor Fingerprinting:** Automatically resolves MAC addresses to manufacturers (e.g., "Apple, Inc.", "Espressif") using `mac-vendor-lookup`.
* **⚡ Live Streams:** Uses **WebSockets (Django Channels)** to push alerts and graph updates instantly—no page refreshes required.

---

## 🏗️ Architecture

The system follows a distributed, microservices-style architecture:

1.  **Sensing Layer (Scapy):** A background worker captures raw packets and performs active scanning.
2.  **Processing Layer (Celery):** Handles heavy lifting (ML prediction, API queries) asynchronously.
3.  **Message Bus (Redis):** Acts as the high-speed bridge between the scanner and the web server.
4.  **Presentation Layer (Django + Channels):** Serves the UI and manages WebSocket connections.

---

## 🛠️ Technical Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Backend** | Python, Django | Core application logic and REST API. |
| **Network Engine** | Scapy | Packet sniffing and ARP injection. |
| **Async Tasks** | Celery | Distributed task queue management. |
| **Broker** | Redis | In-memory data structure store. |
| **Real-Time** | Django Channels (Daphne) | ASGI WebSocket handling. |
| **ML Engine** | Scikit-Learn | Unsupervised Anomaly Detection. |
| **External APIs** | VirusTotal, IP-API | Threat intelligence and Geo-coding. |
| **Frontend** | Bootstrap 5, Chart.js, Leaflet | "Command Center" UI. |

---

## 🚀 Setup & Installation

### Prerequisites
* **Python 3.10+**
* **Redis Server** (Running locally or via Docker)
* **PostgreSQL**
* **Windows Users:** Must install [Npcap](https://npcap.com/) (Check "Install in WinPcap API-compatible Mode").

### 1. Clone the Repository
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

# Install Dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a .env file in the root directory:
```
# .env
DEBUG=True
SECRET_KEY=your_secret_key
# Database (Simple Setup)
DB_NAME=ghost_hunter
DB_USER=postgres
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
# Redis (Defaults are usually fine for local)
REDIS_HOST=localhost
REDIS_PORT=6379
#Threat Intelligence (VirusTotal API Key)
VT_API_KEY=your_api_key
```

### 4. Database Initialization
Create the database in Postgres first, then run:
```
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
Terminal 3: Django Web Server (The Hoster)
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
Simulating a Threat
To see the Red Alert UI without actual malware:
1. Open network/threat_engine.py.
2. Uncomment the simulation line: return True, 99 inside check_ip().
3. Restart the Celery Worker.
4. Trigger a scan.

## ⚠️ Troubleshooting

- "Permission Denied" (Scapy): Ensure you are running the terminal as Administrator/Root. Raw packet capture requires elevated privileges.
- Map not showing points: Ensure you have generated traffic (opened browser tabs) while the scanner is running so the passive sniffer captures packets.
- Redis Connection Error: Ensure the Redis service is running (redis-server or via Docker).

## 📄 License

This project is open-source and available under the MIT License.
