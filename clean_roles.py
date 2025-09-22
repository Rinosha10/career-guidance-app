import pandas as pd
import re

# 1. Load merged dataset
df = pd.read_csv("roles.csv")

print("✅ Loaded roles.csv")
print(f"Total records: {len(df)}")
print("\nColumns available:", list(df.columns))
print("\nSample data:")
print(df.head(5))

# 2. Basic Cleaning
def clean_text(text):
    if pd.isna(text):
        return ""
    # Lowercase
    text = text.lower()
    # Remove newlines, tabs
    text = re.sub(r"[\n\t\r]", " ", text)
    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Apply cleaning to title & description
df["title"] = df["title"].astype(str).apply(clean_text)
df["description"] = df["description"].astype(str).apply(clean_text)
df["required_skills"] = df["required_skills"].astype(str).apply(clean_text)
df["desired_skills"] = df["desired_skills"].astype(str).apply(clean_text)
df["industry"] = df["industry"].astype(str).apply(clean_text)

# 3. Split skills into lists (if comma-separated)
df["required_skills"] = df["required_skills"].apply(lambda x: [s.strip() for s in x.split(",")] if x else [])
df["desired_skills"] = df["desired_skills"].apply(lambda x: [s.strip() for s in x.split(",")] if x else [])

# 4. Drop duplicates again (if any)
df = df.drop_duplicates(subset=["title", "description"], keep="first")

# 5. Save cleaned dataset
df.to_csv("roles_clean.csv", index=False, encoding="utf-8")

print("\n✅ Cleaning Done!")
print(f"Final dataset saved as roles_clean.csv with {len(df)} records.")
print("\nUnique job titles:", df['title'].nunique())
