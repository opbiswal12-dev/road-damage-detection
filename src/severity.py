"""Heuristic severity scoring for detected road damage."""

DAMAGE_TYPE_SCORES = {
    "D00": 25,  # Longitudinal crack
    "D10": 35,  # Transverse crack
    "D20": 60,  # Alligator crack
    "D40": 65,  # Pothole
}


def calculate_size_score(area_ratio: float) -> int:
    if area_ratio < 0.01:
        return 10
    if area_ratio < 0.05:
        return 25
    if area_ratio < 0.10:
        return 50
    if area_ratio < 0.20:
        return 75
    return 100


def calculate_severity(
    damage_type: str,
    confidence: float,
    box_width: float,
    box_height: float,
    image_width: float,
    image_height: float,
) -> tuple[float, str]:
    if damage_type not in DAMAGE_TYPE_SCORES:
        raise ValueError(f"Unknown damage type: {damage_type}")
    if image_width <= 0 or image_height <= 0:
        raise ValueError("Image dimensions must be positive")

    confidence = max(0.0, min(1.0, float(confidence)))
    area_ratio = max(0.0, box_width * box_height) / (image_width * image_height)
    score = (
        0.40 * DAMAGE_TYPE_SCORES[damage_type]
        + 0.40 * calculate_size_score(area_ratio)
        + 0.20 * confidence * 100
    )
    score = round(max(0.0, min(100.0, score)), 2)
    level = "LOW" if score <= 25 else "MEDIUM" if score <= 50 else "HIGH" if score <= 75 else "CRITICAL"
    return score, level


def yolo_to_pixel_box(normalized_width, normalized_height, image_width, image_height):
    return normalized_width * image_width, normalized_height * image_height


if __name__ == "__main__":
    print(calculate_severity("D40", 0.92, 200, 150, 1000, 1000))
