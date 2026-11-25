import json
import logging
import os
import sqlite3
import time
import redis

DATABASE_URL = os.getenv("DATABASE_URL", "/tmp/urlshortener.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "10"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] [Worker] %(message)s")
logger = logging.getLogger("queue-worker")

def init_db():
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS short_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code VARCHAR(32) UNIQUE,
            original_url VARCHAR(2048),
            created_at TIMESTAMP,
            clicks INTEGER DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code VARCHAR(32),
            accessed_at TIMESTAMP,
            client_ip VARCHAR(64),
            user_agent VARCHAR(512)
        )
    """)
    conn.commit()
    conn.close()

def main():
    logger.info("Starting Queue Worker (The Depot)...")
    init_db()

    r = None
    while not r:
        try:
            r = redis.Redis.from_url(REDIS_URL, decode_responses=True)
            r.ping()
            logger.info("Connected to Redis successfully.")
        except Exception as e:
            logger.warning("Waiting for Redis: %s", e)
            time.sleep(2)

    while True:
        try:
            # 1. Process asynchronous Shorten Queue (order buffering)
            raw_task = r.lpop("shorten:queue")
            if raw_task:
                task = json.loads(raw_task)
                code = task["short_code"]
                url = task["original_url"]
                conn = sqlite3.connect(DATABASE_URL)
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR IGNORE INTO short_urls (short_code, original_url, created_at, clicks) VALUES (?, ?, datetime('now'), 0)",
                    (code, url)
                )
                conn.commit()
                conn.close()
                logger.info("Processed async shorten task: %s -> %s", code, url)

            # 2. Process asynchronous Analytics Queue (click batching)
            raw_event = r.lpop("analytics:queue")
            if raw_event:
                event = json.loads(raw_event)
                code = event["short_code"]
                ip = event.get("client_ip", "unknown")
                conn = sqlite3.connect(DATABASE_URL)
                cursor = conn.cursor()
                cursor.execute("UPDATE short_urls SET clicks = clicks + 1 WHERE short_code = ?", (code,))
                cursor.execute("INSERT INTO access_logs (short_code, accessed_at, client_ip) VALUES (?, datetime('now'), ?)", (code, ip))
                conn.commit()
                conn.close()
                logger.info("Processed click analytics event for code: %s", code)

            if not raw_task and not raw_event:
                time.sleep(0.5)

        except Exception as e:
            logger.error("Error in worker loop: %s", e)
            time.sleep(1)

if __name__ == "__main__":
    main()
