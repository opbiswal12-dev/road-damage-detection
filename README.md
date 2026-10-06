# 🛣️ RoadVision: AI-Based Road Damage Detection & Maintenance Priority System

## 📌 Project Overview

**RoadVision** is a production-ready AI application that detects and classifies road damage from images, estimates severity, and calculates maintenance priorities. It combines computer vision with data analytics to help road agencies optimize maintenance workflows.

The system uses a **YOLO11n deep learning model** trained on the RDD2022 (Road Damage Dataset 2022) to identify four types of road damage and provides an interactive Streamlit dashboard for visualization and management.

---

## 🎯 Key Features

✅ **Automatic road damage detection** from uploaded images  
✅ **Multi-class damage classification** (4 damage types)  
✅ **Severity estimation** based on damage type, size, and detection confidence  
✅ **Maintenance priority calculation** considering road importance and traffic  
✅ **Interactive Streamlit dashboard** with real-time analytics  
✅ **SQLite database** for persistent storage and tracking  
✅ **Map visualization** of damage locations  
✅ **Maintenance status management** (Pending, In Progress, Completed)  

---

## 🚧 Supported Damage Classes

| Code | Damage Type          | Description                           |
|------|----------------------|---------------------------------------|
| D00  | Longitudinal Crack   | Cracks running parallel to traffic   |
| D10  | Transverse Crack     | Cracks running perpendicular to traffic |
| D20  | Alligator Crack      | Interconnected network of cracks    |
| D40  | Pothole              | Localized loss of pavement material  |

---

## 🧠 Technology Stack

- **Backend**: Python 3.8+
- **UI Framework**: Streamlit
- **Computer Vision**: YOLO11n (Ultralytics)
- **Deep Learning**: PyTorch
- **Database**: SQLite3
- **Data Processing**: Pandas, NumPy
- **Image Processing**: OpenCV

---

## 📊 Scoring & Prioritization

### Severity Estimation

Severity combines three factors:

```
Severity Score = 
  0.40 × Damage Type Score +
  0.40 × Size Score +
  0.20 × Confidence Score
```

**Levels**: LOW (≤25) → MEDIUM (≤50) → HIGH (≤75) → CRITICAL (>75)

### Maintenance Priority

Priority is calculated from:

```
Priority Score = 
  0.40 × Severity Score +
  0.25 × Road Importance +
  0.20 × Traffic Level +
  0.15 × Location Risk
```

**Levels**: LOW (≤25) → MEDIUM (≤50) → HIGH (≤75) → CRITICAL (>75)

> **Note**: Current scoring is a prototype heuristic, not a certified civil-engineering standard.

---

## 📁 Project Structure

```
road-damage-detection/
│
├── app.py                      # Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
│
├── .streamlit/
│   └── config.toml            # Streamlit configuration
│
├── src/
│   ├── __init__.py
│   ├── database.py            # SQLite operations
│   ├── severity.py            # Severity scoring
│   ├── priority.py            # Priority calculation
│   └── gps.py                 # Location helpers
│
├── models/
│   └── best.pt                # Trained YOLO model
│
├── data/
│   └── road_damage.db         # SQLite database (auto-created)
│
└── venv/                       # Virtual environment (excluded)
```

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Git
- 500MB+ disk space for model and data

### Step-by-Step Setup

#### 1. Clone the repository

```bash
git clone https://github.com/opbiswal12-dev/road-damage-detection.git
cd road-damage-detection
```

#### 2. Create a virtual environment

**Windows (PowerShell):**
```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Initialize the database

```bash
python -m src.database
```

This creates `data/road_damage.db` automatically.

#### 5. Run the application

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## 📖 Usage Guide

### Dashboard

**Metrics Overview:**
- Total detections recorded
- High-priority issues requiring attention
- Pending repairs awaiting maintenance
- Critical issues needing immediate action

**Visualizations:**
- Priority distribution chart
- Recent damage reports table
- System summary and status

### Detect Damage

1. **Upload** a road image (JPG, PNG, JPEG)
2. **Adjust settings**:
   - Road Importance (0-100)
   - Traffic Level (0-100)
   - Location Risk (0-100)
3. **Click** "Analyze Image"
4. **Review** detected damage with bounding boxes
5. **Records auto-save** to the database

### Locations

- **Interactive map** showing all detected damage locations
- **Location table** with coordinates and priority levels
- **Zoom controls** for detailed area inspection

### Maintenance

- **Damage inventory** with severity and priority scores
- **Status management**: Pending → In Progress → Completed
- **Bulk viewing** of all repairs with location and severity

### Analytics

- **Damage type distribution** (which damages are most common)
- **Severity breakdown** (how severe are detected damages)
- **Priority overview** (which repairs are most urgent)

---

## 📊 Database Schema

```sql
CREATE TABLE road_damage (
    damage_id INTEGER PRIMARY KEY AUTOINCREMENT,
    damage_type TEXT NOT NULL,              -- D00, D10, D20, D40
    confidence REAL NOT NULL,               -- 0.0 to 1.0
    severity_score REAL NOT NULL,           -- 0 to 100
    severity_level TEXT NOT NULL,           -- LOW, MEDIUM, HIGH, CRITICAL
    latitude REAL,
    longitude REAL,
    timestamp TEXT NOT NULL,                -- ISO 8601 format
    road_importance REAL NOT NULL,          -- 0 to 100
    traffic_level REAL NOT NULL,            -- 0 to 100
    location_risk REAL NOT NULL,            -- 0 to 100
    priority_score REAL NOT NULL,           -- 0 to 100
    priority_level TEXT NOT NULL,           -- LOW, MEDIUM, HIGH, CRITICAL
    status TEXT NOT NULL DEFAULT 'Pending'  -- Pending, In Progress, Completed
);
```

---

## 🔄 System Workflow

```
┌─────────────────────┐
│  Road Image Upload  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ YOLO Object         │
│ Detection           │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Extract Damage Type │
│ & Confidence Score  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Calculate Severity  │
│ (type + size + conf)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Calculate Priority  │
│ (severity + road +  │
│  traffic + location)│
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Save to SQLite      │
│ Database            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Display in          │
│ Dashboard           │
└─────────────────────┘
```

---

## 📚 Dataset Information

**RDD2022 (Road Damage Dataset 2022)**
- Multi-country road damage imagery
- 4 damage classes with YOLO format annotations
- License: CC BY-SA 4.0
- Used for model training on Google Colab (Tesla T4 GPU)

---

## 🤖 Model Details

**Architecture**: YOLO11n (Nano variant)
- Lightweight and fast
- Suitable for real-time detection
- Pre-trained on COCO, fine-tuned on RDD2022

**Model File**: `models/best.pt` (~6-10 MB)

**Performance**:
- Inference speed: ~50-100ms per image
- Compatible with CPU and GPU devices

---

## ⚙️ Configuration

Customize the app behavior by editing `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#0066cc"
backgroundColor = "#0f172a"
secondaryBackgroundColor = "#1e293b"
textColor = "#e2e8f0"

[client]
showErrorDetails = false

[server]
port = 8501
headless = true
```

---

## 🚀 Deployment

### Local Development

```bash
streamlit run app.py
```

### Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Select `app.py` as the entry point
5. Deploy!

### Docker

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

## 🔮 Future Enhancements

- [ ] Real device GPS integration (mobile/vehicle sensors)
- [ ] Photo metadata extraction (EXIF timestamp & location)
- [ ] Export reports (PDF, CSV, GeoJSON)
- [ ] Multi-model ensemble for higher accuracy
- [ ] Image annotation tools for dataset expansion
- [ ] API endpoint for programmatic access
- [ ] Cost estimation for repairs
- [ ] Historical trend analysis
- [ ] Road network optimization algorithms
- [ ] Mobile app for fieldwork

---

## ⚠️ Current Limitations

- **GPS**: Uses demonstration coordinates (can be integrated with real device location)
- **Database**: SQLite suitable for single-user; upgrade to PostgreSQL for team use
- **Severity**: Heuristic-based; not a certified civil engineering assessment
- **Model**: Trained on RDD2022 dataset; may require fine-tuning for other regions
- **Batch**: Processes one image at a time; doesn't support batch uploads yet

---

## 📄 License

This project is licensed under the **MIT License**. See LICENSE file for details.

Dataset license: **CC BY-SA 4.0**

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Support & Contact

**Author**: Om Prasad Biswal  
**GitHub**: [@opbiswal12-dev](https://github.com/opbiswal12-dev)  
**Email**: opbiswal12@gmail.com  
**LinkedIn**: [om-prasad-biswal](https://linkedin.com/in/om-prasad-biswal)

---

## 🙏 Acknowledgments

- **Ultralytics** for YOLO framework
- **RDD2022 Dataset** creators and contributors
- **Streamlit** for the web framework
- **PyTorch** for deep learning infrastructure

---

## 📊 Project Stats

- **Lines of Code**: ~1000+
- **Supported Damage Classes**: 4
- **Database Records**: Unlimited (scalable)
- **Map Precision**: GPS coordinates (latitude, longitude)
- **Detection Speed**: ~50-100ms per image
- **Model Size**: ~6-10 MB

---

## 🎓 Learning Resources

- [YOLO Documentation](https://docs.ultralytics.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SQLite Tutorial](https://www.sqlite.org/)
- [Road Damage Dataset](https://github.com/sekilab/RDD2022)

---

**Last Updated**: September 2026  
**Status**: Production Ready ✅
