import streamlit as st

st.set_page_config(
    page_title="Employee Management",
    layout="wide"
)

# Login page
login = st.Page(
    "pages/login.py",
    title="Login",
    url_path="login"
)

# Admin pages
dashboard = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    url_path="dashboard"
)

employees = st.Page(
    "pages/employees.py",
    title="Employees",
    url_path="employees"
)

update_employee = st.Page(
    "pages/update_employee.py",
    title="Update Employee",
    url_path="update-employee"
)

add_employee = st.Page(
    "pages/add_employee.py",
    title="Add Employee",
    url_path="add-employee"
)

if not st.session_state.get("authenticated", False):

    # Only login is shown
    pg = st.navigation(
        [
            login,
            dashboard,
            employees,
            update_employee,
            add_employee
        ],
        #position="hidden"
    )

else:

    # Admin pages exist, but aren't shown in sidebar
    pg = st.navigation(
        [
            dashboard,
            employees,
            update_employee,
            add_employee
        ],
    )

pg.run()