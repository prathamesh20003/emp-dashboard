import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("fastapi_url")

st.title("Logs")

st.write("Applications logs.")

st.markdown("---")