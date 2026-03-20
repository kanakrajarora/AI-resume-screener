import json
import re

def safe_json_loads(text):
    try:
        # remove ```json ``` wrappers
        text = re.sub(r"```json|```", "", text).strip()
        return json.loads(text)
    except:
        return {}