FROM python:3.12-slim
WORKDIR /srv
RUN pip install --no-cache-dir "fastapi>=0.115" "uvicorn[standard]>=0.30" "python-multipart>=0.0.9"
COPY app.py .
EXPOSE 3003
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3003"]
