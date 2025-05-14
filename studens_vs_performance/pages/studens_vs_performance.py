import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Studens VS Performance Analysis", page_icon="📈")

# Load data from specified path
@st.cache_data
def load_data():
    df = pd.read_csv("AnalysisEssentials/studens_vs_performance/student_habits_performance.csv")
    return df

students_df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Students")
gender = st.sidebar.multiselect("Gender", options=students_df["gender"].unique(), default=students_df["gender"].unique())
part_time = st.sidebar.multiselect("Part-time Job", options=students_df["part_time_job"].unique(), default=students_df["part_time_job"].unique())
age_min, age_max = st.sidebar.slider("Age Range", int(students_df["age"].min()), int(students_df["age"].max()), (int(students_df["age"].min()), int(students_df["age"].max())))
internet_quality = st.sidebar.multiselect("Internet Quality", options=students_df["internet_quality"].unique(), default=students_df["internet_quality"].unique())
mental_health = st.sidebar.slider("Mental Health Rating", int(students_df["mental_health_rating"].min()), int(students_df["mental_health_rating"].max()), (int(students_df["mental_health_rating"].min()), int(students_df["mental_health_rating"].max())))
parental_edu = st.sidebar.multiselect("Parental Education", options=students_df["parental_education_level"].unique(), default=students_df["parental_education_level"].unique())

filtered_df = students_df[
    (students_df["gender"].isin(gender)) &
    (students_df["part_time_job"].isin(part_time)) &
    (students_df["age"] >= age_min) & (students_df["age"] <= age_max) &
    (students_df["internet_quality"].isin(internet_quality)) &
    (students_df["mental_health_rating"] >= mental_health[0]) & (students_df["mental_health_rating"] <= mental_health[1]) &
    (students_df["parental_education_level"].isin(parental_edu))
]

# Main Title
st.title("📊 Student Habits & Performance Dashboard")

# Overview Metrics
st.subheader("Overview Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Average Exam Score", f"{filtered_df['exam_score'].mean():.2f}")
col2.metric("Average Study Hours", f"{filtered_df['study_hours_per_day'].mean():.2f}")
col3.metric("Average Sleep Hours", f"{filtered_df['sleep_hours'].mean():.2f}")

# Scatter Plot
st.subheader("Study Hours vs Exam Score")
fig1 = px.scatter(filtered_df, x="study_hours_per_day", y="exam_score", color="gender",
                  hover_data=["age", "sleep_hours"], trendline="ols")
st.plotly_chart(fig1, use_container_width=True)

# Boxplot by Diet
st.subheader("Exam Score by Diet Quality")
fig2 = px.box(filtered_df, x="diet_quality", y="exam_score", color="diet_quality")
st.plotly_chart(fig2, use_container_width=True)

# Mental Health Impact
st.subheader("Mental Health Rating vs Exam Score")
fig3 = px.scatter(filtered_df, x="mental_health_rating", y="exam_score", color="gender",
                  trendline="ols", size="sleep_hours")
st.plotly_chart(fig3, use_container_width=True)

# NEW: Exam Score by Parental Education
st.subheader("Exam Score by Parental Education Level")
fig4 = px.box(filtered_df, x="parental_education_level", y="exam_score", color="parental_education_level")
st.plotly_chart(fig4, use_container_width=True)

# NEW: Distribution of Sleep Hours
st.subheader("Distribution of Sleep Hours")
fig5 = px.histogram(filtered_df, x="sleep_hours", nbins=20, color="gender")
st.plotly_chart(fig5, use_container_width=True)

# NEW: Internet Quality vs Exam Score
st.subheader("Internet Quality vs Exam Score")
fig6 = px.violin(filtered_df, x="internet_quality", y="exam_score", box=True, color="internet_quality")
st.plotly_chart(fig6, use_container_width=True)

# Notes and Insights
st.markdown("### 📝 Observations")
st.markdown("""
- Students with more **study hours** generally perform better, though outliers exist.
- Better **diet quality** appears linked to higher average scores.
- Higher **mental health ratings** are positively associated with exam scores.
- Students whose parents have **higher education levels** may benefit academically.
- **Internet quality** also seems to have an impact, possibly due to smoother access to resources.
""")


st.markdown("---")
st.markdown(
    """
    This dashboard is part of a personal project to analyze student habits and their impact on academic performance. 
    The data is sourced from an actual dataset created for educational purposes using 1000 test subjects in the USA.
    
    If you have any questions or feedback, feel free to reach out!
    """
)