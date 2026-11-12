# Cloud Data Engineering & Learning Recommendation Pipeline

## Business Context / Problem
Recommend next learning activities based on skills, prerequisites, assessment results, and content difficulty.

## Architecture & Tech Stack
- **Language:** Python
- **Data Processing:** Pandas, NumPy
- **Storage/Format:** CSV (Raw and Structured layers)
- **Design Patterns:** Metadata-driven generation, event-history retention, separate ground-truth anomaly catalog.

## Project Structure
```text
learning_recommendation_pipeline/
├── data/
│   ├── raw/                 # Generated master and transaction CSVs
│   └── ground_truth/        # Injected anomaly and label files
├── src/
│   ├── __init__.py
│   ├── generator.py         # Synthetic data generation script
│   └── validator.py         # Integrity and constraint validator
├── requirements.txt         # Dependencies list
└── README.md                # Project documentation

## How to Run the UI
1. Install requirements: `pip install -r requirements.txt`
2. Launch the dashboard: `streamlit run app.py`
3. Open your browser at: `http://localhost:8501`