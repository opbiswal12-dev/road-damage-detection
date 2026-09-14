# GPS / Location module

from datetime import datetime


def create_location(latitude, longitude):

    timestamp = datetime.now()

    location = {
        "latitude": latitude,
        "longitude": longitude,
        "timestamp": timestamp
    }

    return location


# Test

location = create_location(
    20.2961,
    85.8245
)

print("GPS Location")
print("Latitude:", location["latitude"])
print("Longitude:", location["longitude"])
print("Timestamp:", location["timestamp"])