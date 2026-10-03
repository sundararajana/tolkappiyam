# See https://pypi.org/project/tholkaappiyam/
from tholkaappiyam import thol
import json

# Returns the entire JSON dataset of Tholkaappiyam to the user
data = thol.data_json()

# read it back as dictionary
if isinstance(data, str):
    data = json.loads(data)

# The nurpa missing from the PyPI dataset
missing_nurpa = {
    "paadal": "வாயுறை வாழ்த்தே வயங்க நாடின்\nவேம்புங் கடுவும் போல வெஞ்சொல்\nதாங்குதல் இன்றி வழிநனி பயக்குமென்று\nஓம்படைக் கிளவியின் வாயுறுத் தற்றே.",
    "vilakkam": {
        "paadal_category": "",
        "paadal_meaning": ""
    }
}

# Traverse the nested structure to find the 1362nd nurpa and insert the missing one
global_count = 0
inserted = False

for adhikaram in data:
    for iyal in adhikaram['iyal']:
        noorpa_list = iyal['noorpa']

        for index, noorpa in enumerate(noorpa_list):
            global_count += 1

            # The moment we hit 1362, insert our missing nurpa at the NEXT index
            if global_count == 1362:
                noorpa_list.insert(index + 1, missing_nurpa)
                inserted = True
                break

        if inserted: break
    if inserted: break

# Recount the actual total by walking the final modified structure
final_global_count = 0
for adhikaram in data:
    for iyal in adhikaram['iyal']:
        final_global_count += len(iyal['noorpa'])

# write it as json so that output is readable with indent
# and Tamil characters show up without being unicode escaped.
with open("tolkappiyam.json", "w", encoding="utf-8") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)
    file.write('\n')

print(f"Missing nurpa successfully injected. Total global nurpas : {final_global_count}")
