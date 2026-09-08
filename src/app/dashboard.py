import streamlit as st
import pandas as pd
import requests


API_URL = "http://localhost:8000"

st.set_page_config(page_title="EM", layout="wide")

# css
st.markdown(
    """
<style>
    .main {
        padding-top: 2rem;
    }

    .metric-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
    }

    .employee-card {
        padding: 15px;
        border: 1px solid #e5e7eb;
        border-radius: 10px;
        margin-bottom: 10px;
    }
</style>
""",
    unsafe_allow_html=True,
)

# sidebar
with st.sidebar:

    st.title("Admin")

    st.markdown("---")

    page = st.radio("Navigation", ["Dashboard", "Employees", "Add Employee"])

    st.markdown("---")

# dashboard
if page == "Dashboard":
    
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

elif page == "Employees":

    st.title("Employees")
    st.write("View and manage all bank employees.")

    # Get employees from FastAPI
    response = requests.get(
        f"{API_URL}/employees/"
    )

    if response.status_code != 200:

        st.error("Could not fetch employees.")

    else:

        employees = response.json()

        if employees:
            
            df = pd.DataFrame(employees)

            df = df.rename(
                columns={
                    "employee_id": "Employee ID",
                    "first_name": "First Name",
                    "last_name": "Last Name",
                    "email": "Email",
                    "phone": "Phone",
                    "department": "Department",
                    "designation": "Designation",
                    "branch": "Branch",
                    "joining_date": "Joining Date",
                    "status": "Status"
                }
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.markdown("---")

            st.subheader("Edit Employee")
            
            employee_ids = [
                employee["employee_id"]
                for employee in employees
            ]

            selected_id = st.selectbox(
                "Select Employee",
                employee_ids
            )

            # finding selected employee
            selected_employee = next(
                employee
                for employee in employees
                if employee["employee_id"] == selected_id
            )

            # update form
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

                    department = st.selectbox(
                        "Department",
                        departments,
                        index=departments.index(
                            selected_employee["department"]
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

                    branch = st.selectbox(
                        "Branch",
                        branches,
                        index=branches.index(
                            selected_employee["branch"]
                        )
                    )

                    joining_date = st.date_input(
                        "Joining Date",
                        value=selected_employee["joining_date"]
                    )

                    statuses = ["Active", "Inactive"]

                    status = st.selectbox(
                        "Status",
                        statuses,
                        index=statuses.index(
                            selected_employee["status"]
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

                        st.error(
                            response.json().get(
                                "detail",
                                "Update failed"
                            )
                        )

        else:

            st.info("No employees found.")
     
# add employee
elif page == "Add Employee":
    
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
                    },
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success(f"Employee {data['employee_id']} added successfully!")

                else:
                    error = response.json()

                    st.error(f"Error: {error['detail']}")
