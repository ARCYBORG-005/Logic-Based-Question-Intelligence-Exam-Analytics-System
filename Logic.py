import re
import json

INPUT_PATH = "data/processed/questions/number_system_100_percent.txt"
OUTPUT_JSON = "data/processed/questions/number_system_master.json"

# Semantic Logic Map (Using Patterns instead of just words)
SMART_MAP = {
    "Unit Digit Logic": [
        r"\d+\s*\^",                 # Matches exponents like 7^105
        r"units?\s+digit",           # Matches "unit digit" or "units digit"
        r"last\s+digit"              # Matches "last digit"
    ],
    "Arithmetic & Geometric Progression": [
        r"A\.P\.", r"G\.P\.",        # Matches short forms
        r"progression",              # Matches the word
        r"sum\s+of\s+first\s+\d+",   # Matches "sum of first 100"
        r"a\s*\+\s*\(n\s*-\s*1\)d"   # Matches the formula itself
    ],
    "Divisibility & Remainders": [
        r"divisible", r"divided\s+by", 
        r"remainder", r"multiple\s+of"
    ],
    "Digit Manipulation": [
        r"two-digit", r"interchanging", 
        r"reversed", r"ten's\s+digit"
    ]
}

def upgrade_logic_database():
    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        blocks = f.read().strip().split("\n\n")
    
    master_data = []
    for block in blocks:
        block = block.strip()
        num_match = re.match(r"^(\d+)\.", block)
        q_id = int(num_match.group(1)) if num_match else 0
        
        assigned_variety = "Basic Arithmetic"
        low_block = block.lower()
        
        # Check against patterns
        for variety, patterns in SMART_MAP.items():
            if any(re.search(p, block if p.isupper() else low_block) for p in patterns):
                assigned_variety = variety
                break
        
        master_data.append({
            "id": q_id,
            "variety": assigned_variety,
            "text": block
        })

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(master_data, f, indent=4)
    
    print(f"✅ Logic Upgraded. Total Questions: {len(master_data)}")

if __name__ == "__main__":
    upgrade_logic_database()
