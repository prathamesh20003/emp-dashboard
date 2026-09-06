import streamlit as st
from database import Base, engine, SessionLocal
import models
import pandas as pd
from crud import (
    create_employee,
    get_all_employees,
    get_total_employee_count,
    get_active_employee_count,
    get_inactive_employee_count,
    get_department_count,
    update_employee
)


Base.metadata.create_all(bind=engine)

st.set_page_config(
    page_title="EM",
    layout="wide"
)

#css
st.markdown("""
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
""", unsafe_allow_html=True)

#sidebar
with st.sidebar:

    st.title("Admin")

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Employees",
            "Add Employee"
        ]
    )

    st.markdown("---")

# dashboard
if page == "Dashboard":

    st.title("Employee Management Dashboard")

    st.write(
        "Manage and monitor bank employees from one place."
    )

    st.markdown("---")

    # Get data from database
    db = SessionLocal()

    try:
        total_employees = get_total_employee_count(db)
        active_employees = get_active_employee_count(db)
        inactive_employees = get_inactive_employee_count(db)
        departments = get_department_count(db)

    finally:
        db.close()

    # Dashboard metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Employees",
            total_employees
        )

    with col2:
        st.metric(
            "Active Employees",
            active_employees
        )

    with col3:
        st.metric(
            "Inactive Employees",
            inactive_employees
        )

    with col4:
        st.metric(
            "Departments",
            departments
        )

    st.markdown("---")


# employees
elif page == "Employees":

    st.title("Employees")
    st.write("View and manage all bank employees.")

    db = SessionLocal()

    try:
        employees = get_all_employees(db)

        if employees:

            # Display employees
            data = []

            for employee in employees:
                data.append({
                    "Employee ID": employee.employee_id,
                    "First Name": employee.first_name,
                    "Last Name": employee.last_name,
                    "Email": employee.email,
                    "Phone": employee.phone,
                    "Department": employee.department,
                    "Designation": employee.designation,
                    "Branch": employee.branch,
                    "Joining Date": employee.joining_date,
                    "Status": employee.status
                })

            df = pd.DataFrame(data)

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True
            )

            st.markdown("---")

            # Select employee
            st.subheader("Edit Employee")

            employee_ids = [
                employee.employee_id
                for employee in employees
            ]

            selected_id = st.selectbox(
                "Select Employee",
                employee_ids
            )

            # Find selected employee
            selected_employee = next(
                (
                    employee
                    for employee in employees
                    if employee.employee_id == selected_id
                ),
                None
            )

            # Edit form
            with st.form("edit_employee_form"):

                col1, col2 = st.columns(2)

                with col1:

                    first_name = st.text_input(
                        "First Name",
                        value=selected_employee.first_name
                    )

                    last_name = st.text_input(
                        "Last Name",
                        value=selected_employee.last_name
                    )

                    email = st.text_input(
                        "Email",
                        value=selected_employee.email
                    )

                    phone = st.text_input(
                        "Phone",
                        value=selected_employee.phone or ""
                    )

                    department = st.selectbox(
                        "Department",
                        [
                            "IT",
                            "HR",
                            "Finance",
                            "Operations",
                            "Loans",
                            "Marketing"
                        ],
                        index=[
                            "IT",
                            "HR",
                            "Finance",
                            "Operations",
                            "Loans",
                            "Marketing"
                        ].index(selected_employee.department)
                    )

                with col2:

                    designation = st.text_input(
                        "Designation",
                        value=selected_employee.designation
                    )

                    branch_options = [
                        "Mumbai",
                        "Pune",
                        "Delhi",
                        "Bangalore",
                        "Chennai",
                        "Hyderabad"
                    ]

                    branch = st.selectbox(
                        "Branch",
                        branch_options,
                        index=branch_options.index(
                            selected_employee.branch
                        )
                    )

                    joining_date = st.date_input(
                        "Joining Date",
                        value=selected_employee.joining_date
                    )

                    status = st.selectbox(
                        "Status",
                        ["Active", "Inactive"],
                        index=["Active", "Inactive"].index(
                            selected_employee.status
                        )
                    )

                submitted = st.form_submit_button(
                    "Update Employee",
                    use_container_width=True
                )

                if submitted:

                    try:

                        update_employee(
                            db=db,
                            employee_id=selected_employee.employee_id,
                            first_name=first_name,
                            last_name=last_name,
                            email=email,
                            phone=phone,
                            department=department,
                            designation=designation,
                            branch=branch,
                            joining_date=joining_date,
                            status=status
                        )

                        st.success(
                            f"Employee {selected_employee.employee_id} updated successfully!"
                        )

                    except Exception as e:

                        db.rollback()

                        st.error(
                            f"Error updating employee: {e}"
                        )

        else:

            st.info("No employees found.")

    finally:
        db.close()

        
# add employee
elif page == "Add Employee":

    st.title("Add Employee")
    st.write("Enter employee details below")

    st.markdown("---")

    #form to add employees
    with st.form("add_employee_form"):

        # Employee details
        st.subheader("Employee Details")

        col1, col2 = st.columns(2)

        with col1:
            employee_id = st.text_input(
                "Employee ID",
                placeholder="EMP001"
            )

            first_name = st.text_input(
                "First Name",
                placeholder="Enter first name"
            )

            last_name = st.text_input(
                "Last Name",
                placeholder="Enter last name"
            )

            email = st.text_input(
                "Email",
                placeholder="employee@bank.com"
            )

            phone = st.text_input(
                "Phone",
                placeholder="Enter phone number"
            )

        with col2:
            department = st.selectbox(
                "Department",
                [
                    "IT",
                    "HR",
                    "Finance",
                    "Operations",
                    "Loans",
                    "Marketing"
                ]
            )

            designation = st.text_input(
                "Designation",
                placeholder="e.g. Software Engineer"
            )

            branch = st.selectbox(
                "Branch",
                [
                    "Mumbai",
                    "Pune",
                    "Delhi",
                    "Bangalore",
                    "Chennai",
                    "Hyderabad"
                ]
            )

            joining_date = st.date_input(
                "Joining Date"
            )

            status = st.selectbox(
                "Status",
                [
                    "Active",
                    "Inactive"
                ]
            )

        st.markdown("---")

        submitted = st.form_submit_button(
            "Add Employee",
            use_container_width=True
        )

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

                db = SessionLocal()
        
                try:
                    employee = create_employee(
                        db=db,
                        employee_id=employee_id,
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=phone,
                        department=department,
                        designation=designation,
                        branch=branch,
                        joining_date=joining_date,
                        status=status
                    )
        
                    st.success(
                        f"Employee {employee.employee_id} added successfully!"
                    )
        
                except Exception as e:
                    db.rollback()
                    st.error(f"Error: {e}")
        
                finally:
                    db.close()
