import streamlit as st
import requests

st.set_page_config(page_title="Multi-Agent Research System", layout="wide")
st.title("Multi-Agent Research System")
st.markdown("Enter a topic below to have the AI agents research and write a report.")

topic = st.text_input("Enter research topic:", placeholder="e.g. Recent advancements in solid state batteries")

if st.button("Start Research"):
    if topic:
        with st.spinner(f"Agents are researching: {topic}... This may take a minute or two."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/api/v1/research",
                    json={"topic": topic, "depth": "comprehensive"}
                )
                if response.status_code == 200:
                    data = response.json()
                    st.success("Research complete!")
                    st.markdown("### Final Report")
                    st.markdown(data.get("message", "No content found."))
                else:
                    st.error(f"Failed to start research task: {response.text}")
            except Exception as e:
                st.error(f"Error connecting to API: {e}. Is the backend running?")
    else:
        st.warning("Please enter a topic.")
