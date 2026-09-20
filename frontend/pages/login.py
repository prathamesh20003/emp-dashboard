import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Login",
    layout="centered"
)

st.markdown(
    """
    <style>
    /* Center the content */
    .block-container {
        max-width: 450px;
        padding-top: 8rem;
    }

    /* Login title */
    .login-title {
        text-align: center;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .login-subtitle {
        text-align: center;
        margin-bottom: 30px;
        font-size: 15px;
    }

    /* Form card */
    [data-testid="stForm"] {
        padding: 35px;
        border-radius: 14px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    }

    /* Input labels */
    label {
        font-weight: 600 !important;
    }

    /* Input fields */
    input {
        border-radius: 8px !important;
    }

    /* Login button */
    .stFormSubmitButton button {
        width: 100%;
        border-radius: 8px;
        height: 45px;
        font-weight: 600;
        font-size: 16px;
    }

    /* Success / error messages */
    .stAlert {
        border-radius: 8px;
    }

    </style>
    """,
    unsafe_allow_html=True
)



st.markdown(
    '<div class="login-title">Login</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="login-subtitle">Sign in to access the Employee Management System</div>',
    unsafe_allow_html=True
)


with st.form("login_form"):

    employee_id = st.text_input(
        "User ID",
        placeholder="Enter your user ID"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    submitted = st.form_submit_button(
        "Login"
    )

    if submitted:   

        if not employee_id or not password:

            st.error("Please enter your User ID and Password.")

        else:

            try:

                response = requests.post(
                    f"{API_URL}/login",
                    json={
                        "employee_id": employee_id,
                        "password": password
                    }
                )

                if response.status_code == 200:

                    st.success("Login successful!")

                    data = response.json()
                
                    st.session_state["authenticated"] = True
                    st.session_state["employee_id"] = data["employee_id"]
                    st.session_state["role"] = data["role"]

                    #st.switch_page("/dashboard")

                else:

                    try:
                        detail = response.json().get(
                            "detail",
                            "Invalid credentials"
                        )
                    except Exception:
                        detail = "Invalid credentials"

                    st.error(detail)

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the server."
                )
