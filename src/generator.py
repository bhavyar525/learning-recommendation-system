import os
import random
import numpy as np
import pandas as pd

def generate_synthetic_data(seed=20261022, num_learners=1000, num_skills=50, num_content=200, num_attempts=50000):
    """
    Generates synthetic data matching the educational recommendation problem statement.
    """
    np.random.seed(seed)
    random.seed(seed)
    
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/ground_truth", exist_ok=True)
    
    print("Step 1 & 3: Initializing Master Data & Deterministic IDs...")
    
    # 1. Learners (Using uppercase 'D' for days)
    learner_ids = [f"LRN-{i:06d}" for i in range(1, num_learners + 1)]
    learners_df = pd.DataFrame({
        "learner_id": learner_ids,
        "signup_date": pd.to_datetime("2025-01-01") + pd.to_timedelta(np.random.randint(0, 300, num_learners), unit="D"),
        "status": np.random.choice(["Active", "Inactive", "Cold-Start"], size=num_learners, p=[0.7, 0.2, 0.1])
    })
    
    # 2. Courses
    courses = [{"course_id": f"CRS-{i:06d}", "course_name": f"Course_{i}", "difficulty": random.choice(["Beginner", "Intermediate", "Advanced"])} for i in range(1, 11)]
    courses_df = pd.DataFrame(courses)

    # 3. Skills & Prerequisites
    skill_ids = [f"SKL-{i:06d}" for i in range(1, num_skills + 1)]
    skills_df = pd.DataFrame({
        "skill_id": skill_ids,
        "skill_name": [f"Skill_{i}" for i in range(1, num_skills + 1)],
        "base_difficulty": np.random.choice([1, 2, 3], size=num_skills)
    })
    
    prereqs = []
    for i in range(10, num_skills):
        parent = random.choice(skill_ids[:i])
        prereqs.append({"skill_id": skill_ids[i], "prerequisite_skill_id": parent})
    prereqs_df = pd.DataFrame(prereqs)

    # 4. Content Items
    content_ids = [f"CNT-{i:06d}" for i in range(1, num_content + 1)]
    content_df = pd.DataFrame({
        "content_id": content_ids,
        "skill_id": np.random.choice(skill_ids, size=num_content),
        "format": np.random.choice(["Video", "Quiz", "Reading", "Lab"], size=num_content),
        "difficulty_level": np.random.choice([1, 2, 3], size=num_content)
    })

    print("Step 2 & 4: Generating Transactional/Event Data (Attempts & Results)...")
    
    # 5. Attempts & Assessment Results (Using uppercase 'D' for days)
    attempts = []
    for i in range(num_attempts):
        l_id = random.choice(learner_ids)
        c_id = random.choice(content_ids)
        att_id = f"ATT-{l_id}-{i:05d}"
        
        timestamp = pd.to_datetime("2025-06-01") + pd.to_timedelta(np.random.randint(0, 180), unit="D")
        score = float(np.clip(np.random.normal(70, 20), 0, 100))
        passed = score >= 60.0
        
        attempts.append({
            "attempt_id": att_id,
            "learner_id": l_id,
            "content_id": c_id,
            "timestamp": timestamp,
            "score": round(score, 2),
            "status": "Passed" if passed else "Failed"
        })

    attempts_df = pd.DataFrame(attempts)

    print("Step 5: Injecting Labelled Edge Cases / Negative Scenarios...")
    anomalies = []
    
    anomalies.append({
        "anomaly_id": "ANO-001",
        "type": "Prerequisite_Violation",
        "description": "Recommended advanced skill without completing prerequisite.",
        "entity_id": "LRN-000001",
        "ground_truth_label": "Invalid_Recommendation"
    })

    if not attempts_df.empty:
        attempts_df.loc[0, "timestamp"] = attempts_df.loc[10, "timestamp"] + pd.Timedelta(days=5)
        anomalies.append({
            "anomaly_id": "ANO-002",
            "type": "Invalid_Timestamp_Order",
            "description": "Attempt timestamp occurs out of sequence.",
            "entity_id": attempts_df.loc[0, "attempt_id"],
            "ground_truth_label": "Temporal_Error"
        })

    content_df.loc[0, "skill_id"] = "SKL-999999"
    anomalies.append({
        "anomaly_id": "ANO-003",
        "type": "Orphaned_Content_Skill",
        "description": "Content item references a non-existent skill ID.",
        "entity_id": content_df.loc[0, "content_id"],
        "ground_truth_label": "Integrity_Violation"
    })

    ground_truth_df = pd.DataFrame(anomalies)

    print("Step 9: Exporting to CSV files...")
    learners_df.to_csv("data/raw/learners.csv", index=False)
    courses_df.to_csv("data/raw/courses.csv", index=False)
    skills_df.to_csv("data/raw/skills.csv", index=False)
    prereqs_df.to_csv("data/raw/skill_prerequisites.csv", index=False)
    content_df.to_csv("data/raw/content_items.csv", index=False)
    attempts_df.to_csv("data/raw/attempts.csv", index=False)
    ground_truth_df.to_csv("data/ground_truth/ground_truth_anomalies.csv", index=False)
    
    print("Data Generation Complete. Files saved in /data/")

if __name__ == "__main__":
    generate_synthetic_data()