import streamlit as st

st.set_page_config(
    page_title="Employee Management",
    layout="wide"
)

dashboard = st.Page(
    "pages/dashboard.py",
    title="Dashboard",
    url_path="dashboard"
)

employees = st.Page(
    "pages/employees.py",
    title="View Employees",
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

login = st.Page(
    "pages/login.py",
    title="Login",
    url_path="login"
)

pg = st.navigation(
    [
        dashboard,
        employees,
        update_employee,
        add_employee
    ],
)
pg.run()
