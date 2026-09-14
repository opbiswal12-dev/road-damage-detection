# Road Damage Detection and Maintenance Priority System

## 📌 Project Overview

The **Road Damage Detection and Maintenance Priority System** is an AI-based application designed to detect and classify road damage from road images and help prioritize road maintenance.

The system uses a **YOLO-based deep learning model** trained on the RDD2022 road damage dataset to identify different types of road damage. After detection, the system estimates damage severity, calculates a maintenance priority score, stores the information in a database, and presents the results through an interactive Streamlit dashboard.

## 🎯 Objectives

* Automatically detect road damage from images.
* Classify detected damage into different categories.
* Estimate the severity of each detected damage.
* Calculate a maintenance priority score.
* Store detected road damage records.
* Display damage locations on a map.
* Provide maintenance and analytics information through a dashboard.

## 🚧 Damage Classes

The current model detects four types of road damage:

| Class | Damage Type        |
| ----- | ------------------ |
| D00   | Longitudinal Crack |
| D10   | Transverse Crack   |
| D20   | Alligator Crack    |
| D40   | Pothole            |

## 🧠 Technologies Used

* Python
* YOLO / Ultralytics
* PyTorch
* Streamlit
* Pandas
* SQLite
* Google Colab
* OpenCV / Computer Vision concepts

## 🔄 System Workflow

```text
Road Image
    ↓
YOLO Object Detection
    ↓
Damage Classification
    ↓
Severity Estimation
    ↓
GPS / Location Information
    ↓
Maintenance Priority Calculation
    ↓
SQLite Database
    ↓
Streamlit Dashboard
    ↓
Maintenance & Analytics
```

## 📊 Severity Estimation

The prototype estimates severity using three factors:

* Damage type
* Detected damage size
* Model confidence

The current prototype uses the following weighted formula:

```text
Severity Score =
0.40 × Damage Type Score
+ 0.40 × Size Score
+ 0.20 × Confidence Score
```

The resulting score is categorized as:

* LOW
* MEDIUM
* HIGH
* CRITICAL

> Note: The current severity calculation is a project prototype/heuristic and is not an official civil-engineering road assessment standard.

## ⭐ Maintenance Priority

The maintenance priority score combines:

* Damage severity
* Road importance
* Traffic level
* Location risk

The current prototype uses:

```text
Priority Score =
0.40 × Severity Score
+ 0.25 × Road Importance
+ 0.20 × Traffic Level
+ 0.15 × Location Risk
```

Priority levels are:

* LOW
* MEDIUM
* HIGH
* CRITICAL

## 📍 Location

The system stores latitude, longitude, and timestamp information with detected road damage records.

The current prototype uses a demonstration GPS location. Integration with real device GPS can be added in a future version.

## 🗄️ Database

The application uses **SQLite** to store road damage records, including:

* Damage type
* Confidence
* Severity score
* Severity level
* Latitude
* Longitude
* Timestamp
* Road importance
* Traffic level
* Location risk
* Priority score
* Priority level
* Maintenance status

## 📈 Streamlit Dashboard

The application currently contains:

### Dashboard

Displays:

* Total detections
* High-priority issues
* Pending repairs
* Critical issues
* Priority overview
* Recent damage reports

### Detect Damage

Allows the user to:

1. Upload a road image.
2. Run the trained YOLO model.
3. View detected road damage.
4. View confidence values.
5. Calculate severity.
6. Calculate maintenance priority.
7. Save the detection to the database.

### Locations

Displays detected road damage locations on a map and provides location information in a table.

### Maintenance

Displays detected road damage records with severity, priority, location, and maintenance status.

### Analytics

Provides charts and summaries for:

* Damage types
* Severity levels
* Priority levels

## 📁 Project Structure

```text
road damage detection/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── dataset/
│   ├── train/
│   ├── val/
│   ├── test/
│   └── data.yaml
│
├── models/
│   └── best.pt
│
├── src/
│   ├── severity.py
│   ├── gps.py
│   ├── priority.py
│   ├── database.py
│   └── ...
│
├── data/
│   └── road_damage.db
│
└── venv/
```

> The `dataset/`, `venv/`, and training output directories are excluded from GitHub using `.gitignore`.

## 📚 Dataset

The project uses the **RDD2022 (Road Damage Dataset 2022)** in YOLO format.

The dataset contains road images collected from multiple countries and includes annotations for different types of road damage.

The dataset used for model training contains four classes:

* Longitudinal Crack
* Transverse Crack
* Alligator Crack
* Pothole

Dataset license: **CC BY-SA 4.0**

## 🤖 Model

The project uses a **YOLO11n** object detection model fine-tuned on the RDD2022 dataset.

The trained model is stored as:

```text
models/best.pt
```

The current prototype model was trained using Google Colab with a Tesla T4 GPU.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_LINK>
```

### 2. Open the project

```bash
cd "road damage detection"
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

On Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

Run:

```bash
streamlit run app.py
```

The Streamlit application will open in your browser.

## ⚠️ Current Limitations

The current version is a working prototype. Some components use simplified or demonstration values.

Future
