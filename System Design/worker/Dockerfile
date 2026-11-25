FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir redis
COPY worker.py .
ENV PYTHONUNBUFFERED=1
CMD ["python", "worker.py"]
