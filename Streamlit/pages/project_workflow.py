import streamlit as st

with st.sidebar:
    st.page_link('main.py', label='Predictor', icon='🏎️')
    st.page_link('pages/project_workflow.py', label='Project Workflow', icon='🚀')

tab1, tab2, tab3 = st.tabs(["Data Collection", "EDA", "ML Modeling"])

with tab1:
    st.title("🔍 Data Collection")

with tab2:
    st.title("📊 EDA")

with tab3:
    st.title("🤖 ML Modeling")