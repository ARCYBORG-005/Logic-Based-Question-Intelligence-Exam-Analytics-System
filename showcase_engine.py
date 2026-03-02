import pdfplumber
import re
import os

PDF_PATH = "data/raw/rs_aggarwal.pdf"
OUTPUT_PATH = "data/processed/questions/number_system_exercise_final.txt"

def extract_step_1_refined():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    
    # Scanning a wider range to catch the 1-153 gap
    START_PAGE = 8 
    END_PAGE = 60
    
    exercise_questions = []
    # Pattern: Number at start of line
    q_start_re = re.compile(r"^(\d+)\.\s")
    # Pattern: Must contain options to be a valid exercise question
    options_re = re.compile(r"\(a\).+\(b\).+\(c\).+\(d\)")

    with pdfplumber.open(PDF_PATH) as pdf:
        for p_idx in range(START_PAGE - 1, END_PAGE):
            page = pdf.pages[p_idx]
            width = page.width
            
            # Use three zones: Left Column, Middle Gutter (Ignore), Right Column
            left_zone = page.within_bbox((0, 40, width/2 - 5, page.height - 40))
            right_zone = page.within_bbox((width/2 + 5, 40, width, page.height - 40))

            for zone in [left_zone, right_zone]:
                text = zone.extract_text()
                if not text: continue
                
                lines = text.split('\n')
                current_q = ""
                
                for line in lines:
                    line = line.strip()
                    if q_start_re.match(line):
                        # Save previous question if it looks like a real question (has options)
                        if current_q and ("(a)" in current_q or "(b)" in current_q):
                            exercise_questions.append(current_q)
                        current_q = line
                    else:
                        if current_q:
                            current_q += " " + line
                
                # Add the last one in the zone
                if current_q and ("(a)" in current_q or "(b)" in current_q):
                    exercise_questions.append(current_q)

            print(f"Deep Scanning Page {p_idx + 1}...")

    # Final Filter: Remove duplicates and sort by number
    seen_nums = set()
    final_list = []
    for q in exercise_questions:
        num = int(q_start_re.match(q).group(1))
        if num not in seen_nums:
            final_list.append(q)
            seen_nums.add(num)
    
    final_list.sort(key=lambda x: int(q_start_re.match(x).group(1)))

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n\n".join(final_list))
    
    print(f"\n STEP 1 REFINED: Found {len(final_list)} unique questions.")
    print(f"Check if Question 1 and Question 380 are both in {OUTPUT_PATH}.")

if __name__ == "__main__":
    extract_step_1_refined()
