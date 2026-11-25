"""Tuesday Demo 2: Two-stage DVC pipeline reproduced incrementally (`dvc repro`).

Demonstrates how `dvc repro` skips unchanged upstream stages and only reruns
downstream stages when a parameter changes.
"""
import argparse
from pathlib import Path
import shutil
import subprocess
import tempfile


def _run(cmd: list[str], cwd: Path) -> str:
    res = subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return res.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--change-stage", choices=["train", "prepare", "none"], default="train",
                        help="Live variation: choose which stage config changes")
    args = parser.parse_args()

    print("\n=== TUESDAY DEMO 2: DVC PIPELINE INCREMENTAL REPRO ===")
    if shutil.which("dvc") is None:
        print("DVC CLI not installed in this Python env. Run inside Docker or install `dvc` via requirements.txt.")
        return

    with tempfile.TemporaryDirectory(prefix="dvc_demo2_") as tmp:
        root = Path(tmp)
        _run(["git", "init"], root)
        _run(["dvc", "init"], root)
        (root / "prep.py").write_text("import sys; Path = __import__('pathlib').Path; Path('clean.txt').write_text('rows=1000\\n')", encoding="utf-8")
        (root / "train.py").write_text("import sys; Path = __import__('pathlib').Path; Path('model.txt').write_text('C=' + sys.argv[1] + '\\n')", encoding="utf-8")
        (root / "params.yaml").write_text("prep_seed: 42\nC: 1.0\n", encoding="utf-8")
        (root / "dvc.yaml").write_text(
            "stages:\n"
            "  prepare:\n    cmd: python prep.py\n    deps: [prep.py]\n    params: [prep_seed]\n    outs: [clean.txt]\n"
            "  train:\n    cmd: python train.py ${C}\n    deps: [train.py, clean.txt]\n    params: [C]\n    outs: [model.txt]\n",
            encoding="utf-8",
        )
        print("--- First `dvc repro` (runs both stages) ---")
        print(_run(["dvc", "repro"], root))

        if args.change_stage == "train":
            (root / "params.yaml").write_text("prep_seed: 42\nC: 2.5\n", encoding="utf-8")
        elif args.change_stage == "prepare":
            (root / "params.yaml").write_text("prep_seed: 99\nC: 1.0\n", encoding="utf-8")

        print(f"--- Second `dvc repro` after changing `{args.change_stage}` ---")
        print(_run(["dvc", "repro"], root))
        print("LIVE VARIATION: run with `--change-stage prepare` vs `--change-stage none`.")


if __name__ == "__main__":
    main()
