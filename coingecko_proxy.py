# ================================================
# FastAPI — CoinGecko Proxy Cache for ETH Dashboard
# ================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, time

app = FastAPI()
CACHE = {}
TTL = 600  # cache for 10 minutes

# --- CORS: allow Streamlit frontend ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or restrict to your Streamlit domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Cached fetch helper ---
def fetch_cached(url):
    now = time.time()
    if url in CACHE and now - CACHE[url]["t"] < TTL:
        return CACHE[url]["data"]
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        data = r.json()
        CACHE[url] = {"data": data, "t": now}
        return data
    except Exception as e:
        return {"error": str(e)}

# --- Proxy routes ---
@app.get("/proxy/metadata")
def metadata():
    url = "https://api.coingecko.com/api/v3/coins/ethereum"
    return fetch_cached(url)

@app.get("/proxy/live_market")
def live_market():
    url = ("https://api.coingecko.com/api/v3/simple/price"
           "?ids=ethereum&vs_currencies=usd&include_market_cap=true"
           "&include_24hr_vol=true&include_24hr_change=true")
    return fetch_cached(url)

@app.get("/proxy/ohlc")
def ohlc(days: int = 90):
    url = f"https://api.coingecko.com/api/v3/coins/ethereum/ohlc?vs_currency=usd&days={days}"
    return fetch_cached(url)

@app.get("/proxy/market_chart")
def market_chart(days: int = 90):
    url = f"https://api.coingecko.com/api/v3/coins/ethereum/market_chart?vs_currency=usd&days={days}"
    return fetch_cached(url)

@app.get("/")
def health():
    return {"status": "ok", "service": "ETH Proxy"}
