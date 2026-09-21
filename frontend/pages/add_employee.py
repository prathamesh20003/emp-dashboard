import streamlit as st
import requests

API_URL = "https://emp-dashboard-production.up.railway.app"
#API_URL = "http://127.0.0.1:8000"

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

        last_name = st.text_input("Last Name", placeholder="Enter last name")

        email = st.text_input("Email", placeholder="employee@bank.com")

        phone = st.text_input("Phone", placeholder="Enter phone number")

        role = st.text_input("Role", placeholder="Enter role")
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

        status = st.selectbox("Status", ["Active", "Inactive"])

    st.markdown("---")

    submitted = st.form_submit_button("Add Employee", use_container_width=True)

    if submitted:
        
        if not employee_id:
            st.error("Employee ID is required.")

        elif not first_name:
            st.error("First Name is required.")

        elif not last_name:
            st.error("Last Name is required.")

        elif not email:
            st.error("Email is required.")

        else:
            response = requests.post(
                f"{API_URL}/employees/",
                json={
                    "employee_id": employee_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone": phone,
                    "department": department,
                    "designation": designation,
                    "branch": branch,
                    "joining_date": str(joining_date),
                    "status": status,
                    "role": role
                },
            )

            if response.status_code == 200:
                data = response.json()

                st.success(f"Employee {data['employee_id']} added successfully!")

            else:
                error = response.json()

                st.error(f"Error: {error['detail']}")
