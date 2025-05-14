import streamlit as st

st.set_page_config(
    page_title="Report Hub",
    page_icon="📈",
)

st.write("# Welcome to my Streamlit Report Hub!")

st.sidebar.success("Select a report to view above.")

st.markdown(
    """
    Hello and welcome! my name is Shachar Atsami and I'm a **Data Analyst** with a deep passion for uncovering insights 
    and telling stories through data. This app is part of a **personal project** designed 
    to showcase both my analytical skills and my enthusiasm for exploring interesting datasets.

    The app is built using **[Streamlit](https://streamlit.io/)** and is publicly accessible, 
    so feel free to explore, share, and interact!

    ## 📊 Available Reports

    - **Students vs Performance**  
      Dive into an analysis of student habits and their correlation with academic performance. 
      We explore how factors like study time, parental education, and internet access relate 
      to student outcomes.

    *(More reports coming soon!)*

    ---

    Thank you for visiting — I hope you find the analyses insightful and engaging!
    """
)
