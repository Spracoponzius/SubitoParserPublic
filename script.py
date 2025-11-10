import requests
from bs4 import BeautifulSoup
import time
import json
import os
import urllib.parse

# === CONFIGURAZIONE ===
SEARCH_TERMS = ["esempio1","esempio2"]  # termini di ricerca
SLEEP_TIME = 300  # secondi tra un controllo e l'altro (5 min)
SEEN_FILE = "seen.json"

# --- Telegram ---
TOKEN = "" #token del bot fornito da BotFather
CHAT_ID = "" #ID legato alla chat con l'utente


# === FUNZIONI ===
def send_telegram(msg):
    """Invia un messaggio Telegram al tuo chat_id"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": msg, "disable_web_page_preview": False}
    try:
        requests.post(url, params=params, timeout=10)
    except Exception as e:
        print(f"[!] Errore invio Telegram: {e}")


def load_seen():
    """Carica la lista di annunci già visti"""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, "r") as f:
            return set(json.load(f))
    return set()


def save_seen(seen):
    """Salva la lista di annunci già notificati"""
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


def fetch_ads(search_term):
    """Scarica gli annunci per una data parola chiave"""
    encoded = urllib.parse.quote_plus(search_term)
    url = f"https://www.subito.it/annunci-italia/vendita/usato/?q={encoded}"

    headers = {"User-Agent": "Mozilla/5.0"}
    html = requests.get(url, headers=headers, timeout=10).text
    soup = BeautifulSoup(html, "html.parser")

    ads = []
    # Selezione flessibile: link con aria-label (titolo) e href verso subito.it
    for a in soup.find_all("a", href=True, attrs={"aria-label": True}):
        href = a["href"]
        title = a["aria-label"]
        if "subito.it" in href and title:
            # Estrai ID numerico
            if href.endswith(".htm"):
                ad_id = href.split("-")[-1].split(".")[0]
            else:
                ad_id = href
            ads.append((ad_id, title, href))
    return ads


# === MAIN LOOP ===
def main():
    msg = "Inizio monitoraggio..."
    send_telegram(msg)
    seen = load_seen()
    print(f"[i] Inizio monitoraggio... Termini: {', '.join(SEARCH_TERMS)}")

# Ciclo while-true con sleep time poco elegante ma funziona e basta  
    while True:
        found_new = []
        for term in SEARCH_TERMS:
            ads = fetch_ads(term)
            for ad_id, title, link in ads:
                if ad_id not in seen:
                    seen.add(ad_id)
                    found_new.append((title, link))

        if found_new:
            for title, link in found_new:
                msg = f"\n• {title}\n{link}\n"
                send_telegram(msg)
                print(msg)
                
            save_seen(seen)

        else:
            print("[·] Nessun nuovo annuncio trovato.")
        time.sleep(SLEEP_TIME)


if __name__ == "__main__":
    main()
