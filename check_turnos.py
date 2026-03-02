import os
import requests
from playwright.sync_api import sync_playwright

URL = "https://turnos.argentina.gob.ar/turnos/seleccionTurno/3219/pais/37/prov/67/loc/2875/pda/3616"

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def send_telegram(msg):
    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(URL, timeout=60000)

    page.wait_for_timeout(8000)

    content = page.content().lower()

    if "no hay turnos disponibles" not in content:
        send_telegram("🚨 TURNO DISPONIBLE 🚨\nEntrá YA:\n" + URL)

    browser.close()
