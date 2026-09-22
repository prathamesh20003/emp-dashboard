import streamlit as st
import pandas as pd
import requests


#API_URL = "https://emp-dashboard-production.up.railway.app"
API_URL = "http://127.0.0.1:8000"

st.title("Update Employee")
st.write("Search for an employee and update their information.")



with st.form("search_employee_form"):

    search = st.text_input(
        "Search Employee",
        placeholder="Employee ID, name, email, department, branch..."
    )

    search_submitted = st.form_submit_button(
        "Search",
        use_container_width=True
    )

#search logic
if search_submitted:

    if not search.strip():

        st.warning("Please enter a search keyword.")

    else:

        try:

            response = requests.get(
                f"{API_URL}/employees/",
                params={
                    "search": search,
                    "offset": 0,
                    "limit": 10
                }
            )

            if response.status_code != 200:

                st.error("Could not search employees.")
                st.stop()

            data = response.json()

            employees = data["employees"]

            if not employees:

                st.info("No employees found.")
                st.stop()

            # Store search results
            st.session_state["update_search_results"] = employees

        except requests.exceptions.ConnectionError:

            st.error("Could not connect to the server.")
            st.stop()

# display
employees = st.session_state.get(
    "update_search_results",
    []
)


if employees:

    employee_ids = [
        employee["employee_id"]
        for employee in employees
    ]

    selected_id = st.selectbox(
        "Select Employee",
        employee_ids
    )

    selected_employee = next(
        employee
        for employee in employees
        if employee["employee_id"] == selected_id
    )

    st.markdown("---")
    
    #update form
    with st.form("edit_employee_form"):

        col1, col2 = st.columns(2)

        with col1:

            first_name = st.text_input(
                "First Name",
                value=selected_employee["first_name"]
            )

            middle_name = st.text_input(
                "Middle Name",
                value=selected_employee["middle_name"]
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

            date_of_birth = st.date_input(
                "Date of Birth",
                value=selected_employee["date_of_birth"]
            )

            gender_options = ["Male", "Female", "Other"]
            
            current_gender = selected_employee.get("gender")
            
            if current_gender not in gender_options:
                current_gender = "Other"
            
            gender = st.selectbox(
                "Gender",
                gender_options,
                index=gender_options.index(current_gender)
            )

            address = st.text_input(
                "Address",
                value=selected_employee["address"]
            )

            city = st.text_input(
                "City",
                value=selected_employee["city"]
            )

            state = st.text_input(
                "State",
                value=selected_employee["state"]
            )

            postal_code = st.text_input(
                "Postal Code",
                value=selected_employee["postal_code"]
            )
        with col2:
            
            salary = st.number_input(
                "Salary",
                value=selected_employee["salary"] or 0
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


            designation = st.text_input(
                "Designation",
                value=selected_employee["designation"]
            )

            current_employee_type = selected_employee["employee_type"]

            employee_type = st.selectbox(
                "Employee Type",
                ["Full Time", "Part Time", "Contract"],
                index=(
                    ["Full Time", "Part Time", "Contract"].index(current_employee_type)
                    if current_employee_type in ["Full Time", "Part Time", "Contract"]
                    else 0
                )
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

            role = st.text_input(
                "Role",
                value=selected_employee["role"] or ""
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

            try:

                response = requests.put(
                    f"{API_URL}/employees/{selected_id}",
                    json=update_data
                )

                if response.status_code == 200:

                    st.success(
                        "Employee updated successfully!"
                    )

                    # Remove old search results
                    st.session_state.pop(
                        "update_search_results",
                        None
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

            except requests.exceptions.ConnectionError:

                st.error("Could not connect to the server.")

    st.markdown("---")
    
    st.subheader("Delete Employee")
    
    st.warning(
        f"You are about to permanently delete "
        f"{selected_employee['first_name']} "
        f"{selected_employee['last_name']} "
        f"({selected_employee['employee_id']})."
    )
    
    if st.button(
        "🗑️ Delete Employee",
        use_container_width=True
    ):
    
        try:
    
            response = requests.delete(
                f"{API_URL}/delete-employees/{selected_id}",
                timeout=10
            )
    
            if response.status_code == 200:
    
                st.success(
                    "Employee deleted successfully!"
                )
    
                # Remove search results
                st.session_state.pop(
                    "update_search_results",
                    None
                )
    
                st.rerun()
    
            else:
    
                try:
    
                    detail = response.json().get(
                        "detail",
                        "Delete failed"
                    )
    
                except Exception:
    
                    detail = "Delete failed"
    
                st.error(detail)
    
        except requests.exceptions.ConnectionError:
    
            st.error(
                "Could not connect to the server."
            )
    
        except requests.exceptions.Timeout:
    
            st.error(
                "The server took too long to respond."
            )