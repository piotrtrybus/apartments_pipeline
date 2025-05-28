FROM python:3.11-slim

WORKDIR /prague_apartments_pipeline

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .

CMD ["python", "orchestration.py"]
