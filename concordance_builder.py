import json
import re
import unicodedata
from collections import defaultdict

INPUT_FILE = "tolkappiyam.json"
OUTPUT_FILE = "concordance.json"

def tokenize(text):
    text = unicodedata.normalize("NFC", text)
    return re.findall(r"[\u0B80-\u0BFF]+", text)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    corpus = json.load(f)

nurpas = []
concordance = defaultdict(list)

global_noorpa = 0

for adhikaaram in corpus:
    for iyal_number, iyal_data in enumerate(adhikaaram["iyal"], start=1):
        for noorpa_number, noorpa_data in enumerate(
            iyal_data["noorpa"], start=1
        ):
            global_noorpa += 1

            paadal = unicodedata.normalize(
                "NFC", noorpa_data["paadal"]
            )
            nurpas.append(paadal)

            paadal_position = 0

            lines = paadal.splitlines()

            for line_number, line in enumerate(lines, start=1):
                words = tokenize(line)

                for position, word in enumerate(words):
                    concordance[word].append({
                        "adhikaaram": adhikaaram["adhikaaram"],
                        "iyal_name": iyal_data["iyal_name"],
                        "iyal": iyal_number,
                        "noorpa": noorpa_number,
                        "global_noorpa": global_noorpa,
                        "line": line_number,
                        "position": position,
                        "paadal_position": paadal_position
                    })
                    paadal_position += 1

output = { "nurpas" : nurpas, "concordance" : concordance };

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        output,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"Distinct words: {len(concordance)}")
print(
    "Total occurrences:",
    sum(len(v) for v in concordance.values())
)
