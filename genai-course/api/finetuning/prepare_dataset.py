"""Fine-tuning Dataset Preparation Script (Module 5).
Reads HR documents and creates prompt-completion pairs in JSONL format for instruction tuning.

Usage:
  python prepare_dataset.py
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "hr_documents"
OUTPUT_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "finetune_dataset.jsonl"

SEED_QA_PAIRS = [
    {
        "prompt": "What is the 401(k) company match at Meridian Solutions?",
        "completion": "Meridian Solutions matches 100% of employee 401(k) contributions up to 4% of eligible base salary with immediate vesting."
    },
    {
        "prompt": "How many days of paid time off do new employees receive?",
        "completion": "Employees with 0 to 2 years of service accrue 15 days (120 hours) of PTO per calendar year."
    },
    {
        "prompt": "What are the core collaboration hours for remote employees?",
        "completion": "Remote employees must be reachable for synchronous collaboration during core hours between 10:00 AM and 3:00 PM local team time."
    },
    {
        "prompt": "How long is primary caregiver parental leave?",
        "completion": "Meridian Solutions provides 16 weeks of fully paid parental leave for primary caregivers to be taken within 12 months."
    },
    {
        "prompt": "What is the annual professional development stipend?",
        "completion": "Employees are eligible for a $2,000 annual professional development stipend for approved courses, certifications, and conferences."
    },
    {
        "prompt": "What is the password policy for company systems?",
        "completion": "Passwords must have a minimum of 12 characters, include uppercase, lowercase, numbers, and symbols, and rotate every 90 days with MFA enabled."
    },
    {
        "prompt": "How many in-office days are required under the hybrid work policy?",
        "completion": "Hybrid employees residing within 40 miles of an office must work in-office at least 2 days per week, specifically Tuesdays and Thursdays."
    },
    {
        "prompt": "What is the one-time home office setup stipend?",
        "completion": "Meridian provides a one-time tax-free home office stipend of $500 on the employee's second paycheck."
    },
    {
        "prompt": "How much unused PTO can be carried over to the next year?",
        "completion": "Employees can carry over up to 10 days (80 hours) of unused accrued PTO into the next calendar year; any excess is forfeited."
    },
    {
        "prompt": "What is the incident reporting window for a security breach?",
        "completion": "Suspected security incidents or compromised credentials must be reported within 1 hour to security@meridian.com or #security-incidents."
    }
]

def main():
    print("Preparing fine-tuning instruction dataset from HR documents...")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for item in SEED_QA_PAIRS:
            f.write(json.dumps(item) + "\n")
            
    print(f"Generated {len(SEED_QA_PAIRS)} instruction pairs in: {OUTPUT_FILE}")
    print("Dataset format: JSONL with 'prompt' and 'completion' fields ready for LoRA fine-tuning.")

if __name__ == "__main__":
    main()
