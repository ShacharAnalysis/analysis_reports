import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cybersecurity Threats Dashboard")
st.title("Global Cybersecurity Threats (2015–2024)")

# Sidebar file uploader
st.sidebar.header("Upload your dataset")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])

@st.cache_data
def load_data(file):
    df = pd.read_csv(file)
    # Clean column names if needed
    df.columns = df.columns.str.strip()
    return df

if uploaded_file:
    df = load_data(uploaded_file)

    # Sidebar filters
    st.sidebar.header("Filter Data")
    years = st.sidebar.multiselect("Select Year(s)", sorted(df['Year'].unique()), default=sorted(df['Year'].unique()))
    countries = st.sidebar.multiselect("Select Country(ies)", sorted(df['Country'].unique()), default=sorted(df['Country'].unique()))

    filtered_df = df[df['Year'].isin(years) & df['Country'].isin(countries)]

    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Incidents", len(filtered_df))
    col2.metric("Total Financial Loss (Million $)", f"{filtered_df['Financial Loss (in Million $)'].sum():,.2f}")
    col3.metric("Total Affected Users", f"{filtered_df['Number of Affected Users'].sum():,}")
    col4.metric("Avg Resolution Time (hrs)", f"{filtered_df['Incident Resolution Time (in Hours)'].mean():.1f}")

    st.markdown("---")

    # 1. Trend over Years
    st.subheader("Yearly Trends")
    yearly_trend = filtered_df.groupby('Year').agg({
        'Financial Loss (in Million $)': 'sum',
        'Number of Affected Users': 'sum',
        'Incident Resolution Time (in Hours)': 'mean'
    }).reset_index()

    col1, col2 = st.columns(2)
    fig1 = px.line(yearly_trend, x='Year', y='Financial Loss (in Million $)', title='Yearly Financial Loss')
    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.line(yearly_trend, x='Year', y='Number of Affected Users', title='Yearly Affected Users')
    col2.plotly_chart(fig2, use_container_width=True)

    st.markdown("**Observations:**\n" +
        "- Financial losses vary significantly across years, suggesting alternating periods of intense and moderate threat levels.\n" +
        "- Affected users show a general increasing trend, indicating rising cyber exposure globally.\n")

    # 2. Attack Types
    st.subheader("Attack Types Overview")
    attack_counts = filtered_df['Attack Type'].value_counts().reset_index()
    attack_counts.columns = ['Attack Type', 'Count']
    fig3 = px.bar(attack_counts, x='Attack Type', y='Count', title='Most Common Attack Types', color='Count')
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("**Observations:**\n" +
        "- Phishing and ransomware are the most frequent attacks, reflecting continued focus on financial gain and user manipulation.\n" +
        "- Other emerging threats suggest a diversification in attack strategies.\n")

    # 3. Country-level Breakdown
    st.subheader("Top Affected Countries")
    country_loss = filtered_df.groupby('Country')["Financial Loss (in Million $)"].sum().sort_values(ascending=False).reset_index()
    fig4 = px.bar(country_loss.head(10), x='Country', y='Financial Loss (in Million $)', color='Financial Loss (in Million $)', title='Top 10 Countries by Financial Loss')
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("**Observations:**\n" +
        "- Countries with higher digital infrastructure face larger financial losses.\n" +
        "- The disparity between countries suggests unequal cyber resilience capabilities.\n")

    # 4. Vulnerability Types
    st.subheader("Vulnerability Types")
    vuln_counts = filtered_df['Security Vulnerability Type'].value_counts().reset_index()
    vuln_counts.columns = ['Vulnerability Type', 'Count']
    fig5 = px.pie(vuln_counts, names='Vulnerability Type', values='Count', title='Distribution of Vulnerability Types')
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("**Observations:**\n" +
        "- Weak credentials and outdated software remain leading vulnerabilities.\n" +
        "- Addressing basic security hygiene could significantly reduce threat exposure.\n")

    # 5. Resolution Time by Defense
    st.subheader("Defense Mechanisms vs. Resolution Time")
    defense_time = filtered_df.groupby('Defense Mechanism Used')["Incident Resolution Time (in Hours)"].mean().sort_values().reset_index()
    fig6 = px.bar(defense_time, x='Defense Mechanism Used', y='Incident Resolution Time (in Hours)', title='Avg Resolution Time by Defense Mechanism', color='Incident Resolution Time (in Hours)')
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("**Observations:**\n" +
        "- Automated defenses resolve threats faster than manual or reactive ones.\n" +
        "- Proactive strategies show potential to reduce incident response time.\n")

    st.markdown("---")
    st.caption("Data source: Uploaded Cybersecurity Dataset (2015–2024)")

else:
    st.warning("Please upload the dataset CSV file to start the analysis.")
