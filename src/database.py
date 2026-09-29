"""SQLite persistence for road-damage detections."""

from pathlib import Path
import sqlite3
from typing import Any, Iterable


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "road_damage.db"


def create_database() -> None:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS road_damage (
                damage_id INTEGER PRIMARY KEY AUTOINCREMENT,
                damage_type TEXT NOT NULL,
                confidence REAL NOT NULL,
                severity_score REAL NOT NULL,
                severity_level TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                timestamp TEXT NOT NULL,
                road_importance REAL NOT NULL,
                traffic_level REAL NOT NULL,
                location_risk REAL NOT NULL,
                priority_score REAL NOT NULL,
                priority_level TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending'
            )
            """
        )


def insert_damage_record(
    damage_type: str,
    confidence: float,
    severity_score: float,
    severity_level: str,
    latitude: float,
    longitude: float,
    timestamp: str,
    road_importance: float,
    traffic_level: float,
    location_risk: float,
    priority_score: float,
    priority_level: str,
    status: str = "Pending",
) -> int:
    create_database()
    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(
            """
            INSERT INTO road_damage (
                damage_type, confidence, severity_score, severity_level,
                latitude, longitude, timestamp, road_importance, traffic_level,
                location_risk, priority_score, priority_level, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                damage_type, confidence, severity_score, severity_level,
                latitude, longitude, timestamp, road_importance, traffic_level,
                location_risk, priority_score, priority_level, status,
            ),
        )
        return int(cursor.lastrowid)


def get_damage_records(limit: int | None = None) -> list[tuple[Any, ...]]:
    create_database()
    query = "SELECT * FROM road_damage ORDER BY damage_id DESC"
    parameters: Iterable[int] = ()
    if limit is not None:
        query += " LIMIT ?"
        parameters = (limit,)
    with sqlite3.connect(DATABASE_PATH) as connection:
        return connection.execute(query, tuple(parameters)).fetchall()


def update_damage_status(damage_id: int, status: str) -> None:
    if status not in {"Pending", "In Progress", "Completed"}:
        raise ValueError("Invalid maintenance status")
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            "UPDATE road_damage SET status = ? WHERE damage_id = ?",
            (status, damage_id),
        )


if __name__ == "__main__":
    create_database()
    print(f"Database ready: {DATABASE_PATH}")
