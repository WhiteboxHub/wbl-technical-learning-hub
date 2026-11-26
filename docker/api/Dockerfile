FROM python:3.12-slim

# Prevent Python from buffering stdout/stderr (critical for `docker logs`)
# and from writing .pyc files inside the container.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/srv \
    MANIFEST_DB_PATH=/data/manifest.db

WORKDIR /srv

# 1. Copy only dependency manifest first to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Copy application code and tests
COPY app ./app
COPY tests ./tests

# 3. Create non-root user and data directory for volume mounts
RUN useradd --create-home --shell /bin/bash harbor \
    && mkdir -p /data \
    && chown -R harbor:harbor /srv /data

USER harbor

EXPOSE 8000

HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
