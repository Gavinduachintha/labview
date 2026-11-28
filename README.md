<div align="center">

# 🖥️ LabView

### A tiny status window into your homelab.

**A live, glanceable view of your homelab — in your browser or on a UNIHIKER K10.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20API-000000?style=flat-square&logo=flask&logoColor=white)
![psutil](https://img.shields.io/badge/psutil-Metrics-3776AB?style=flat-square)
![Device](https://img.shields.io/badge/Device-UNIHIKER%20K10-4C9A2A?style=flat-square)
![Platform](https://img.shields.io/badge/Server-Ubuntu%20%2F%20Linux-E95420?style=flat-square&logo=ubuntu&logoColor=white)

</div>

---

## ✨ What is LabView?

LabView is a lightweight **homelab monitoring project**. A Python web server runs on your Ubuntu/Linux machine, collects system health metrics, and presents them in a responsive browser dashboard. The included `k10.py` client can also request the same JSON data and show it on an **ESP32-powered DFRobot UNIHIKER K10**.

## 🔎 What it monitors

The API currently reports:

| Metric | Data provided |
| --- | --- |
| **CPU** | Usage percentage and current frequency |
| **Memory (RAM)** | Total, used, and free memory in bytes, plus usage percentage |
| **Disk** | Total, used, and free space in bytes, plus usage percentage |

### How the pieces fit together

```text
┌─────────────────────────────┐       HTTP / JSON       ┌─────────────────────────────┐
│   Ubuntu / Linux homelab     │  ───────────────────▶  │  DFRobot UNIHIKER K10       │
│                             │      GET /status       │  ESP32 + built-in display   │
│  Flask dashboard + API      │                         │  k10.py display client      │
│  psutil metrics             │                         │  Fetches and shows stats    │
└─────────────────────────────┘                         └─────────────────────────────┘
```

The browser dashboard and device both use the `/status` endpoint. The dashboard refreshes automatically, and the device polls the same endpoint to refresh its display.

## 🧰 Tech stack

- **Python 3** — monitoring service and metric collectors
- **Flask** — web dashboard and lightweight HTTP API
- **psutil** — CPU, memory, and disk statistics
- **HTTP + JSON** — data exchange between the server and device
- **Ubuntu/Linux** — target homelab server
- **MicroPython / DFRobot UNIHIKER K10** — device-side display client (`k10.py`)

All technology badges above are generated with [Shields.io](https://img.shields.io).

## 🚀 Getting started

### Requirements

- Python 3 on the Ubuntu/Linux machine you want to monitor
- Network access from the UNIHIKER K10 to that machine

### 1. Get the project

```bash
git clone https://github.com/Gavinduachintha/labview.git
cd labview
```

### 2. Create an environment and install dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install Flask psutil
```

### 3. Start the monitoring API

```bash
python main.py
```

The dashboard and API listen on port **5000** and bind to `0.0.0.0`, making them reachable from other devices on your local network. Open `http://<SERVER-IP>:5000/` in a browser to view the dashboard.

### 4. Check the endpoints

From the server, or another machine on the same network, try:

```bash
curl http://<SERVER-IP>:5000/
curl http://<SERVER-IP>:5000/api
curl http://<SERVER-IP>:5000/status
```

Replace `<SERVER-IP>` with the homelab machine's local IP address. `/` serves the live dashboard, `/api` returns service information, and `/status` returns JSON in this shape:

```json
{
  "cpu": {
    "usage": 12.5,
    "frequency": 2400.0
  },
  "ram": {
    "total": 16777216000,
    "used": 8388608000,
    "free": 8388608000,
    "percent": 50.0
  },
  "disk": {
    "total": 1000204886016,
    "used": 400081954406,
    "free": 600122932610,
    "percent": 40.0
  }
}
```

Values above are illustrative. RAM and disk sizes are reported in bytes; CPU frequency is reported in MHz when available.

### 5. Set up the UNIHIKER K10

Open `k10.py` in the UNIHIKER K10's MicroPython environment. Set `SSID`, `PASSWORD`, and `URL` near the top of the script. Use the server's **local network IP address** in `URL`, for example `http://192.168.1.20:5000/status`, then run the script on the device. Keep the server and device on networks that can reach each other.

## 🎨 The vibe

A calm, glanceable homelab companion: a dark, responsive dashboard for a quick browser check, plus a compact desk-side display for the essentials.

## 🔐 Network note

The API currently has no authentication and listens on all network interfaces. Keep it on a trusted private network; do not expose port 5000 directly to the public internet. If you use a firewall, allow the device to reach TCP port 5000 on the server.
