FROM python:3.11-slim

WORKDIR /srv

RUN apt-get update && apt-get install -y --no-install-recommends curl git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY fraud_system ./fraud_system
COPY demos ./demos
COPY web ./web
COPY tests ./tests
COPY params.yaml dvc.yaml pyproject.toml ./

EXPOSE 8000 5000

CMD ["uvicorn", "fraud_system.serve:app", "--host", "0.0.0.0", "--port", "8000"]
