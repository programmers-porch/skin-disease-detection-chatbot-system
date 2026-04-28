from config.settings import MAX_CONFIDENCE, MIN_CONFIDENCE, LOW_CONFIDENCE_THRESHOLD

def confidence_from_scores(top_score: float, second_score: float) -> int:
    if top_score <= 0:
        return 0
    gap = max(0.0, top_score - second_score)
    estimate = 30 + (top_score * 4.0) + (gap * 5.0)
    return max(MIN_CONFIDENCE, min(MAX_CONFIDENCE, int(estimate)))

def build_response(top_result: dict, second_score: float):
    disease = top_result["disease"]
    score = top_result["score"]
    matches = top_result["matches"]
    red_flag_hits = top_result["red_flag_hits"]

    confidence = confidence_from_scores(score, second_score)

    lines = []
    lines.append(f"Most likely condition: **{disease['name']}**")
    lines.append(f"Severity level: **{disease.get('severity_level', 'common')}**")
    lines.append(f"Estimated confidence: **{confidence}%**")
    lines.append("")

    if matches:
        lines.append("Why this was suggested:")
        for item in matches[:6]:
            lines.append(f"- {item}")
        lines.append("")

    if red_flag_hits:
        lines.append("Urgent warning signs mentioned in your text:")
        for item in red_flag_hits[:5]:
            lines.append(f"- {item}")
        lines.append("")

    lines.append("Common symptoms:")
    for item in disease.get("core_symptoms", [])[:5]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("Typical locations:")
    for item in disease.get("common_locations", [])[:5]:
        lines.append(f"- {item}")

    lines.append("")
    lines.append("Basic precautions:")
    for item in disease.get("advice", [])[:5]:
        lines.append(f"- {item}")

    questions = disease.get("questions", [])
    if confidence < LOW_CONFIDENCE_THRESHOLD and questions:
        lines.append("")
        lines.append("To improve accuracy, answer these:")
        for q in questions[:3]:
            lines.append(f"- {q}")

    if disease.get("sources"):
        lines.append("")
        lines.append("Sources used:")
        for src in disease["sources"]:
            label = src.get("label", "Source")
            url = src.get("url", "")
            lines.append(f"- {label}: {url}")

    lines.append("")
    lines.append("Note: This is for educational use only and is not a medical diagnosis.")

    return "\n".join(lines)