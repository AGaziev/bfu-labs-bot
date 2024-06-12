FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    python3-venv \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv venv

RUN . venv/bin/activate & pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PATH="/app/venv/bin:$PATH"

CMD ["python", "app.py"]
