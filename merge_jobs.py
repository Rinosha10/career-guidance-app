import os
import pandas as pd

# Path to your folder
folder_path = "."

# Collect all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

print("Files found:", csv_files)  # Debugging

all_dfs = []

for file in csv_files:
    file_path = os.path.join(folder_path, file)
    df = pd.read_csv(file_path, encoding="utf-8", on_bad_lines="skip")

    # Standardize column names
    df.columns = [col.strip().lower() for col in df.columns]

    # Map common column names
    col_map = {
        "job title": "title",
        "role": "title",
        "position": "title",
        "job description": "description",
        "description": "description",
        "skills": "required_skills",
        "required skills": "required_skills",
        "desired skills": "desired_skills"
    }
    df = df.rename(columns={c: col_map.get(c, c) for c in df.columns})

    # Add missing columns if not present
    for col in ["title", "description", "required_skills", "desired_skills", "industry"]:
        if col not in df.columns:
            df[col] = ""

    # Add source column
    df["source"] = file

    # Keep only required columns
    df = df[["title", "description", "required_skills", "desired_skills", "industry", "source"]]

    # Drop empty rows
    df = df.dropna(subset=["title", "description"])

    all_dfs.append(df)

# Merge all
merged_df = pd.concat(all_dfs, ignore_index=True)

# Remove duplicates
merged_df = merged_df.drop_duplicates(subset=["title", "description"], keep="first")

# Add role_id
merged_df.insert(0, "role_id", range(1, len(merged_df) + 1))

# Save to CSV
output_path = os.path.join(folder_path, "roles.csv")
merged_df.to_csv(output_path, index=False, encoding="utf-8")

print(f"✅ Cleaned & merged dataset saved as {output_path}")
print(f"Total roles: {len(merged_df)}")
print(merged_df.head())
