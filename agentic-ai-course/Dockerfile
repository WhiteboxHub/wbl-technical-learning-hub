FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application and web assets
COPY claimflow/ /app/claimflow/
COPY web/ /app/web/
COPY course/ /app/course/
COPY docs/ /app/docs/
COPY tests/ /app/tests/
COPY examples/ /app/examples/

EXPOSE 8000

ENV PYTHONPATH=/app
ENV CLAIMFLOW_LLM_PROVIDER=mock

CMD ["python", "-m", "uvicorn", "claimflow.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
