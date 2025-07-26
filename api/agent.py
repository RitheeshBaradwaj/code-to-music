def map_to_mood(metrics):
    if metrics["functions"] > 5 and metrics["loops"] > 3:
        return "tense"
    if metrics["branches"] > 10:
        return "chaotic"
    return "calm"
