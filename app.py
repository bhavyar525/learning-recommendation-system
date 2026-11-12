import streamlit as st
import pandas as pd
import os
from src.generator import generate_synthetic_data

# Page Config
st.set_page_config(page_title="Learning Recommendation Data Pipeline", layout="wide")

st.title("🎓 Learning Recommendation Data Dashboard")
st.markdown("""
This dashboard manages the **Data Engineering Pipeline** for student learning recommendations.
It handles data generation, validation, and exploration of learner attempts and skill prerequisites.
""")

# Sidebar Navigation
st.sidebar.header("Control Panel")
action = st.sidebar.radio("Navigate to:", ["Project Overview", "Data Generation", "Data Explorer", "Validation Results"])

# --- TAB 1: OVERVIEW ---
if action == "Project Overview":
    st.subheader("Business Context")
    st.write("""
    The goal of this system is to recommend next learning activities based on:
    - **Skills & Prerequisites:** Ensuring students follow a logical path.
    - **Assessment Results:** Tracking past performance.
    - **Content Difficulty:** Matching content to learner mastery.
    """)
    st.info("💡 Use the sidebar to generate data or explore the generated datasets.")

# --- TAB 2: DATA GENERATION ---
elif action == "Data Generation":
    st.subheader("Generate Synthetic Datasets")
    st.write("This will generate 10,000 learners and 500,000 attempts (Scaled down for demo).")
    
    col1, col2 = st.columns(2)
    with col1:
        num_learners = st.number_input("Number of Learners", value=1000)
    with col2:
        num_attempts = st.number_input("Number of Attempts", value=5000)

    if st.button("🚀 Run Pipeline Generator"):
        with st.spinner("Generating data and injecting anomalies..."):
            generate_synthetic_data(num_learners=num_learners, num_attempts=num_attempts)
            st.success("✅ Data generated successfully and saved to /data/raw folder!")

# --- TAB 3: DATA EXPLORER ---
elif action == "Data Explorer":
    st.subheader("Explore Generated Data")
    
    if os.path.exists("data/raw/learners.csv"):
        option = st.selectbox("Select Table to View:", 
                              ["Learners", "Skills", "Content Items", "Attempts", "Ground Truth Anomalies"])
        
        mapping = {
            "Learners": "data/raw/learners.csv",
            "Skills": "data/raw/skills.csv",
            "Content Items": "data/raw/content_items.csv",
            "Attempts": "data/raw/attempts.csv",
            "Ground Truth Anomalies": "data/ground_truth/ground_truth_anomalies.csv"
        }
        
        df = pd.read_csv(mapping[option])
        st.write(f"Showing top rows of {option}")
        st.dataframe(df.head(100), use_container_width=True)
        st.write(f"**Total Records in {option}:** {len(df)}")
    else:
        st.warning("⚠️ No data found. Please run 'Data Generation' first.")

# --- TAB 4: VALIDATION ---
elif action == "Validation Results":
    st.subheader("Data Quality & Integrity Checks")
    
    if os.path.exists("data/raw/learners.csv"):
        learners = pd.read_csv("data/raw/learners.csv")
        skills = pd.read_csv("data/raw/skills.csv")
        content = pd.read_csv("data/raw/content_items.csv")
        
        # Check 1: PK Uniqueness
        if learners["learner_id"].is_unique:
            st.success("✅ Primary Key Uniqueness: PASSED (Learner IDs)")
        else:
            st.error("❌ Primary Key Uniqueness: FAILED")
            
        # Check 2: Orphaned Content
        invalid_skills = content[~content["skill_id"].isin(skills["skill_id"])]
        if len(invalid_skills) > 0:
            st.warning(f"🚩 Found {len(invalid_skills)} record(s) with invalid Skill IDs (Intended Anomaly).")
            st.write(invalid_skills)
            
        # Stats
        st.divider()
        st.metric("Total Learners", len(learners))
        st.metric("Total Skills", len(skills))
    else:
        st.warning("⚠️ No data found. Please run 'Data Generation' first.")