# See https://pypi.org/project/tholkaappiyam/
from tholkaappiyam import thol
import json

# Returns the entire JSON dataset of Tholkaappiyam to the user
data = thol.data_json()

# read it back as dictionary
if isinstance(data, str):
    data = json.loads(data)

# write it as json so that output is readable with indent
# and Tamil characters show up without being unicode escaped.
with open("tolkappiyam.json", "w") as file:
    json.dump(data, file, indent=2, ensure_ascii=False)
    file.write('\n')

