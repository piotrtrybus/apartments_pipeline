FROM python:3.11-slim

WORKDIR /prague_apartments_pipeline

COPY requirements.txt .

RUN apt-get update && apt-get install -y \
    wget \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libxshmfence1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libdrm2 \
    libgbm1 \
    libpango-1.0-0 \
    libx11-xcb1 \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN playwright install

COPY . .

CMD ["python", "orchestration.py"]
