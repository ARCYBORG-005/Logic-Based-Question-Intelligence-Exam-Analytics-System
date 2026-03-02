import re
import json
import os

INPUT_PATH = "data/processed/questions/number_system_100_percent.txt"
OUTPUT_JSON = "data/processed/questions/number_system_master.json"

# Advanced Logic Map for Number System Variety
VARIETY_MAP = {
    "Unit Digit Logic": [r"unit digit", r"last digit", r"unit's place", r"digit in the units"],
    "Divisibility & Remainders": [r"divisible", r"divided by", r"remainder", r"multiple of", r"completely divided"],
    "Place & Face Value": [r"place value", r"face value", r"local value"],
    "Digit Manipulation": [r"two-digit", r"three-digit", r"interchanging", r"reversed", r"sum of the digits"],
    "Number Theory (Primes/Factors)": [r"prime", r"composite", r"rational", r"irrational", r"factors", r"natural number"],
    "Arithmetic Series (AP/GP)": [r"sum of first", r"arithmetic progression", r"geometric", r"a \+ \(n-1\)d"],
    "Factorials & Zeros": [r"number of zeros", r"factorial", r"n!"]
}

def final_logic_polish():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        # Splitting by double newline ensures we treat each of the 380 blocks separately
        blocks = f.read().strip().split("\n\n")
    
    master_data = []

    for block in blocks:
        block = block.strip()
        if not block: continue

        # 1. Clean Question Number
        num_match = re.match(r"^(\d+)\.", block)
        q_id = num_match.group(1) if num_match else "Unknown"

        # 2. Advanced Variety Tagging
        assigned_variety = "Basic Calculation" # Default for things like 123 + 456
        low_block = block.lower()
        for variety, patterns in VARIETY_MAP.items():
            if any(re.search(p, low_block) for p in patterns):
                assigned_variety = variety
                break

        # 3. Source & Difficulty
        source_match = re.search(r"\[([^\]]+)\]|\(([^)]+, \d{4})\)", block)
        source = source_match.group(0) if source_match else "General"
        
        # Difficulty Logic: Question length + presence of variables (x, n, m)
        if len(block) > 220 or any(var in low_block for var in [" n ", " x ", " m "]):
            difficulty = "Hard"
        elif len(block) < 110:
            difficulty = "Easy"
        else:
            difficulty = "Medium"

        master_data.append({
            "id": int(q_id) if q_id.isdigit() else q_id,
            "variety": assigned_variety,
            "difficulty": difficulty,
            "source": source,
            "text": block
        })

    # Save finalized JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(master_data, f, indent=4)

    print(f"🎯 MASTER JSON CREATED: {len(master_data)} questions processed.")
    print(f"Missing IDs: {[i for i in range(1, 381) if i not in [d['id'] for d in master_data]]}")

if __name__ == "__main__":
    final_logic_polish()
