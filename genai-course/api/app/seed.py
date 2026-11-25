"""Seed the vector store with HR policy documents on first startup."""
import os
from pathlib import Path


def _data_dir() -> Path:
    container_path = Path("/app/data/hr_documents")
    if container_path.exists():
        return container_path
    local_path = Path(__file__).resolve().parent.parent.parent / "data" / "hr_documents"
    return local_path


DOCUMENT_IDS = {
    "employee-handbook.md": "employee-handbook",
    "pto-and-leave-policy.md": "pto-and-leave-policy",
    "benefits-and-healthcare.md": "benefits-and-healthcare",
    "remote-work-policy.md": "remote-work-policy",
    "it-security-guidelines.md": "it-security-guidelines",
}


def seed_if_empty() -> None:
    if os.getenv("TESTING") == "1":
        return

    from .vector_store import get_collection, add_chunks
    from .chunker import chunk
    from .embeddings import embed

    try:
        col = get_collection()
        if col.count() > 0:
            print("Seed: ChromaDB already populated, skipping.")
            return
    except Exception as exc:
        print(f"Seed: ChromaDB not reachable at startup ({exc}), skipping auto-seed.")
        return

    print("Seed: Seeding HR policy documents into ChromaDB...")
    chunk_size = int(os.getenv("CHUNK_SIZE", 512))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", 64))

    try:
        for filename, doc_id in DOCUMENT_IDS.items():
            filepath = _data_dir() / filename
            if not filepath.exists():
                print(f"Seed: WARNING — {filepath} not found, skipping.")
                continue
            text = filepath.read_text(encoding="utf-8")
            chunks = chunk(text, "recursive", chunk_size, chunk_overlap)
            if not chunks:
                continue
            texts = [c["text"] for c in chunks]
            vecs = embed(texts)
            meta = {"document_id": doc_id, "source_file": filename}
            add_chunks(doc_id, chunks, vecs, meta)
            print(f"Seed: {doc_id} → {len(chunks)} chunks stored.")
        print("Seed: Done.")
    except Exception as exc:
        print(f"Seed: Could not generate embeddings or seed ChromaDB ({exc}). Application will start without pre-seeded documents.")
