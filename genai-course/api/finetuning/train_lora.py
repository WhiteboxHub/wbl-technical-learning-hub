"""LoRA Fine-Tuning Script with HuggingFace PEFT (Module 5).
NOTE: This script is NOT run during class. It is provided for home study and experimentation.
Running on CPU takes several hours; run on a GPU instance (T4/A10G) if training.

To run via Docker override:
  docker compose -f docker-compose.yml -f docker-compose.finetune.yml run --rm finetuner
"""
import os
import sys
from pathlib import Path

# Note for students reading this script:
MODEL_NAME = "microsoft/phi-2"  # 2.7B parameters, small enough for single-GPU LoRA
DATASET_PATH = Path(__file__).resolve().parent.parent.parent / "data" / "finetune_dataset.jsonl"
OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "lora_adapter"

def main():
    print("=" * 60)
    print("LoRA Fine-Tuning Script — Module 5 Reference Code")
    print(f"Base Model:    {MODEL_NAME}")
    print(f"Dataset:       {DATASET_PATH}")
    print(f"Adapter Dest:  {OUTPUT_DIR}")
    print("=" * 60)

    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments
        from peft import LoraConfig, get_peft_model
        from datasets import load_dataset
    except ImportError:
        print("\nNotice: Fine-tuning packages (torch, transformers, peft) are optional.")
        print("To install dependencies for home training:")
        print("  pip install torch transformers peft datasets accelerate trl\n")
        print("In class, this script is walked through conceptually (see Module 5 Beat 5.5).")
        return

    print("Checking CUDA availability...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Training device: {device.upper()}")
    if device == "cpu":
        print("WARNING: Training on CPU will be extremely slow. A GPU is strongly recommended.")

    print(f"\n[1/4] Loading tokenizer for {MODEL_NAME}...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token

    print("\n[2/4] Defining LoRA Configuration...")
    lora_config = LoraConfig(
        r=8,                           # Rank: bottleneck dimension (8 is typical for LoRA)
        lora_alpha=32,                 # Scaling factor (alpha / r = 4x)
        target_modules=["Wqkv", "out_proj"], # Attention projection weights to adapt
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    print(f"  Rank (r): {lora_config.r}")
    print(f"  Alpha:    {lora_config.lora_alpha}")
    print(f"  Target:   {lora_config.target_modules}")

    print("\n[3/4] Loading base model (frozen weights)...")
    base_model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
        trust_remote_code=True
    )
    model = get_peft_model(base_model, lora_config)
    model.print_trainable_parameters()

    print("\n[4/4] Dataset ready. Run SFTTrainer to train.")
    print("In class, we discuss why LoRA trains only ~0.1% of parameters vs full fine-tuning.")
    print("Done reference check.")

if __name__ == "__main__":
    main()
