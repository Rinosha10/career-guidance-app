import pandas as pd
from collections import Counter

# Load cleaned dataset
df = pd.read_csv("roles_clean.csv")

print("✅ roles_clean.csv loaded")
print(f"Total records: {len(df)}")
print(f"Unique job titles: {df['title'].nunique()}")

# 1. Top 10 job titles
top_titles = df['title'].value_counts().head(10)
print("\n🔝 Top 10 Job Titles:\n", top_titles)

# 2. Most common skills
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
print("\n🛠️ Top 20 Skills:\n", skill_counts)

# 3. Avg description length
df["desc_len"] = df["description"].astype(str).apply(lambda x: len(x.split()))
avg_len = df["desc_len"].mean()
print(f"\n📖 Average job description length: {avg_len:.2f} words")
