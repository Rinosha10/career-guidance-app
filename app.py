import streamlit as st
import pandas as pd
import PyPDF2
import plotly.express as px
from recommend_jobs import recommend_jobs
from io import BytesIO

# ==========================
# App Config
# ==========================
st.set_page_config(
    page_title="🎯 Career Guidance App",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================
# Custom CSS (Light Theme)
# ==========================
st.markdown(
    """
    <style>
    .stApp { background-color: #f9fbfd; }
    h1 { color: #004aad !important; font-weight: 700 !important; }
    section[data-testid="stSidebar"] { background-color: #eaf2fb; }
    div.stButton > button {
        background-color: #004aad; color: white; font-weight: bold; border-radius: 10px;
    }
    div.stButton > button:hover { background-color: #0066cc; color: #ffffff; }
    .stDataFrame { border: 2px solid #004aad; border-radius: 12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================
# Logo & Title
# ==========================
st.image("logo.jpg", width=150)  # 👉 replace with your logo file
st.title("🎯 Smart Job Recommendation System")
st.caption("AI-powered career guidance with resume parsing, skill extraction, and job matching")

# ==========================
# Skill Extractor
# ==========================
with open("skills_list.txt", "r") as f:
    SKILLS_DB = [line.strip().lower() for line in f.readlines() if line.strip()]

def extract_skills_from_text(text):
    text = text.lower()
    found_skills = [skill for skill in SKILLS_DB if skill in text]
    return list(set(found_skills))

def extract_text_from_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# ==========================
# Sidebar Input
# ==========================
st.sidebar.header("⚙️ Input Options")
option = st.sidebar.radio("How do you want to provide your skills?", ("Enter Skills", "Upload Resume"))

user_skills = ""
extracted_skills = []

if option == "Enter Skills":
    user_skills = st.text_area("✍️ Enter your skills (comma separated):", "")
    extracted_skills = [s.strip() for s in user_skills.split(",") if s.strip()]
elif option == "Upload Resume":
    uploaded_file = st.file_uploader("📄 Upload your resume (PDF)", type=["pdf"])
    if uploaded_file:
        resume_text = extract_text_from_pdf(uploaded_file)
        extracted_skills = extract_skills_from_text(resume_text)
        user_skills = ", ".join(extracted_skills)
        st.success(f"✅ Extracted Skills: {user_skills}")

# ==========================
# Main Logic
# ==========================
if st.button("🔍 Recommend Jobs"):
    if user_skills.strip():
        st.subheader("📌 Extracted / Entered Skills")
        st.write(user_skills)

        # ✅ Download extracted skills
        if extracted_skills:
            skills_text = "\n".join(extracted_skills)
            st.download_button(
                label="📥 Download Extracted Skills (TXT)",
                data=skills_text,
                file_name="extracted_skills.txt",
                mime="text/plain",
            )

            # 📊 Skill Demand Chart
            st.subheader("📊 Skill Demand in Job Descriptions")
            roles_df = pd.read_csv("roles_clean.csv")

            demand_counts = {}
            for skill in extracted_skills:
                demand_counts[skill] = roles_df["description"].str.lower().str.contains(skill).sum()

            demand_df = pd.DataFrame(list(demand_counts.items()), columns=["Skill", "Job Count"])
            demand_df = demand_df.sort_values(by="Job Count", ascending=True)

            fig = px.bar(
                demand_df,
                x="Job Count",
                y="Skill",
                orientation="h",
                title="Skill Demand in Dataset",
                labels={"Job Count": "Number of Jobs", "Skill": "Extracted Skills"},
                color="Job Count",
                color_continuous_scale="Blues",
            )

            st.plotly_chart(fig, use_container_width=True)

        # 💼 Job Recommendations
        st.subheader("💼 Top Job Recommendations")
        results = recommend_jobs(user_skills, top_n=20)

        for idx, row in results.head(5).iterrows():
            st.markdown(f"**🔹 {row['title']}**")
            st.write(row["description"][:300] + "...")
            st.caption(f"Similarity Score: {row['similarity']:.2f}")
            st.write("---")

        # 📋 Interactive Recommendations Table
        st.subheader("📋 Interactive Job Recommendations Table")
        results_display = results.rename(columns={"similarity": "Score"})

        search_query = st.text_input("🔍 Search in job titles/descriptions:")
        if search_query:
            results_display = results_display[
                results_display["title"].str.contains(search_query, case=False, na=False) |
                results_display["description"].str.contains(search_query, case=False, na=False)
            ]

        if "industry" in results_display.columns:
            industries = ["All"] + sorted(results_display["industry"].dropna().unique().tolist())
            selected_industry = st.selectbox("🏢 Filter by Industry", industries)
            if selected_industry != "All":
                results_display = results_display[results_display["industry"] == selected_industry]

        st.dataframe(results_display[["title", "description", "Score"]], use_container_width=True, height=400)

        # ✅ Download button
        csv = results_display.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Recommended Jobs (CSV)",
            data=csv,
            file_name="recommended_jobs.csv",
            mime="text/csv",
        )

    else:
        st.warning("⚠️ Please enter skills or upload a resume first.")

# ==========================
# Footer (Step C)
# ==========================
st.markdown(
    """
    <hr>
    <div style="text-align:center; color:gray;">
        © 2025 Career Guidance App | Built with ❤️ using Streamlit  
        <br>
        <a href="https://streamlit.io" target="_blank" style="color:#004aad;">Powered by Streamlit</a>
    </div>
    """,
    unsafe_allow_html=True
)
