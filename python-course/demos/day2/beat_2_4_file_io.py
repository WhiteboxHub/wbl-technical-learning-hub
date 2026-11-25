"""Day 2, Beat 2.4: Kitchen Logbook (File I/O with text & JSON)."""

import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
CONFIG_PATH = DATA_DIR / "model_config.json"
DOCS_PATH = DATA_DIR / "prompt_docs.txt"
LOG_PATH = DATA_DIR / "run_log.txt"
UPDATED_CONFIG_PATH = DATA_DIR / "updated_config.json"

print("=== Beat 2.4: Kitchen Logbook (File I/O) ===")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

with open(DOCS_PATH, "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

print(f"Loaded model config  : {config['model']} (temp={config['temperature']}, max_tokens={config['max_tokens']})")
print(f"Loaded document lines: {len(lines)}")

with open(LOG_PATH, "a", encoding="utf-8") as f:
    f.write(f"Loaded {len(lines)} docs for model={config['model']}\n")

config["last_doc_count"] = len(lines)
with open(UPDATED_CONFIG_PATH, "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)

print("Appended run entry to demos/day2/data/run_log.txt")
print("Saved updated config to demos/day2/data/updated_config.json")

