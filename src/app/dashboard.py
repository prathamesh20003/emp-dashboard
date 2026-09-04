import streamlit as st

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



#dashboard
if page == "Dashboard":

    st.title("EM Dashboard")

    st.write(
        "Manage and monitor bank employees from one place."
    )

    st.markdown("---")

#employees
elif page == "Employees":

    st.title("Employees")

    st.write("View and search all bank employees.")
elif page == "Add Employee":

    st.title("Add Employee")

    st.write("Enter employee details below.")
