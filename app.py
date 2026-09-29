import streamlit as st
import sqlite3
import pandas as pd
import textwrap
from ultralytics import YOLO

from src.severity import calculate_severity
from src.priority import calculate_priority
from src.gps import create_location
from src.database import insert_damage_record


DATABASE_PATH = "data/road_damage.db"


# ============================================================
# DATABASE FUNCTION
# ============================================================

def get_damage_records():

    connection = sqlite3.connect(DATABASE_PATH)

    records = connection.execute("""
        SELECT
            damage_type,
            confidence,
            severity_score,
            severity_level,
            latitude,
            longitude,
            priority_score,
            priority_level,
            status
        FROM road_damage
        ORDER BY rowid DESC
    """).fetchall()

    connection.close()

    return records


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RoadVision",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1e293b;
    }

    section[data-testid="stSidebar"] * {
        color: #e2e8f0;
    }

    .main-title {
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 16px;
        margin-bottom: 30px;
    }

    .metric-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 22px;
        min-height: 130px;
    }

    .metric-title {
        color: #94a3b8;
        font-size: 14px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 32px;
        font-weight: 700;
    }

    .metric-description {
        color: #64748b;
        font-size: 13px;
        margin-top: 5px;
    }

    .section-title {
        font-size: 22px;
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🛣️ RoadVision")

    st.caption("Road Damage Detection & Maintenance")

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "📊 Dashboard",
            "🔍 Detect Damage",
            "📍 Locations",
            "🔧 Maintenance",
            "📈 Analytics"
        ]
    )

    st.markdown("---")

    st.caption("System Status")

    st.success("● System Online")

    st.caption("YOLO Detection Engine")

    st.caption("Database Connected")


# ============================================================
# DASHBOARD
# ============================================================

if page == "📊 Dashboard":

    st.markdown(
        '<div class="main-title">Road Damage Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Monitor road conditions, detect damage and prioritize maintenance.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Get REAL records from database
    # --------------------------------------------------------

    records = get_damage_records()


    # --------------------------------------------------------
    # KPI calculations
    # --------------------------------------------------------

    total_detections = len(records)

    high_priority = sum(
        1 for record in records
        if record[7] == "HIGH"
    )

    pending_repairs = sum(
        1 for record in records
        if record[8] == "Pending"
    )

    critical_issues = sum(
        1 for record in records
        if record[7] == "CRITICAL"
    )


    # ========================================================
    # KPI CARDS
    # ========================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.html(textwrap.dedent(f"""
        <div class="metric-card">

            <div class="metric-title">
                Total Detections
            </div>

            <div class="metric-value">
                {total_detections}
            </div>

            <div class="metric-description">
                Road damage detected
            </div>

        </div>
        """))


    with col2:

        st.html(textwrap.dedent(f"""
        <div class="metric-card">

            <div class="metric-title">
                High Priority
            </div>

            <div class="metric-value">
                {high_priority}
            </div>

            <div class="metric-description">
                Require attention
            </div>

        </div>
        """))


    with col3:

        st.html(textwrap.dedent(f"""
        <div class="metric-card">

            <div class="metric-title">
                Pending Repairs
            </div>

            <div class="metric-value">
                {pending_repairs}
            </div>

            <div class="metric-description">
                Awaiting maintenance
            </div>

        </div>
        """))


    with col4:

        st.html(textwrap.dedent(f"""
        <div class="metric-card">

            <div class="metric-title">
                Critical Issues
            </div>

            <div class="metric-value">
                {critical_issues}
            </div>

            <div class="metric-description">
                Immediate attention
            </div>

        </div>
        """))


    # ========================================================
    # REAL PRIORITY OVERVIEW
    # ========================================================

    left, right = st.columns([2, 1])


    with left:

        st.markdown(
            '<div class="section-title">'
            'Damage Priority Overview'
            '</div>',
            unsafe_allow_html=True
        )


        if records:

            priority_counts = {
                "CRITICAL": 0,
                "HIGH": 0,
                "MEDIUM": 0,
                "LOW": 0
            }


            for record in records:

                priority_level = record[7]

                if priority_level in priority_counts:

                    priority_counts[priority_level] += 1


            chart_data = pd.DataFrame({

                "Priority": [
                    "Critical",
                    "High",
                    "Medium",
                    "Low"
                ],

                "Cases": [
                    priority_counts["CRITICAL"],
                    priority_counts["HIGH"],
                    priority_counts["MEDIUM"],
                    priority_counts["LOW"]
                ]
            })


            st.bar_chart(
                chart_data.set_index("Priority")
            )

        else:

            st.info(
                "No detection records are available yet."
            )


    # ========================================================
    # SYSTEM SUMMARY
    # ========================================================

    with right:

        st.markdown(
            '<div class="section-title">'
            'System Summary'
            '</div>',
            unsafe_allow_html=True
        )


        st.info(
            """
            **RoadVision** uses computer vision to identify road damage
            from images.

            The system calculates:

            • Damage severity  
            • Road priority  
            • Location  
            • Maintenance status
            """
        )


        st.success(
            "Dashboard data is connected to the SQLite database."
        )


    # ========================================================
    # REAL RECENT DAMAGE REPORTS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Recent Damage Reports'
        '</div>',
        unsafe_allow_html=True
    )


    if records:

        recent_rows = []


        for record in records[:10]:

            damage_code = record[0]

            damage_names = {

                "D00": "Longitudinal Crack",

                "D10": "Transverse Crack",

                "D20": "Alligator Crack",

                "D40": "Pothole"
            }


            damage_name = damage_names.get(
                damage_code,
                damage_code
            )


            recent_rows.append({

                "Damage": damage_name,

                "Confidence":
                    f"{record[1] * 100:.2f}%",

                "Severity":
                    record[3],

                "Priority":
                    record[7],

                "Latitude":
                    record[4],

                "Longitude":
                    record[5],

                "Status":
                    record[8]
            })


        recent_data = pd.DataFrame(
            recent_rows
        )


        st.dataframe(
            recent_data,
            width="stretch",
            hide_index=True
        )


    else:

        st.info(
            "No damage reports have been saved yet."
        )


# ============================================================
# DETECT DAMAGE
# ============================================================

elif page == "🔍 Detect Damage":

    st.markdown(
        '<div class="main-title">'
        'Detect Road Damage'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="subtitle">'
        'Upload a road image and analyze it using the trained YOLO model.'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # LOAD TRAINED MODEL
    # ========================================================

    model = YOLO("models/best.pt")


    # ========================================================
    # IMAGE UPLOAD
    # ========================================================

    uploaded_file = st.file_uploader(
        "Upload a road image",
        type=[
            "jpg",
            "jpeg",
            "png"
        ]
    )


    if uploaded_file is not None:

        st.image(
            uploaded_file,
            caption="Uploaded Road Image",
            width="stretch"
        )


        # ====================================================
        # ANALYZE BUTTON
        # ====================================================

        if st.button(
            "🔍 Analyze Image",
            width="stretch"
        ):


            # ------------------------------------------------
            # Save uploaded image
            # ------------------------------------------------

            image_path = "uploaded_road.jpg"


            with open(
                image_path,
                "wb"
            ) as file:

                file.write(
                    uploaded_file.getbuffer()
                )


            # ------------------------------------------------
            # Run YOLO
            # ------------------------------------------------

            results = model.predict(
                source=image_path,
                conf=0.05
            )


            result = results[0]


            # ------------------------------------------------
            # Annotated image
            # ------------------------------------------------

            annotated_image = result.plot()


            st.image(
                annotated_image,
                caption="YOLO Detection Result",
                width="stretch"
            )


            # ------------------------------------------------
            # Detection count
            # ------------------------------------------------

            detection_count = len(result.boxes)


            st.success(
                f"Detection completed! "
                f"{detection_count} damage(s) detected."
            )


            # ====================================================
            # CLASS MAPPING
            # ====================================================

            CLASS_TO_DAMAGE = {

                0: "D00",

                1: "D10",

                2: "D20",

                3: "D40"
            }


            DAMAGE_NAMES = {

                "D00": "Longitudinal Crack",

                "D10": "Transverse Crack",

                "D20": "Alligator Crack",

                "D40": "Pothole"
            }


            # ====================================================
            # GPS LOCATION
            # ====================================================

            location = create_location(
                20.2961,
                85.8245
            )


            latitude = location["latitude"]

            longitude = location["longitude"]

            timestamp = location["timestamp"]


            # ====================================================
            # PROCESS DETECTIONS
            # ====================================================

            if detection_count > 0:

                st.markdown(
                    '<div class="section-title">'
                    'Detection Details'
                    '</div>',
                    unsafe_allow_html=True
                )


                image_height, image_width = result.orig_shape


                for i, box in enumerate(result.boxes):


                    # ========================================
                    # CLASS
                    # ========================================

                    class_id = int(
                        box.cls[0]
                    )


                    # ========================================
                    # CONFIDENCE
                    # ========================================

                    confidence = float(
                        box.conf[0]
                    )


                    # ========================================
                    # DAMAGE CODE
                    # ========================================

                    damage_code = CLASS_TO_DAMAGE.get(
                        class_id,
                        "Unknown"
                    )


                    # ========================================
                    # DAMAGE NAME
                    # ========================================

                    damage_name = DAMAGE_NAMES.get(
                        damage_code,
                        "Unknown Damage"
                    )


                    # ========================================
                    # BOUNDING BOX
                    # ========================================

                    x1, y1, x2, y2 = (
                        box.xyxy[0].tolist()
                    )


                    box_width = x2 - x1

                    box_height = y2 - y1


                    # ========================================
                    # SEVERITY
                    # ========================================

                    severity_score, severity_level = calculate_severity(

                        damage_code,

                        confidence,

                        box_width,

                        box_height,

                        image_width,

                        image_height
                    )


                    # ========================================
                    # PRIORITY
                    # ========================================

                    road_importance = 90

                    traffic_level = 80

                    location_risk = 60


                    priority_score, priority_level = calculate_priority(

                        severity_score,

                        road_importance,

                        traffic_level,

                        location_risk
                    )


                    # ========================================
                    # SAVE TO DATABASE
                    # ========================================

                    insert_damage_record(

                        damage_type=damage_code,

                        confidence=confidence,

                        severity_score=severity_score,

                        severity_level=severity_level,

                        latitude=latitude,

                        longitude=longitude,

                        timestamp=str(timestamp),

                        road_importance=road_importance,

                        traffic_level=traffic_level,

                        location_risk=location_risk,

                        priority_score=priority_score,

                        priority_level=priority_level
                    )


                    # ========================================
                    # DISPLAY RESULT
                    # ========================================

                    st.html(textwrap.dedent(f"""

                    <div class="metric-card">

                        <div class="metric-title">

                            Detection {i + 1}

                        </div>


                        <div class="metric-value">

                            {damage_name}

                        </div>


                        <div class="metric-description">

                            Damage Code:
                            {damage_code}

                            <br>

                            Confidence:
                            {confidence * 100:.2f}%

                            <br>

                            Bounding Box:
                            {box_width:.2f} ×
                            {box_height:.2f} pixels

                            <br>

                            Severity Score:
                            {severity_score:.2f}

                            <br>

                            Severity Level:
                            {severity_level}

                            <br>

                            Road Importance:
                            {road_importance}

                            <br>

                            Traffic Level:
                            {traffic_level}

                            <br>

                            Location Risk:
                            {location_risk}

                            <br>

                            Priority Score:
                            {priority_score:.2f}

                            <br>

                            Priority Level:
                            {priority_level}

                            <br>

                            Latitude:
                            {latitude}

                            <br>

                            Longitude:
                            {longitude}

                            <br>

                            Status:
                            Pending

                        </div>

                    </div>

                    """))


                st.success(
                    f"{detection_count} detection(s) "
                    f"saved successfully to the database."
                )


            else:

                st.warning(
                    "No road damage was detected in this image."
                )


    else:

        st.info(
            "Upload a road image to begin damage detection."
        )


# ============================================================
# LOCATIONS
# ============================================================

# ============================================================
# LOCATIONS
# ============================================================

elif page == "📍 Locations":

    st.markdown(
        '<div class="main-title">'
        'Damage Locations'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'View detected road damage locations from the database.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Get real records from database
    # --------------------------------------------------------

    records = get_damage_records()

    if records:

        # Create list for map
        location_rows = []

        for record in records:

            latitude = record[4]
            longitude = record[5]

            location_rows.append({
                "latitude": latitude,
                "longitude": longitude
            })

        location_data = pd.DataFrame(location_rows)

        # ----------------------------------------------------
        # Display map
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Detected Damage Locations'
            '</div>',
            unsafe_allow_html=True
        )

        st.map(
            location_data,
            latitude="latitude",
            longitude="longitude",
            zoom=15
        )

        # ----------------------------------------------------
        # Display location details
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Location Details'
            '</div>',
            unsafe_allow_html=True
        )

        location_details = []

        damage_names = {

            "D00": "Longitudinal Crack",

            "D10": "Transverse Crack",

            "D20": "Alligator Crack",

            "D40": "Pothole"
        }

        for record in records:

            damage_code = record[0]

            location_details.append({

                "Damage":
                    damage_names.get(
                        damage_code,
                        damage_code
                    ),

                "Latitude":
                    record[4],

                "Longitude":
                    record[5],

                "Priority":
                    record[7],

                "Status":
                    record[8]
            })

        location_table = pd.DataFrame(
            location_details
        )

        st.dataframe(
            location_table,
            width="stretch",
            hide_index=True
        )

    else:

        st.info(
            "No damage locations are available yet. "
            "Run an image through the Detect Damage page first."
        )


# ============================================================
# MAINTENANCE
# ============================================================
# ============================================================
# MAINTENANCE
# ============================================================

elif page == "🔧 Maintenance":

    st.markdown(
        '<div class="main-title">'
        'Maintenance Management'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Track road repair priorities and maintenance status.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # Get real records from database
    # --------------------------------------------------------

    records = get_damage_records()

    if records:

        # ----------------------------------------------------
        # Damage name mapping
        # ----------------------------------------------------

        damage_names = {

            "D00": "Longitudinal Crack",

            "D10": "Transverse Crack",

            "D20": "Alligator Crack",

            "D40": "Pothole"
        }


        # ----------------------------------------------------
        # Create maintenance table
        # ----------------------------------------------------

        maintenance_rows = []


        for record in records:

            damage_code = record[0]

            damage_name = damage_names.get(
                damage_code,
                damage_code
            )


            maintenance_rows.append({

                "Damage":
                    damage_name,

                "Severity":
                    record[3],

                "Priority Score":
                    round(record[6], 2),

                "Priority":
                    record[7],

                "Latitude":
                    record[4],

                "Longitude":
                    record[5],

                "Status":
                    record[8]
            })


        maintenance_data = pd.DataFrame(
            maintenance_rows
        )


        # ----------------------------------------------------
        # Display maintenance table
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Maintenance Priority List'
            '</div>',
            unsafe_allow_html=True
        )


        st.dataframe(
            maintenance_data,
            width="stretch",
            hide_index=True
        )


        # ----------------------------------------------------
        # Maintenance summary
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Maintenance Summary'
            '</div>',
            unsafe_allow_html=True
        )


        col1, col2, col3 = st.columns(3)


        pending_count = sum(
            1 for record in records
            if record[8] == "Pending"
        )


        high_count = sum(
            1 for record in records
            if record[7] == "HIGH"
        )


        critical_count = sum(
            1 for record in records
            if record[7] == "CRITICAL"
        )


        with col1:

            st.metric(
                "Pending Repairs",
                pending_count
            )


        with col2:

            st.metric(
                "High Priority",
                high_count
            )


        with col3:

            st.metric(
                "Critical Issues",
                critical_count
            )


    else:

        st.info(
            "No maintenance records are available yet. "
            "Run an image through the Detect Damage page first."
        )
# ============================================================
# ANALYTICS
# ============================================================

# ============================================================
# ANALYTICS
# ============================================================

elif page == "📈 Analytics":

    st.markdown(
        '<div class="main-title">'
        'Road Damage Analytics'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Analyze road damage patterns and maintenance requirements.'
        '</div>',
        unsafe_allow_html=True
    )

    # Get real records from database
    records = get_damage_records()

    # Create two columns for the charts
    col1, col2 = st.columns(2)

    # ========================================================
    # DAMAGE TYPES
    # ========================================================

    with col1:

        st.markdown(
            '<div class="section-title">'
            'Damage Types'
            '</div>',
            unsafe_allow_html=True
        )

        damage_counts = {
            "D00": 0,
            "D10": 0,
            "D20": 0,
            "D40": 0
        }

        for record in records:

            damage_type = record[0]

            if damage_type in damage_counts:
                damage_counts[damage_type] += 1

        damage_names = {
            "D00": "Longitudinal Crack",
            "D10": "Transverse Crack",
            "D20": "Alligator Crack",
            "D40": "Pothole"
        }

        damage_data = pd.DataFrame({
            "Damage Type": [
                damage_names["D00"],
                damage_names["D10"],
                damage_names["D20"],
                damage_names["D40"]
            ],

            "Count": [
                damage_counts["D00"],
                damage_counts["D10"],
                damage_counts["D20"],
                damage_counts["D40"]
            ]
        })

        st.bar_chart(
            damage_data.set_index("Damage Type")
        )


    # ========================================================
    # SEVERITY
    # ========================================================

    with col2:

        st.markdown(
            '<div class="section-title">'
            'Severity'
            '</div>',
            unsafe_allow_html=True
        )

        severity_counts = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0
        }

        for record in records:

            severity_level = record[3]

            if severity_level in severity_counts:
                severity_counts[severity_level] += 1

        severity_data = pd.DataFrame({
            "Severity": [
                "Critical",
                "High",
                "Medium",
                "Low"
            ],

            "Count": [
                severity_counts["CRITICAL"],
                severity_counts["HIGH"],
                severity_counts["MEDIUM"],
                severity_counts["LOW"]
            ]
        })

        st.bar_chart(
            severity_data.set_index("Severity")
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "RoadVision • AI-based Road Damage Detection & "
    "Maintenance Priority System"
)