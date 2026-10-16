
import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("fastapi_url")

st.title("Audit Requests")
st.write("View pending employee requests and their audit details.")


# Search and pagination state
if "audit_page" not in st.session_state:
    st.session_state["audit_page"] = 0

if "audit_search" not in st.session_state:
    st.session_state["audit_search"] = ""

search = st.text_input(
    "Search audit requests",
    value=st.session_state["audit_search"],
    placeholder="Audit number, employee ID, operation..."
)

if search != st.session_state["audit_search"]:
    st.session_state["audit_search"] = search
    st.session_state["audit_page"] = 0
    st.rerun()

limit = 10
offset = st.session_state["audit_page"] * limit

# Fetch audit records from FastAPI
try:
    response = requests.get(
        f"{API_URL}/audits/",
        params={
            "search": search,
            "offset": offset,
            "limit": limit,
        },
        timeout=15,
    )

    if response.status_code == 401:
        st.error("Session expired. Please log in again.")
        st.stop()

    response.raise_for_status()
    result = response.json()

    audits = result["audits"]
    total = result["total"]

except requests.exceptions.ConnectionError:
    st.error("Could not connect to the FastAPI server.")
    st.stop()

except requests.exceptions.RequestException as exc:
    st.error(f"Could not fetch audit records: {exc}")
    st.stop()

except (KeyError, ValueError):
    st.error("Unexpected response from the API.")
    st.stop()


# Display audit requests as cards
if audits:
    for audit in audits:
        with st.container(border=True):
            st.subheader(
                f" {audit.get('audit_operation', 'N/A')}"
            )

            col1, col2 = st.columns(2)
 
            with col1:

                st.write("*Requested By:*",audit.get("audit_employee_id", "N/A"))

                st.write("*Target Employee:*",audit.get("target_employee_id", "N/A"))

            with col2:
                st.write("*Date:*",audit.get("audit_date", "N/A"))

                st.write("*Time:*",audit.get("audit_time", "N/A"))

                st.write("*Status:*",audit.get("audit_status", "N/A"))

            with st.expander("View full audit details"):
                st.json(audit)

else:
    st.info("No audit requests found.")


# Pagination
total_pages = max(1, (total + limit - 1) // limit)
page = st.session_state["audit_page"]

st.write(
    f"Page {page + 1} of {total_pages} "
    f"• {total} audit requests"
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button(
        "← Previous",
        disabled=(page == 0),
        use_container_width=True,
    ):
        st.session_state["audit_page"] -= 1
        st.rerun()

with col2:
    start = offset + 1 if total else 0
    end = min(offset + len(audits), total)
    st.write(f"Showing {start}–{end}")

with col3:
    if st.button(
        "Next →",
        disabled=(page >= total_pages - 1),
        use_container_width=True,
    ):
        st.session_state["audit_page"] += 1
        st.rerun()
