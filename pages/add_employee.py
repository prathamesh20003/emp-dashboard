import streamlit as st
import requests
import os
from dotenv import load_dotenv
from datetime import date


load_dotenv()

API_URL = os.getenv("fastapi_url")

st.title("Add Employee")
st.write("Enter employee details below")

st.markdown("---")

# form to add employees
with st.form("add_employee_form"):
    
    # Employee details
    st.subheader("Employee Details")

    col1, col2 = st.columns(2)

    with col1:
        employee_id = st.text_input("Employee ID", placeholder="EMP001")

        first_name = st.text_input("First Name", placeholder="Enter first name")

        middle_name = st.text_input("Middle Name", placeholder="Enter middle name")

        last_name = st.text_input("Last Name", placeholder="Enter last name")

        date_of_birth = st.date_input("Date of Birth", value=date(2000,1,1), min_value=date(1950, 1, 1), max_value=date.today())

        gender = st.selectbox("Gender", ["Male", "Female", "Other"])

        email = st.text_input("Email", placeholder="employee@bank.com")

        phone = st.text_input("Phone", placeholder="Enter phone number")

        address = st.text_input("Address", placeholder="Enter address")

        city = st.text_input("City", placeholder="Enter city")

        state = st.text_input("State", placeholder="Enter state")

        postal_code = st.text_input("Postal Code", placeholder="Enter Postal code")
        
    with col2:
        department = st.selectbox(
            "Department",
            ["IT", "HR", "Finance", "Operations", "Loans", "Marketing"],
        )

        designation = st.text_input(
            "Designation", placeholder="e.g. Software Engineer"
        )

        branch = st.selectbox(
            "Branch",
            ["Mumbai", "Pune", "Delhi", "Bangalore", "Chennai", "Hyderabad"],
        )

        joining_date = st.date_input("Joining Date")

        salary = st.number_input("Salary", min_value=0.0, step=0.01)

        employee_type = st.selectbox("Employee Type", ["Full Time", "Part Time", "Contract"])

        reporting_manager = st.text_input("Reporting Manager", placeholder="Enter reporting manager")

        role = st.text_input("Role", placeholder="Enter role")

        status = st.selectbox("Status", ["Active", "Inactive"])

    st.markdown("---")

    submitted = st.form_submit_button("Add Employee", use_container_width=True)

    if submitted:

        response = requests.post(
            f"{API_URL}/add-audit-request/",
            json={
                "employee_id": employee_id,
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                
                "email": email,
                "phone": phone,

                "date_of_birth": str(date_of_birth),
                "gender": gender,

                "address": address,
                "city": city,
                "state": state,
                "postal_code": postal_code,

                "salary": salary,
                
                "department": department,
                "designation": designation,
                "employee_type": employee_type,
                "branch": branch,
                "joining_date": str(joining_date),
                "reporting_manager": reporting_manager,
                
                "status": status,
                "role": role,

                "audit_employee_id": st.session_state["employee_id"],
                "audit_operation": "Add Employee"
            },
        )

        if response.status_code == 200:
            data = response.json()

            st.success(f"Request to add Employee {data['employee_id']} sent")

        else:
            error = response.json()

            st.error(f"Error: {error['detail']}")
