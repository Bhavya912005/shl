import streamlit as st
import requests
import pandas as pd

# 🔗 Update this if your API URL changes
API_URL = "https://oa-recommendation.onrender.com/recommend"

st.set_page_config(page_title="SHL Assessment Recommender", layout="wide")

st.title("🔍 SHL Assessment Recommender")
st.markdown(
    "Enter a job description or hiring query below to receive SHL assessment recommendations "
    "based on semantic similarity, duration, and filters like remote/adaptive support."
)

query = st.text_area(
    "Job description or query:",
    height=200,
    placeholder=(
        "e.g. Hiring for a Java developer who collaborates well and can complete an assessment in 40 minutes."
    ),
)

# Always show logs (for debugging deployment)
st.write("✅ Streamlit app loaded.")
st.write("📡 Target API URL:", API_URL)

if st.button("Get Recommendations"):
    if not query.strip():
        st.warning("⚠️ Please enter a query before submitting.")
    else:
        with st.spinner("🔎 Sending query to API..."):
            try:
                response = requests.post(API_URL, json={"query": query}, timeout=75)

                # Show response status and raw text
                st.write("📬 API Status Code:", response.status_code)
                st.write("📨 Raw Response Body:", response.text)

                if response.status_code == 200:
                    data = response.json()

                    if isinstance(data, dict) and "message" in data:
                        st.info(f"ℹ️ {data['message']}")
                    elif isinstance(data, list) and data:
                        df = pd.DataFrame(data)
                        df = df.rename(
                            columns={
                                "name": "Assessment Name",
                                "url": "Link",
                                "remote_support": "Remote?",
                                "adaptive_support": "Adaptive?",
                                "duration_minutes": "Duration (mins)",
                                "type": "Type",
                            }
                        )
                        st.success(f"✅ Found {len(df)} recommended assessment(s):")
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("🔍 No assessments matched the criteria.")
                else:
                    st.error(f"❌ API returned status code {response.status_code}")

            except Exception as e:
                st.error(f"🚨 API call failed: {e}")
