import streamlit as st

st.set_page_config(
    page_title="Employee Management",
    layout="wide"
)

# Login
login = st.Page(
    "pages/login.py",
    title="Login",
    url_path="login"
)

# Employee
home = st.Page(
    "pages/home.py",
    title="Home",
    url_path="home"
)

# Admin
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


authenticated = st.session_state.get("authenticated", False)
role = st.session_state.get("role", "").lower()


if not authenticated:

    pg = st.navigation(
        [login],
        position="hidden"
    )

elif role == "admin" and authenticated == True:

    pg = st.navigation(
        [
            dashboard,
            employees,
            update_employee,
            add_employee
        ],
    )

elif role == "employee" and authenticated == True:

    pg = st.navigation(
        [home],
        position="hidden"
    )

else:

    st.session_state.clear()
    st.switch_page("/")


pg.run()