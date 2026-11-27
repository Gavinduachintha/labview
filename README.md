<div align="center">

# 🖥️ LabView

### A tiny status window into your homelab.

**Monitor your server at a glance — right from the built-in display of a UNIHIKER K10.**

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/API-Flask-000000?style=flat-square&logo=flask&logoColor=white)
![Hardware](https://img.shields.io/badge/Device-DFRobot%20UNIHIKER%20K10-4C9A2A?style=flat-square)
![Platform](https://img.shields.io/badge/Server-Ubuntu%20%2F%20Linux-E95420?style=flat-square&logo=ubuntu&logoColor=white)

</div>

---

## ✨ What is LabView?

LabView is a lightweight **homelab monitoring project**. A small Python web server runs on your Ubuntu/Linux homelab machine, collects system health metrics, and makes them available as JSON. An **ESP32-powered DFRobot UNIHIKER K10** can request that data and present the latest stats on its built-in screen.

> This repository contains the server-side monitoring API. The UNIHIKER K10 display client/firmware is a separate component and is not included here.

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
│  Flask API + psutil metrics │                         │  Fetches and shows stats    │
└─────────────────────────────┘                         └─────────────────────────────┘
```

The server exposes a `/status` endpoint. The device connects over your network, requests the endpoint, then uses the returned values to refresh its display.

## 🧰 Tech stack

- **Python 3** — monitoring service and metric collectors
- **Flask** — lightweight HTTP API
- **psutil** — CPU, memory, and disk statistics
- **HTTP + JSON** — data exchange between the server and device
- **Ubuntu/Linux** — target homelab server
- **ESP32 / DFRobot UNIHIKER K10** — client device and built-in display (firmware maintained separately)

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

The API listens on port **5000** and binds to `0.0.0.0`, making it reachable from other devices on your local network.

### 4. Check the endpoints

From the server, or another machine on the same network, try:

```bash
curl http://<SERVER-IP>:5000/
curl http://<SERVER-IP>:5000/status
```

Replace `<SERVER-IP>` with the homelab machine's local IP address. The status endpoint returns JSON in this shape:

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

Values above are illustrative. RAM and disk sizes are reported in bytes; CPU frequency is reported in MHz when available. The root endpoint (`/`) returns basic service information.

### 5. Connect the UNIHIKER K10

Configure the device-side client to join a network that can reach the server, request `http://<SERVER-IP>:5000/status`, and render the returned CPU, RAM, and disk values on the built-in display. The client firmware is not part of this repository.

## 🎨 The vibe

A calm, glanceable homelab companion: keep the server details on the machine, and bring just the essentials to a compact desk-side display. No dashboard tab required.

## 🔐 Network note

The API currently has no authentication and listens on all network interfaces. Keep it on a trusted private network; do not expose port 5000 directly to the public internet. If you use a firewall, allow the device to reach TCP port 5000 on the server.
