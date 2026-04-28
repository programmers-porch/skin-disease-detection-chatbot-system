from utils.text_processing import normalize, tokenize
from config.settings import WEIGHTS

def phrase_match(phrase: str, text: str) -> bool:
    return normalize(phrase) in normalize(text)

def score_disease(user_text: str, disease: dict):
    text = normalize(user_text)
    tokens = set(tokenize(user_text))

    score = 0.0
    matches = []
    red_flag_hits = []

    for alias in disease.get("aliases", []):
        if phrase_match(alias, text):
            score += WEIGHTS["alias"]
            matches.append(f"alias: {alias}")

    for field, weight in [
        ("core_symptoms", WEIGHTS["core"]),
        ("appearance", WEIGHTS["appearance"]),
        ("common_locations", WEIGHTS["location"]),
        ("triggers", WEIGHTS["trigger"]),
    ]:
        for item in disease.get(field, []):
            if phrase_match(item, text):
                score += weight
                matches.append(f"{field.replace('_', ' ')}: {item}")

    for item in disease.get("red_flags", []):
        if phrase_match(item, text):
            score += WEIGHTS["red_flag"]
            red_flag_hits.append(item)

    for item in disease.get("core_symptoms", []) + disease.get("appearance", []) + disease.get("common_locations", []) + disease.get("triggers", []):
        words = set(tokenize(item))
        overlap = len(tokens.intersection(words))
        if overlap:
            score += overlap * WEIGHTS["token_overlap"]

    severity = disease.get("severity_level", "common")
    score += WEIGHTS["severity_boost"].get(severity, 0.0)

    return score, matches, red_flag_hits

def rank_diseases(user_text: str, db: list):
    results = []
    for disease in db:
        score, matches, red_flag_hits = score_disease(user_text, disease)
        results.append({
            "disease": disease,
            "score": score,
            "matches": matches,
            "red_flag_hits": red_flag_hits
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results