import json
import random
import re

from fastapi import FastAPI, Query, HTTPException

from .models import GenerateResponse

app = FastAPI(
    title="Flash‐Fiction Generator",
    version="0.1"
)

# Load data once at startup
with open("server/data/templates.json") as f:
    TEMPLATES = json.load(f)["templates"]

with open("server/data/placeholders.json") as f:
    PLACEHOLDERS = json.load(f)

# Simple pronoun map
PRONOUNS = {
    "he/she": "they",
    "himself/herself": "them"
}

PLACEHOLDER_KEYS = set(PLACEHOLDERS.keys())

@app.get("/generate", response_model=GenerateResponse)
def generate(silliness: float = Query(
    0.0, ge=0.0, le=1.0, description="0=all serious, 1=all comical"
)):
    if not 0.0 <= silliness <= 1.0:
        raise HTTPException(400, "silliness must be between 0.0 and 1.0")

    template = random.choice(TEMPLATES)

    def repl(match):
        key = match.group(1)
        # pronoun?
        if key in PRONOUNS:
            return PRONOUNS[key]
        # placeholder?
        if key in PLACEHOLDER_KEYS:
            choices = []
            serious_list = PLACEHOLDERS[key]["serious"]
            comical_list = PLACEHOLDERS[key].get("comical", [])
            # build weighted pool
            if comical_list:
                # weight serious: 1-silliness, comical: silliness
                pick_serious = random.random() > silliness
                pool = serious_list if pick_serious else comical_list
            else:
                pool = serious_list
            return random.choice(pool)
        # unknown—leave as is
        return match.group(0)

    # replace all {keys}
    filled = re.sub(r"{([^}]+)}", repl, template)
    return GenerateResponse(text=filled)
