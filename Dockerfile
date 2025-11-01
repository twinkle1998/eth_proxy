# =========================================================
# Dockerfile — FastAPI CoinGecko Proxy Cache (for Streamlit)
# Author: Twinkle
# =========================================================

# ---------- Base Image ----------
FROM python:3.11-slim

# ---------- Working Directory ----------
WORKDIR /app

# ---------- Install Dependencies ----------
# Copy requirement file first (for Docker layer caching)
COPY requirements.txt .

# Install pip dependencies without cache to reduce size
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Copy Project Files ----------
COPY coingecko_proxy.py .

# ---------- Expose Port ----------
EXPOSE 10000

# ---------- Environment Variables ----------
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# ---------- Start Server ----------
CMD ["uvicorn", "coingecko_proxy:app", "--host", "0.0.0.0", "--port", "10000"]
