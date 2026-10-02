
import json
import unicodedata
from collections import defaultdict

INPUT = "tolkappiyam.json"
OUTPUT = "concordance.json"


def tokenize(text):
    """Split text into Unicode letter/mark sequences."""
    text = unicodedata.normalize("NFC", text)

    words = []
    current = []

    for char in text:
        category = unicodedata.category(char)

        if category.startswith("L") or category.startswith("M"):
            current.append(char)
        else:
            if current:
                words.append("".join(current))
                current = []

    if current:
        words.append("".join(current))

    return words


def build_concordance(data):
    index = defaultdict(list)

    global_noorpa = 0

    for adhikaaram in data:
        adhikaaram_name = adhikaaram["adhikaaram"]

        for iyal_number, iyal in enumerate(
            adhikaaram["iyal"], start=1
        ):
            iyal_name = iyal["iyal_name"]

            for noorpa_number, noorpa in enumerate(
                iyal["noorpa"], start=1
            ):
                global_noorpa += 1

                original_text = noorpa["paadal"]

                for line_number, line in enumerate(
                    original_text.splitlines(), start=1
                ):
                    words = tokenize(line)

                    for position, word in enumerate(words):
                        index[word].append({
                            "adhikaaram": adhikaaram_name,
                            "iyal_name": iyal_name,
                            "iyal": iyal_number,
                            "noorpa": noorpa_number,
                            "global_noorpa": global_noorpa,
                            "line": line_number,
                            "position": position,
                            "text": line
                        })

    return dict(index)


with open(INPUT, encoding="utf-8") as f:
    data = json.load(f)

index = build_concordance(data)

with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump(
        index,
        f,
        ensure_ascii=False,
        indent=2
    )

print(f"Distinct words: {len(index)}")
print(f"Total occurrences: {sum(map(len, index.values()))}")
