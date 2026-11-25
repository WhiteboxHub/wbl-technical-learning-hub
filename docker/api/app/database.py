from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

try:
    import redis
except ImportError:  # pragma: no cover
    redis = None  # type: ignore

DEFAULT_DB_PATH = Path(os.getenv("MANIFEST_DB_PATH", "/data/manifest.db"))
DEFAULT_REDIS_URL = os.getenv("REDIS_URL", "")
_redis_clients: dict[str, Any] = {}


def get_db_path() -> Path:
    return Path(os.getenv("MANIFEST_DB_PATH", str(DEFAULT_DB_PATH)))


def _ensure_db(db_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS containers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                container_code TEXT NOT NULL UNIQUE,
                cargo TEXT NOT NULL,
                origin_port TEXT NOT NULL,
                destination_port TEXT NOT NULL,
                weight_kg INTEGER NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        conn.commit()


@contextmanager
def get_db() -> Iterator[sqlite3.Connection]:
    """Yield a SQLite connection, ensuring the containers table exists."""
    db_path = get_db_path()
    _ensure_db(db_path)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def get_redis_client() -> Any:
    """Return a cached Redis client for the configured REDIS_URL, or None if disabled/invalid."""
    url = os.getenv("REDIS_URL", DEFAULT_REDIS_URL)
    if not url or redis is None:
        return None
    client = _redis_clients.get(url)
    if client is None:
        try:
            client = redis.Redis.from_url(url, decode_responses=True, socket_connect_timeout=1)
        except ValueError:
            return None
        _redis_clients[url] = client
    return client

