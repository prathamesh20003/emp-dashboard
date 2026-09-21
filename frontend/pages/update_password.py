import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Change Password",
    layout="centered"
)

# Check login
if not st.session_state.get("authenticated", False):
    st.switch_page("/")

employee_id = st.session_state.get("employee_id")

st.title("Change Password")
st.write("Please create a new password for your account.")

with st.form("change_password_form"):

    new_password = st.text_input(
        "New Password",
        type="password",
        placeholder="Enter your new password"
    )

    confirm_password = st.text_input(
        "Confirm New Password",
        type="password",
        placeholder="Re-enter your new password"
    )

    submitted = st.form_submit_button("Change Password")

    if submitted:

        if not new_password or not confirm_password:
            st.error("Please enter both password fields.")

        elif new_password != confirm_password:
            st.error("Passwords do not match.")

        else:

            try:

                response = requests.post(
                    f"{API_URL}/change-password/",
                    json={
                        "employee_id": employee_id,
                        "new_password": new_password
                    }
                )

                if response.status_code == 200:

                    st.success("Password changed successfully.")

                    # Mark first login as completed
                    st.session_state["session_no"] = 1

                    st.switch_page("/home")

                else:

                    try:
                        detail = response.json().get(
                            "detail",
                            "Could not change password."
                        )
                    except Exception:
                        detail = "Could not change password."

                    st.error(detail)

            except requests.exceptions.ConnectionError:

                st.error("Could not connect to the server.")