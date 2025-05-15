import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("studens_vs_performance/Global_Cybersecurity_Threats_2015-2024.csv")

st.set_page_config(page_title="Cybersecurity Threats Dashboard", layout="wide", page_icon="🔒")
st.title("\U0001F512 Global Cybersecurity Threats (2015–2024)")

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

# 2. Attack Types
st.subheader("Attack Types Overview")
attack_counts = filtered_df['Attack Type'].value_counts().reset_index()
attack_counts.columns = ['Attack Type', 'Count']
fig3 = px.bar(attack_counts, x='Attack Type', y='Count', title='Most Common Attack Types', color='Count')
st.plotly_chart(fig3, use_container_width=True)

# 3. Country-level Breakdown
st.subheader("Top Affected Countries")
country_loss = filtered_df.groupby('Country')["Financial Loss (in Million $)"].sum().sort_values(ascending=False).reset_index()
fig4 = px.bar(country_loss.head(10), x='Country', y='Financial Loss (in Million $)', color='Financial Loss (in Million $)', title='Top 10 Countries by Financial Loss')
st.plotly_chart(fig4, use_container_width=True)

# 4. Vulnerability Types
st.subheader("Vulnerability Types")
vuln_counts = filtered_df['Security Vulnerability Type'].value_counts().reset_index()
vuln_counts.columns = ['Vulnerability Type', 'Count']
fig5 = px.pie(vuln_counts, names='Vulnerability Type', values='Count', title='Distribution of Vulnerability Types')
st.plotly_chart(fig5, use_container_width=True)

# 5. Resolution Time by Defense
st.subheader("Defense Mechanisms vs. Resolution Time")
defense_time = filtered_df.groupby('Defense Mechanism Used')["Incident Resolution Time (in Hours)"].mean().sort_values().reset_index()
fig6 = px.bar(defense_time, x='Defense Mechanism Used', y='Incident Resolution Time (in Hours)', title='Avg Resolution Time by Defense Mechanism', color='Incident Resolution Time (in Hours)')
st.plotly_chart(fig6, use_container_width=True)


st.markdown("**Observations:**\n" +
    "- Yearly Trends\n" +
    "* Peaks in financial loss often correlate with global-scale attacks or new malware variants.\n" +
    "* Sudden drops may indicate improved regulation, awareness campaigns, or underreporting.\n" +
    "- Attack Types\n" +
    "* The rise in social engineering attacks suggests increasing exploitation of human factors.\n" +
    "* Emerging attacks like supply chain or zero-day exploits, though less frequent, may carry high impact.\n" +
    "- Country-level Breakdown\n" +
    "* Economically developed nations bear higher losses, possibly due to more valuable targets and data.\n" +
    "* Regional clusters of high loss may indicate geopolitical targeting or regional vulnerabilities.\n" +
    "- Vulnerability Types\n" +
    "* Persistent high counts for basic issues (e.g., weak passwords) reveal gaps in user education and enforcement.\n" +
    "* Less frequent but severe vulnerabilities (e.g., zero-day flaws) point to the need for rapid patching processes.\n" +
    "- Defense Mechanisms\n" +
    "* AI-based defenses and intrusion detection systems tend to lower resolution time significantly.\n" +
    "* Countries or organizations relying heavily on manual defense methods may experience slower recovery and higher damages.\n"
)

st.markdown("---")
st.caption("Data source: Simulated Cybersecurity Dataset (2015–2024)")
