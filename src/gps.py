"""Location helpers."""

from datetime import datetime, timezone


def create_location(latitude: float, longitude: float) -> dict:
    return {
        "latitude": float(latitude),
        "longitude": float(longitude),
        "timestamp": datetime.now(timezone.utc),
    }


if __name__ == "__main__":
    print(create_location(20.2961, 85.8245))
