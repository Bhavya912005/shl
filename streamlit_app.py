import streamlit as st
import requests
import pandas as pd

# 👉 Replace this with your actual Render API URL
API_URL = "https://oa-recommendation.onrender.com/docs"

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")

st.title("🔍 SHL Assessment Recommender")
st.markdown("Enter a job description or hiring query to get relevant SHL assessments.")

query = st.text_area("Job description or query", height=200, placeholder="e.g. Hiring for a frontend developer with good communication skills. Assessment should be under 40 minutes and support remote testing.")

if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("Please enter a query first.")
    else:
        with st.spinner("Fetching recommendations..."):
            try:
                response = requests.post(API_URL, json={"query": query})
                if response.status_code == 200:
                    data = response.json()
                    if "message" in data:
                        st.info(data["message"])
                    elif isinstance(data, list) and data:
                        df = pd.DataFrame(data)
                        df = df.rename(columns={
                            "name": "Assessment Name",
                            "url": "Link",
                            "remote_support": "Remote?",
                            "adaptive_support": "Adaptive?",
                            "duration_minutes": "Duration (mins)",
                            "type": "Type"
                        })
                        st.success(f"Found {len(df)} assessment(s):")
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No assessments found.")
                else:
                    st.error(f"API returned status code {response.status_code}")
            except Exception as e:
                st.error(f"Error: {e}")
