import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

# Load dataset
df = pd.read_csv("roles_clean.csv")

# ---- Top 10 Job Titles ----
top_titles = df['title'].value_counts().head(10)

plt.figure(figsize=(10,6))
top_titles.plot(kind="bar", color="skyblue", edgecolor="black")
plt.title("Top 10 Job Titles", fontsize=16)
plt.xlabel("Job Title")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("top_job_titles.png")
plt.show()

# ---- Top 20 Skills ----
all_skills = []
for col in ["required_skills", "desired_skills"]:
    df[col] = df[col].astype(str)
    for skills in df[col]:
        if skills and skills != "nan":
            for s in skills.strip("[]").replace("'", "").split(","):
                skill = s.strip().lower()
                if skill:
                    all_skills.append(skill)

skill_counts = Counter(all_skills).most_common(20)
skills, counts = zip(*skill_counts)

plt.figure(figsize=(10,6))
plt.barh(skills[::-1], counts[::-1], color="lightgreen", edgecolor="black")
plt.title("Top 20 Skills", fontsize=16)
plt.xlabel("Frequency")
plt.tight_layout()
plt.savefig("top_skills.png")
plt.show()
