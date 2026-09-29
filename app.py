from pathlib import Path
import tempfile

import pandas as pd
import streamlit as st
from ultralytics import YOLO

from src.database import create_database, get_damage_records, update_damage_status, insert_damage_record
from src.gps import create_location
from src.priority import calculate_priority
from src.severity import calculate_severity


st.set_page_config(page_title="RoadVision", page_icon="🛣️", layout="wide")
create_database()

CLASS_TO_DAMAGE = {0: "D00", 1: "D10", 2: "D20", 3: "D40"}
DAMAGE_NAMES = {
    "D00": "Longitudinal Crack",
    "D10": "Transverse Crack",
    "D20": "Alligator Crack",
    "D40": "Pothole",
}


@st.cache_resource
def load_model():
    return YOLO("models/best.pt")


def records_dataframe(records):
    columns = [
        "damage_id", "damage_type", "confidence", "severity_score", "severity_level",
        "latitude", "longitude", "timestamp", "road_importance", "traffic_level",
        "location_risk", "priority_score", "priority_level", "status",
    ]
    data = pd.DataFrame(records, columns=columns)
    if not data.empty:
        data["damage"] = data["damage_type"].map(DAMAGE_NAMES).fillna(data["damage_type"])
    return data


def process_image(image_path: str, road_importance: float, traffic_level: float, location_risk: float):
    model = load_model()
    result = model.predict(source=image_path, conf=0.25, verbose=False)[0]
    image_height, image_width = result.orig_shape
    location = create_location(20.2961, 85.8245)
    detections = []

    for box in result.boxes:
        class_id = int(box.cls[0])
        damage_type = CLASS_TO_DAMAGE.get(class_id)
        if damage_type is None:
            continue
        confidence = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        severity_score, severity_level = calculate_severity(
            damage_type, confidence, x2 - x1, y2 - y1, image_width, image_height
        )
        priority_score, priority_level = calculate_priority(
            severity_score, road_importance, traffic_level, location_risk
        )
        record_id = insert_damage_record(
            damage_type, confidence, severity_score, severity_level,
            location["latitude"], location["longitude"],
            location["timestamp"].isoformat(), road_importance, traffic_level,
            location_risk, priority_score, priority_level,
        )
        detections.append({
            "id": record_id,
            "damage_type": damage_type,
            "damage_name": DAMAGE_NAMES[damage_type],
            "confidence": confidence,
            "severity_score": severity_score,
            "severity_level": severity_level,
            "priority_score": priority_score,
            "priority_level": priority_level,
            "latitude": location["latitude"],
            "longitude": location["longitude"],
        })
    return result, detections


st.title("🛣️ RoadVision")
st.caption("AI-based road damage detection and maintenance prioritization")
page = st.sidebar.radio("Navigation", ["Dashboard", "Detect Damage", "Locations", "Maintenance", "Analytics"])

if page == "Dashboard":
    data = records_dataframe(get_damage_records())
    total = len(data)
    high = int((data["priority_level"] == "HIGH").sum()) if total else 0
    critical = int((data["priority_level"] == "CRITICAL").sum()) if total else 0
    pending = int((data["status"] == "Pending").sum()) if total else 0
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total detections", total)
    c2.metric("High priority", high)
    c3.metric("Pending repairs", pending)
    c4.metric("Critical issues", critical)
    if data.empty:
        st.info("No detections yet. Open Detect Damage to analyze an image.")
    else:
        st.subheader("Recent damage reports")
        st.dataframe(data.head(10)[["damage", "confidence", "severity_level", "priority_level", "latitude", "longitude", "status"]], hide_index=True, width="stretch")
        st.subheader("Priority overview")
        st.bar_chart(data["priority_level"].value_counts())

elif page == "Detect Damage":
    st.header("Detect Road Damage")
    road_importance = st.slider("Road importance", 0, 100, 90)
    traffic_level = st.slider("Traffic level", 0, 100, 80)
    location_risk = st.slider("Location risk", 0, 100, 60)
    uploaded = st.file_uploader("Upload a road image", type=["jpg", "jpeg", "png"])
    if uploaded:
        st.image(uploaded, caption="Uploaded image", use_container_width=True)
        if st.button("Analyze image", type="primary"):
            suffix = Path(uploaded.name).suffix or ".jpg"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
                temp_file.write(uploaded.getbuffer())
                temp_path = temp_file.name
            try:
                result, detections = process_image(temp_path, road_importance, traffic_level, location_risk)
                st.image(result.plot(), caption="Detection result", use_container_width=True)
                if detections:
                    st.success(f"Saved {len(detections)} detection(s) to the database.")
                    st.dataframe(pd.DataFrame(detections), hide_index=True, width="stretch")
                else:
                    st.warning("No supported road damage was detected.")
            except Exception as error:
                st.error(f"Detection failed: {error}")

elif page == "Locations":
    st.header("Damage Locations")
    data = records_dataframe(get_damage_records())
    if data.empty:
        st.info("No locations available yet.")
    else:
        st.map(data[["latitude", "longitude"]].dropna(), latitude="latitude", longitude="longitude", zoom=15)
        st.dataframe(data[["damage", "latitude", "longitude", "priority_level", "status"]], hide_index=True, width="stretch")

elif page == "Maintenance":
    st.header("Maintenance Management")
    data = records_dataframe(get_damage_records())
    if data.empty:
        st.info("No maintenance records available yet.")
    else:
        for _, row in data.iterrows():
            with st.container(border=True):
                left, right = st.columns([4, 1])
                left.write(f"**{row['damage']}** · {row['priority_level']} · score {row['priority_score']}")
                left.caption(f"Severity: {row['severity_level']} | Location: {row['latitude']}, {row['longitude']}")
                new_status = right.selectbox("Status", ["Pending", "In Progress", "Completed"], index=["Pending", "In Progress", "Completed"].index(row["status"]), key=f"status_{row['damage_id']}")
                if new_status != row["status"] and st.button("Save", key=f"save_{row['damage_id']}"):
                    update_damage_status(int(row["damage_id"]), new_status)
                    st.success("Status updated. Refreshing records on the next run.")

elif page == "Analytics":
    st.header("Road Damage Analytics")
    data = records_dataframe(get_damage_records())
    if data.empty:
        st.info("No analytics available yet.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Damage types")
            st.bar_chart(data["damage"].value_counts())
        with c2:
            st.subheader("Severity levels")
            st.bar_chart(data["severity_level"].value_counts())
        st.subheader("Priority levels")
        st.bar_chart(data["priority_level"].value_counts())
