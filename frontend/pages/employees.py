import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000"


st.title("Employees")
st.write("View all bank employees.")

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

    else:

        st.info("No employees found.")