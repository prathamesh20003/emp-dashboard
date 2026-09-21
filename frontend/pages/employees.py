import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"

st.title("Employees")
st.write("View all bank employees.")


if "employee_page" not in st.session_state:
    st.session_state["employee_page"] = 0

if "employee_search" not in st.session_state:
    st.session_state["employee_search"] = ""

# search input
search = st.text_input(
    "Search employees",
    value=st.session_state["employee_search"],
    placeholder="Search by ID, name, email, department, branch..."
)

if search != st.session_state["employee_search"]:

    st.session_state["employee_search"] = search
    st.session_state["employee_page"] = 0

    st.rerun()

#employee pagination

page = st.session_state["employee_page"]

limit = 10
offset = page * limit


try:

    response = requests.get(
        f"{API_URL}/employees/",
        params={
            "search": search,
            "offset": offset,
            "limit": limit
        }
    )

    if response.status_code != 200:

        st.error("Could not fetch employees.")
        st.stop()

    data = response.json()

    employees = data["employees"]
    total = data["total"]

except requests.exceptions.ConnectionError:

    st.error("Could not connect to the server.")
    st.stop()


# display table

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
            "status": "Status",
            "role": "Role"
        }
    )

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No employees found.")


# paginated view

total_pages = max(1, (total + limit - 1) // limit)

st.write(
    f"Page {page + 1} of {total_pages} "
    f"• {total} matching employees"
)


col1, col2, col3 = st.columns([1, 1, 1])


with col1:

    if st.button(
        "← Previous",
        disabled=(page == 0),
        use_container_width=True
    ):

        st.session_state["employee_page"] -= 1
        st.rerun()


with col2:

    st.write(
        f"Showing {offset + 1}–"
        f"{min(offset + len(employees), total)}"
    )


with col3:

    if st.button(
        "Next →",
        disabled=(page >= total_pages - 1),
        use_container_width=True
    ):

        st.session_state["employee_page"] += 1
        st.rerun()