import hashlib
import json
import os
import random
import string
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, SessionLocal, engine, get_db

INSTANCE_ID = os.getenv("HOSTNAME", "standalone-instance")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
NO_CACHE = os.getenv("NO_CACHE", "0") == "1"
SIMULATE_DB_DELAY = float(os.getenv("SIMULATE_DB_DELAY", "0.0"))
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", "60"))

_redis_client = None

def get_redis():
    global _redis_client
    if NO_CACHE:
        return None
    if _redis_client is None:
        try:
            import redis
            _redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True, socket_connect_timeout=0.5, socket_timeout=0.5)
            _redis_client.ping()
        except Exception:
            _redis_client = None
    return _redis_client

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    # Pre-seed sample URLs if empty
    with SessionLocal() as db:
        if db.query(models.ShortURL).count() == 0:
            sample_urls = [
                ("wbl", "https://whiteboxlearning.com"),
                ("docs", "https://docs.python.org/3/"),
                ("cloud", "https://aws.amazon.com/architecture/"),
            ]
            for code, target in sample_urls:
                db.add(models.ShortURL(short_code=code, original_url=target))
            db.commit()
    yield

app = FastAPI(
    title="Growing City URL Shortener - System Design Demo Service",
    description="A stateless URL shortener designed to demonstrate system scaling, load balancing, caching, queues, and database bottlenecks.",
    version="1.0.0",
    lifespan=lifespan
)

def generate_short_code(url: str, length: int = 6) -> str:
    hash_object = hashlib.md5(f"{url}-{time.time()}-{random.random()}".encode())
    return hash_object.hexdigest()[:length]

@app.get("/health")
def health_check():
    """Liveness probe returning instance identifier to prove load balancing across replicas."""
    r = get_redis()
    cache_alive = False
    if r:
        try:
            r.ping()
            cache_alive = True
        except Exception:
            pass

    return {
        "status": "healthy",
        "instance_id": INSTANCE_ID,
        "cache_enabled": not NO_CACHE,
        "cache_connected": cache_alive,
        "db_delay_seconds": SIMULATE_DB_DELAY
    }

@app.post("/api/shorten", response_model=schemas.ShortenResponse, status_code=201)
def create_short_url(
    payload: schemas.ShortenRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Creates a shortened URL.
    Demonstrates:
    - Synchronous DB write (default)
    - Asynchronous write queueing (when payload.async_queue is True or QUEUE_WRITES=1)
    """
    code = payload.custom_code.strip() if payload.custom_code else generate_short_code(payload.url)
    
    # Check if async write queue is requested (The Depot in The Growing City)
    queue_mode = payload.async_queue or os.getenv("QUEUE_WRITES", "0") == "1"
    r = get_redis()

    if queue_mode and r:
        task = {
            "short_code": code,
            "original_url": payload.url,
            "timestamp": time.time()
        }
        r.rpush("shorten:queue", json.dumps(task))
        # Warm the cache optimistically so reads work right away
        r.setex(f"url:{code}", CACHE_TTL_SECONDS, payload.url)
        response.status_code = 202
        return schemas.ShortenResponse(
            short_code=code,
            short_url=f"/r/{code}",
            original_url=payload.url,
            created_at=models.datetime.datetime.utcnow(),
            queued=True
        )

    # Synchronous DB write (simulating bottleneck when traffic surges)
    if SIMULATE_DB_DELAY > 0:
        time.sleep(SIMULATE_DB_DELAY)

    existing = db.query(models.ShortURL).filter(models.ShortURL.short_code == code).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Short code '{code}' already exists")

    entry = models.ShortURL(short_code=code, original_url=payload.url)
    db.add(entry)
    db.commit()
    db.refresh(entry)

    # Cache-aside: write to cache (The Corner Shop)
    if r:
        try:
            r.setex(f"url:{code}", CACHE_TTL_SECONDS, payload.url)
        except Exception:
            pass

    return schemas.ShortenResponse(
        short_code=entry.short_code,
        short_url=f"/r/{entry.short_code}",
        original_url=entry.original_url,
        created_at=entry.created_at,
        queued=False
    )

@app.get("/r/{short_code}")
def redirect_to_url(
    short_code: str,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Critical Read Path: Resolves short code and redirects.
    Demonstrates:
    - Cache-Aside pattern (checks Redis first; hits DB on miss)
    - Staleness and Cache Invalidation
    - Asynchronous click event ingestion via Redis Queue
    """
    start_time = time.time()
    r = get_redis()
    cache_hit = False
    target_url = None

    # Step 1: Check Cache (The Corner Shop)
    if r:
        try:
            cached = r.get(f"url:{short_code}")
            if cached:
                target_url = cached
                cache_hit = True
                r.incr("metrics:cache_hits")
        except Exception:
            pass

    # Step 2: Cache Miss -> Fallback to Database (The Central Warehouse)
    if not target_url:
        if r:
            r.incr("metrics:cache_misses")
        if SIMULATE_DB_DELAY > 0:
            time.sleep(SIMULATE_DB_DELAY)

        record = db.query(models.ShortURL).filter(models.ShortURL.short_code == short_code).first()
        if not record:
            raise HTTPException(status_code=404, detail=f"Short code '{short_code}' not found")
        target_url = record.original_url

        # Populate Cache with TTL
        if r:
            try:
                r.setex(f"url:{short_code}", CACHE_TTL_SECONDS, target_url)
            except Exception:
                pass

    # Step 3: Asynchronously log click event via queue (so logging doesn't slow down redirect)
    if r:
        try:
            event = {
                "short_code": short_code,
                "client_ip": request.client.host if request.client else "unknown",
                "timestamp": time.time()
            }
            r.rpush("analytics:queue", json.dumps(event))
        except Exception:
            pass

    elapsed_ms = (time.time() - start_time) * 1000
    headers = {
        "X-Instance-Id": INSTANCE_ID,
        "X-Cache": "HIT" if cache_hit else "MISS",
        "X-Response-Time-Ms": f"{elapsed_ms:.2f}"
    }

    return RedirectResponse(url=target_url, status_code=302, headers=headers)

@app.get("/api/stats/{short_code}", response_model=schemas.URLStats)
def get_url_stats(
    short_code: str,
    db: Session = Depends(get_db)
):
    """Retrieves access statistics and cache presence."""
    if SIMULATE_DB_DELAY > 0:
        time.sleep(SIMULATE_DB_DELAY)

    record = db.query(models.ShortURL).filter(models.ShortURL.short_code == short_code).first()
    if not record:
        raise HTTPException(status_code=404, detail=f"Short code '{short_code}' not found")

    r = get_redis()
    is_cached = False
    if r:
        try:
            is_cached = bool(r.exists(f"url:{short_code}"))
        except Exception:
            pass

    return schemas.URLStats(
        short_code=record.short_code,
        original_url=record.original_url,
        clicks=record.clicks,
        created_at=record.created_at,
        cached=is_cached
    )

@app.post("/api/cache/flush")
def flush_cache():
    """Flushes Redis cache to demonstrate cache invalidation and thundering herd / cache stampede."""
    r = get_redis()
    if not r:
        return {"status": "cache_disabled_or_unavailable"}
    r.flushdb()
    return {"status": "cache_flushed", "message": "All cached items purged. Next reads will hit the database directly."}

@app.get("/api/metrics")
def get_metrics():
    """System-wide telemetry: cache hit ratio, queue lengths, instance info."""
    r = get_redis()
    metrics = {
        "instance_id": INSTANCE_ID,
        "cache_hits": 0,
        "cache_misses": 0,
        "hit_ratio_percent": 0.0,
        "analytics_queue_length": 0,
        "shorten_queue_length": 0
    }
    if r:
        try:
            hits = int(r.get("metrics:cache_hits") or 0)
            misses = int(r.get("metrics:cache_misses") or 0)
            total = hits + misses
            metrics["cache_hits"] = hits
            metrics["cache_misses"] = misses
            metrics["hit_ratio_percent"] = round((hits / total * 100), 1) if total > 0 else 0.0
            metrics["analytics_queue_length"] = r.llen("analytics:queue")
            metrics["shorten_queue_length"] = r.llen("shorten:queue")
        except Exception:
            pass
    return metrics
