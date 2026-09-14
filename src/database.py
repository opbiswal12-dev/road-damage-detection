# Database module for road damage detection

import sqlite3


DATABASE_PATH = "data/road_damage.db"


def create_database():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS road_damage (

            damage_id INTEGER PRIMARY KEY AUTOINCREMENT,

            damage_type TEXT,
            confidence REAL,

            severity_score REAL,
            severity_level TEXT,

            latitude REAL,
            longitude REAL,
            timestamp TEXT,

            road_importance REAL,
            traffic_level REAL,
            location_risk REAL,

            priority_score REAL,
            priority_level TEXT,

            status TEXT
        )
    """)

    connection.commit()
    connection.close()


def insert_damage_record(
    damage_type,
    confidence,
    severity_score,
    severity_level,
    latitude,
    longitude,
    timestamp,
    road_importance,
    traffic_level,
    location_risk,
    priority_score,
    priority_level
):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO road_damage (
            damage_type,
            confidence,
            severity_score,
            severity_level,
            latitude,
            longitude,
            timestamp,
            road_importance,
            traffic_level,
            location_risk,
            priority_score,
            priority_level,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        damage_type,
        confidence,
        severity_score,
        severity_level,
        latitude,
        longitude,
        timestamp,
        road_importance,
        traffic_level,
        location_risk,
        priority_score,
        priority_level,
        "Pending"
    ))

    connection.commit()
    connection.close()

    print("Damage record inserted successfully!")


def get_damage_records():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("SELECT * FROM road_damage")

    records = cursor.fetchall()

    connection.close()

    return records


# ==========================================
# TEST
# ==========================================

create_database()

print("Database created successfully!")

print()
print("Saved Road Damage Records:")

records = get_damage_records()

for record in records:
    print(record)