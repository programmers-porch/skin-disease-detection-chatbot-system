MAX_CONFIDENCE = 95
MIN_CONFIDENCE = 10
LOW_CONFIDENCE_THRESHOLD = 50

WEIGHTS = {
    "alias": 8.0,
    "core": 4.5,
    "appearance": 3.5,
    "location": 2.5,
    "trigger": 2.0,
    "red_flag": 2.5,
    "token_overlap": 0.7,
    "severity_boost": {
        "common": 0.0,
        "medium": 0.5,
        "critical": 1.0
    }
}