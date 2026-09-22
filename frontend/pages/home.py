import streamlit as st

#API_URL = "https://emp-dashboard-production.up.railway.app"
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="My Profile",
    layout="wide"
)

# Make sure the user is logged in
if not st.session_state.get("authenticated", False):
    st.switch_page("/")


employee = st.session_state.get("employee")

if not employee:
    st.error("Employee details could not be loaded.")
    st.stop()


st.title(employee.get('first_name', '') + " " + employee.get('last_name', ''))
st.write("Welcome to the Employee Management System.")

st.divider()


col1, col2 = st.columns(2)

with col1:

    st.subheader("Personal Information")

    st.write(f"**Employee ID:** {employee.get('employee_id', '')}")
    st.write(f"**First Name:** {employee.get('first_name', '')}")
    st.write(f"**Last Name:** {employee.get('last_name', '')}")
    st.write(f"**Email:** {employee.get('email', '')}")
    st.write(f"**Phone:** {employee.get('phone', '')}")


with col2:

    st.subheader("Employment Information")

    st.write(f"**Department:** {employee.get('department', '')}")
    st.write(f"**Designation:** {employee.get('designation', '')}")
    st.write(f"**Branch:** {employee.get('branch', '')}")
    st.write(f"**Joining Date:** {employee.get('joining_date', '')}")
    st.write(f"**Status:** {employee.get('status', '')}")
    st.write(f"**Role:** {employee.get('role', '')}")


st.divider()


if st.button("Logout"):

    st.session_state.clear()

    st.rerun()