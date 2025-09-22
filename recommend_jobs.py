import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset once
roles_df = pd.read_csv("roles_clean.csv")

def recommend_jobs(student_skills, top_n=5):
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(roles_df["description"].fillna(""))

    query_vec = vectorizer.transform([student_skills])
    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()

    # Get top matches
    indices = similarity.argsort()[-top_n:][::-1]
    results = roles_df.iloc[indices][["title", "description"]].copy()
    results["similarity"] = similarity[indices]

    # ✅ Sort by similarity
    results = results.sort_values(by="similarity", ascending=False)

    return results.reset_index(drop=True)
