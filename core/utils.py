import json, os, hashlib
from datetime import datetime
from .config import SALT, DATA_FILE

def _hash(value: str) -> str:
    return hashlib.sha256((SALT + str(value)).encode("utf-8")).hexdigest()[:16]

def anonymize_candidate(candidate: dict) -> dict:
    # Start with core hashed info
    record = {
        "id": _hash(candidate.get("email","") + candidate.get("phone","")),
        "name": candidate.get("name",""),
        "email": candidate.get("email",""),
        "phone": candidate.get("phone",""),
        "name_hash": _hash(candidate.get("name","")),
        "email_hash": _hash(candidate.get("email","")),
        "phone_hash": _hash(candidate.get("phone","")),
        "years_exp": candidate.get("years_exp"),
        "desired_positions": candidate.get("desired_positions"),
        "location": candidate.get("location"),
        "tech_stack": candidate.get("tech_stack", []),
        "created_at": datetime.utcnow().isoformat() + "Z"
    }

    # Include fresher info if present
    fresher_fields = ["degree", "domain", "cgpa", "marks_12th", "marks_10th"]
    for field in fresher_fields:
        if field in candidate:
            record[field] = candidate[field]

    # Include experience info if present
    exp_fields = ["last_company", "years_in_company", "position_in_company"]
    for field in exp_fields:
        if field in candidate:
            record[field] = candidate[field]

    return record


def save_candidate(candidate: dict):
    records = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                records = json.load(f)
        except Exception:
            records = []
    records.append(candidate)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)
