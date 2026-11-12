# Cloud Data Engineering & Learning Recommendation System

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

Running the Application
1. Install Dependencies
pip install -r requirements.txt

2. Generate Sample Data
Run the synthetic data generator to create learner, skill, and assessment datasets.
python src/generator.py

3. Run Data Validation
Validate data quality and business rules.
python src/validator.py

4. Launch the Streamlit Dashboard
streamlit run app.py

5. Access the Application
Open your browser and navigate to:
http://localhost:8501