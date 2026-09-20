import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"


st.title("Update Employee")
st.write("Update employee information.")

# Get employees from FastAPI
response = requests.get(
    f"{API_URL}/employees/"
)

if response.status_code != 200:

    st.error("Could not fetch employees.")

else:

    employees = response.json()

    if not employees:

        st.info("No employees found.")

    else:

        employee_ids = [
            employee["employee_id"]
            for employee in employees
        ]

        selected_id = st.selectbox(
            "Select Employee",
            employee_ids
        )

        # Find selected employee
        selected_employee = next(
            employee
            for employee in employees
            if employee["employee_id"] == selected_id
        )

        st.markdown("---")

        with st.form("edit_employee_form"):

            col1, col2 = st.columns(2)

            with col1:

                first_name = st.text_input(
                    "First Name",
                    value=selected_employee["first_name"]
                )

                last_name = st.text_input(
                    "Last Name",
                    value=selected_employee["last_name"]
                )

                email = st.text_input(
                    "Email",
                    value=selected_employee["email"]
                )

                phone = st.text_input(
                    "Phone",
                    value=selected_employee["phone"] or ""
                )

                departments = [
                    "IT",
                    "HR",
                    "Finance",
                    "Operations",
                    "Loans",
                    "Marketing"
                ]

                current_department = selected_employee["department"]

                department = st.selectbox(
                    "Department",
                    departments,
                    index=(
                        departments.index(current_department)
                        if current_department in departments
                        else 0
                    )
                )

            with col2:

                designation = st.text_input(
                    "Designation",
                    value=selected_employee["designation"]
                )

                branches = [
                    "Mumbai",
                    "Pune",
                    "Delhi",
                    "Bangalore",
                    "Chennai",
                    "Hyderabad"
                ]

                current_branch = selected_employee["branch"]

                branch = st.selectbox(
                    "Branch",
                    branches,
                    index=(
                        branches.index(current_branch)
                        if current_branch in branches
                        else 0
                    )
                )

                joining_date = st.date_input(
                    "Joining Date",
                    value=pd.to_datetime(
                        selected_employee["joining_date"]
                    ).date()
                )

                statuses = [
                    "Active",
                    "Inactive"
                ]

                current_status = selected_employee["status"]

                status = st.selectbox(
                    "Status",
                    statuses,
                    index=(
                        statuses.index(current_status)
                        if current_status in statuses
                        else 0
                    )
                )

            submitted = st.form_submit_button(
                "Update Employee",
                use_container_width=True
            )

            if submitted:

                update_data = {
                    "employee_id": selected_employee["employee_id"],
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "phone": phone,
                    "department": department,
                    "designation": designation,
                    "branch": branch,
                    "joining_date": str(joining_date),
                    "status": status
                }

                response = requests.put(
                    f"{API_URL}/employees/{selected_id}",
                    json=update_data
                )

                if response.status_code == 200:

                    st.success(
                        "Employee updated successfully!"
                    )

                    st.rerun()

                else:

                    try:
                        detail = response.json().get(
                            "detail",
                            "Update failed"
                        )
                    except Exception:
                        detail = "Update failed"

                    st.error(detail)