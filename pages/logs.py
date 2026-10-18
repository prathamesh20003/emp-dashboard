import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("fastapi_url")

st.title("Logs")
st.write("View all system activity logs.")

# ---- state ----
if "log_page" not in st.session_state:
    st.session_state["log_page"] = 0
if "log_search" not in st.session_state:
    st.session_state["log_search"] = ""

search = st.text_input(
    "Search logs",
    value=st.session_state["log_search"],
    placeholder="Report number, operation, status, employee ID...",
)

if search != st.session_state["log_search"]:
    st.session_state["log_search"] = search
    st.session_state["log_page"] = 0
    st.rerun()

limit = 10
offset = st.session_state["log_page"] * limit

# ---- fetch ----
try:
    response = requests.get(
        f"{API_URL}/logs/",
        params={"search": search, "offset": offset, "limit": limit},
        timeout=15,
    )

    if response.status_code == 401:
        st.error("Session expired. Please log in again.")
        st.stop()

    response.raise_for_status()
    result = response.json()

    logs = result["logs"]
    total = result["total"]

except requests.exceptions.ConnectionError:
    st.error("Could not connect to the FastAPI server.")
    st.stop()
except requests.exceptions.RequestException as exc:
    st.error(f"Could not fetch logs: {exc}")
    st.stop()
except (KeyError, ValueError):
    st.error("Unexpected response from the API.")
    st.stop()


# ---- display ----
if logs:
    for log in logs:
        with st.container(border=True):
            head_left, head_right = st.columns([3, 1])
            with head_left:
                st.markdown(
                        f"**`{log.get('id', 'N/A')}`** &nbsp;&nbsp; "
                        f"{log.get('report_operation', 'N/A')} &nbsp;&nbsp;" 
                        f"**{log.get('target_employee_id', 'N/A')}**"
                    )

            col1, col2 = st.columns(2)
            with col1:
                st.write("**Report Number:**", log.get("report_number", "N/A"))
                st.write("**Reporter:**", log.get("reporter_employee_id", "N/A"))
            with col2:
                st.write("**Date:**", log.get("report_date", "N/A"))
                st.write("**Time:**", log.get("report_time", "N/A"))


else:
    st.info("No logs found.")


# ---- pagination ----
total_pages = max(1, (total + limit - 1) // limit)
page = st.session_state["log_page"]

st.write(f"Page {page + 1} of {total_pages} • {total} log entries")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("← Previous", disabled=(page == 0), use_container_width=True):
        st.session_state["log_page"] -= 1
        st.rerun()

with col2:
    start = offset + 1 if total else 0
    end = min(offset + len(logs), total)
    st.write(f"Showing {start}–{end}")

with col3:
    if st.button(
        "Next →",
        disabled=(page >= total_pages - 1),
        use_container_width=True,
    ):
        st.session_state["log_page"] += 1
        st.rerun()