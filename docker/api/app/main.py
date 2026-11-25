from __future__ import annotations

import logging
import os
import sqlite3
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException, Response, status

from .database import get_db, get_db_path, get_redis_client
from .schemas import ContainerCreate, ContainerRecord, ContainerStatus, ContainerUpdate

logger = logging.getLogger(__name__)
PORT_NAME = os.getenv("PORT_NAME", "Port of Rotterdam")
_UPDATABLE_COLUMNS = frozenset({"cargo", "destination_port", "weight_kg", "status"})


def _row_to_record(row: sqlite3.Row) -> ContainerRecord:
    return ContainerRecord(
        id=row["id"],
        container_code=row["container_code"],
        cargo=row["cargo"],
        origin_port=row["origin_port"],
        destination_port=row["destination_port"],
        weight_kg=row["weight_kg"],
        status=row["status"],
        created_at=row["created_at"],
    )


app = FastAPI(
    title="The Shipping Container — Cargo Manifest API",
    description="Python FastAPI service used to practice Docker images, Dockerfiles, volumes, and networking.",
    version="1.0.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    redis_status = "disabled"
    client = get_redis_client()
    if client is not None:
        try:
            client.ping()
            redis_status = "connected"
        except Exception:
            redis_status = "unreachable"
    return {
        "status": "ok",
        "port": os.getenv("PORT_NAME", PORT_NAME),
        "db_path": str(get_db_path()),
        "redis": redis_status,
    }


@app.get("/containers", response_model=list[ContainerRecord])
def list_containers(status_filter: ContainerStatus | None = None) -> list[ContainerRecord]:
    client = get_redis_client()
    if client is not None:
        try:
            client.incr("manifest:list_hits")
        except Exception as exc:
            logger.warning("Failed to increment Redis list_hits: %s", exc)

    with get_db() as conn:
        if status_filter:
            rows = conn.execute(
                "SELECT * FROM containers WHERE status = ? ORDER BY id DESC",
                (status_filter,),
            ).fetchall()
        else:
            rows = conn.execute("SELECT * FROM containers ORDER BY id DESC").fetchall()
    return [_row_to_record(row) for row in rows]


@app.post("/containers", response_model=ContainerRecord, status_code=status.HTTP_201_CREATED)
def create_container(payload: ContainerCreate) -> ContainerRecord:
    created_at = datetime.now(timezone.utc).isoformat()
    with get_db() as conn:
        try:
            cursor = conn.execute(
                """
                INSERT INTO containers (
                    container_code, cargo, origin_port, destination_port, weight_kg, status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload.container_code.upper(),
                    payload.cargo,
                    payload.origin_port,
                    payload.destination_port,
                    payload.weight_kg,
                    payload.status,
                    created_at,
                ),
            )
            conn.commit()
        except sqlite3.IntegrityError as exc:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Container code '{payload.container_code.upper()}' already exists.",
            ) from exc

        row = conn.execute(
            "SELECT * FROM containers WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    assert row is not None
    return _row_to_record(row)


@app.get("/containers/{container_id}", response_model=ContainerRecord)
def get_container(container_id: int) -> ContainerRecord:
    with get_db() as conn:
        row = conn.execute("SELECT * FROM containers WHERE id = ?", (container_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Container not found")
    return _row_to_record(row)


@app.patch("/containers/{container_id}", response_model=ContainerRecord)
def update_container(container_id: int, payload: ContainerUpdate) -> ContainerRecord:
    updates = {
        k: v
        for k, v in payload.model_dump(exclude_unset=True, exclude_none=True).items()
        if k in _UPDATABLE_COLUMNS
    }
    if not updates:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Provide at least one non-null field to update.",
        )

    with get_db() as conn:
        existing = conn.execute("SELECT * FROM containers WHERE id = ?", (container_id,)).fetchone()
        if existing is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Container not found")

        assignments = ", ".join(f"{col} = ?" for col in updates)
        values = list(updates.values()) + [container_id]
        conn.execute(f"UPDATE containers SET {assignments} WHERE id = ?", values)
        conn.commit()
        row = conn.execute("SELECT * FROM containers WHERE id = ?", (container_id,)).fetchone()
    assert row is not None
    return _row_to_record(row)


@app.delete("/containers/{container_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_container(container_id: int) -> Response:
    with get_db() as conn:
        cursor = conn.execute("DELETE FROM containers WHERE id = ?", (container_id,))
        conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Container not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/stats")
def stats() -> dict[str, int]:
    with get_db() as conn:
        total = conn.execute("SELECT COUNT(*) AS c FROM containers").fetchone()["c"]
        total_weight = conn.execute(
            "SELECT COALESCE(SUM(weight_kg), 0) AS w FROM containers"
        ).fetchone()["w"]

    list_hits = 0
    client = get_redis_client()
    if client is not None:
        try:
            raw = client.get("manifest:list_hits")
            list_hits = int(raw) if raw else 0
        except Exception as exc:
            logger.warning("Failed to read Redis list_hits: %s", exc)
            list_hits = 0

    return {
        "total_containers": total,
        "total_weight_kg": total_weight,
        "list_endpoint_hits": list_hits,
    }
