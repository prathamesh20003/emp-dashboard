import streamlit as st
import requests

API_URL = "https://radiant-purpose-production-3134.up.railway.app"

st.title("Employee Management Dashboard")

st.write("Manage and monitor bank employees from one place.")

st.markdown("---")

try:
    response = requests.get(
        f"{API_URL}/dashboard/"
    )

    if response.status_code == 200:

        dashboard_data = response.json()
        total_employees = dashboard_data["total_employees"]
        active_employees = dashboard_data["active_employees"]
        inactive_employees = dashboard_data["inactive_employees"]
        departments = dashboard_data["departments"]

    else:
        st.error("Could not fetch dashboard data.")
        st.stop()
except requests.exceptions.ConnectionError:
    st.error("Could not connect to the server.")
    st.stop()

# Dashboard metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Employees", total_employees)

with col2:
    st.metric("Active Employees", active_employees)

with col3:
    st.metric("Inactive Employees", inactive_employees)

with col4:
    st.metric("Departments", departments)

st.markdown("---")

if st.button("Logout"):

    st.session_state.clear()

    st.rerun()