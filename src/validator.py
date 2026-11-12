import pandas as pd

def validate_datasets():
    print("Running Validation Checks (Step 8)...")
    
    learners = pd.read_csv("data/raw/learners.csv")
    skills = pd.read_csv("data/raw/skills.csv")
    content = pd.read_csv("data/raw/content_items.csv")
    attempts = pd.read_csv("data/raw/attempts.csv")
    
    # 1. Primary Key Uniqueness
    assert learners["learner_id"].is_unique, "Duplicate Learner IDs found!"
    assert skills["skill_id"].is_unique, "Duplicate Skill IDs found!"
    assert content["content_id"].is_unique, "Duplicate Content IDs found!"
    assert attempts["attempt_id"].is_unique, "Duplicate Attempt IDs found!"
    print("✔ Primary Key Uniqueness Checks Passed.")

    # 2. Foreign Key Integrity Check (accounting for injected anomaly)
    invalid_skills = content[~content["skill_id"].isin(skills["skill_id"])]
    assert len(invalid_skills) == 1, "Injected orphaned content anomaly missing!"
    print("✔ Foreign Key Integrity & Anomaly Capture Checks Passed.")

    print("All validation criteria successfully evaluated.")

if __name__ == "__main__":
    validate_datasets()