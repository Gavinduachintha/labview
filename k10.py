import network
import time
import gc
import urequests as requests
from unihiker_k10 import screen

# ---------- Config ----------
SSID = "YOUR_WIFI_SSID"
PASSWORD = "YOUR_WIFI_PASSWORD"
URL = "http://YOUR_SERVER_IP:5000/status"   # use the server's local network IP
REFRESH_S = 2

# ---------- Colours ----------
BG     = 0x0B0F14
CARD   = 0x151B23
TRACK  = 0x2A333F
WHITE  = 0xFFFFFF
GRAY   = 0x8A94A3
GREEN  = 0x2ECC71
AMBER  = 0xF5A623
RED    = 0xE74C3C
CYAN   = 0x38BDF8

# ---------- Layout (240 x 320 portrait) ----------
CARD_X, CARD_W, CARD_H = 6, 228, 82
CARD_Y = (36, 124, 212)
BAR_W = 200


def rect(x, y, w, h, color):
    screen.draw_rect(x=x, y=y, w=w, h=h, bcolor=color, fcolor=color)


def text(s, x, y, size, color):
    screen.draw_text(text=s, x=x, y=y, font_size=size, color=color)


def level_color(pct):
    if pct < 60:
        return GREEN
    if pct < 85:
        return AMBER
    return RED


def gb(b):
    return b / 1e9


def draw_header(online, note=""):
    rect(0, 0, 240, 30, CARD)
    text("SERVER STATUS", 8, 5, 20, WHITE)
    screen.draw_circle(x=222, y=15, r=6,
                       fcolor=GREEN if online else RED,
                       bcolor=GREEN if online else RED)


def draw_card(idx, label, pct, big, detail):
    y = CARD_Y[idx]
    col = level_color(pct)
    rect(CARD_X, y, CARD_W, CARD_H, CARD)
    text(label, 16, y + 6, 16, GRAY)
    text(big, 16, y + 26, 28, col)
    text(detail, 120, y + 32, 16, WHITE)
    # progress bar
    rect(16, y + 64, BAR_W, 10, TRACK)
    fill = int(BAR_W * max(0, min(pct, 100)) / 100)
    if fill > 0:
        rect(16, y + 64, fill, 10, col)


def draw_footer(msg, color=GRAY):
    rect(0, 298, 240, 22, BG)
    text(msg, 8, 301, 14, color)


def render(data, online, footer):
    rect(0, 0, 240, 320, BG)
    draw_header(online)

    cpu, ram, disk = data["cpu"], data["ram"], data["disk"]

    draw_card(0, "CPU", cpu["usage"],
              "{:.1f}%".format(cpu["usage"]),
              "{:.0f} MHz".format(cpu["frequency"]))

    draw_card(1, "RAM", ram["percent"],
              "{:.0f}%".format(ram["percent"]),
              "{:.1f}/{:.1f} GB".format(gb(ram["used"]), gb(ram["total"])))

    draw_card(2, "DISK", disk["percent"],
              "{:.0f}%".format(disk["percent"]),
              "{:.0f}/{:.0f} GB".format(gb(disk["used"]), gb(disk["total"])))

    draw_footer(footer, CYAN if online else RED)
    screen.show_draw()


def splash(msg, color=WHITE):
    rect(0, 0, 240, 320, BG)
    text(msg, 20, 150, 20, color)
    screen.show_draw()


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        splash("Connecting Wi-Fi...", AMBER)
        wlan.connect(SSID, PASSWORD)
        t = 15
        while not wlan.isconnected() and t > 0:
            time.sleep(1)
            t -= 1
    return wlan


def fetch():
    r = None
    try:
        r = requests.get(URL)
        return r.json()
    finally:
        if r:
            r.close()


# ---------- Main ----------
screen.init(dir=2)
wlan = connect_wifi()

if not wlan.isconnected():
    splash("Wi-Fi failed", RED)
else:
    last = None
    while True:
        try:
            if not wlan.isconnected():
                wlan.connect(SSID, PASSWORD)
                time.sleep(3)
            last = fetch()
            render(last, True, "IP " + wlan.ifconfig()[0])
        except Exception as e:
            if last:
                render(last, False, "Offline: " + str(e)[:22])
            else:
                splash("Server unreachable", RED)
        gc.collect()
        time.sleep(REFRESH_S)
