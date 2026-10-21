import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("fastapi_url")

st.title("Audit Requests")
st.write("Review proposed employee changes and approve or reject requests.")

if not API_URL:
    st.error("FastAPI URL is missing. Check your .env file.")
    st.stop()

API_URL = API_URL.rstrip("/")

# Search and pagination state
if "audit_page" not in st.session_state:
    st.session_state["audit_page"] = 0

if "audit_search" not in st.session_state:
    st.session_state["audit_search"] = ""

if "audit_confirmation" not in st.session_state:
    st.session_state["audit_confirmation"] = None

search = st.text_input(
    "Search audit requests",
    value=st.session_state["audit_search"],
    placeholder="Audit number, employee ID, operation, or status...",
)

if search != st.session_state["audit_search"]:
    st.session_state["audit_search"] = search
    st.session_state["audit_page"] = 0
    st.rerun()

limit = 10
offset = st.session_state["audit_page"] * limit

# Fetch audit records
try:
    response = requests.get(
        f"{API_URL}/audits/",
        params={
            "search": search,
            "offset": offset,
            "limit": limit,
        },
        timeout=15,
    )

    if response.status_code == 401:
        st.error("Session expired. Please log in again.")
        st.stop()

    response.raise_for_status()
    result = response.json()

    audits = result["audits"]
    total = result["total"]

except requests.exceptions.ConnectionError:
    st.error("Could not connect to the FastAPI server.")
    st.stop()

except requests.exceptions.RequestException as exc:
    st.error(f"Could not fetch audit records: {exc}")
    st.stop()

except (KeyError, ValueError, TypeError):
    st.error("Unexpected response from the API.")
    st.stop()


# Display audit requests
if audits:
    for audit in audits:
        audit_number = audit.get("audit_number", "")
        status = audit.get("audit_status", "N/A")
        employee = audit.get("employee")

        with st.container(border=True):
            st.subheader(
                f"{audit.get('audit_operation', 'N/A')} "
                f"— {audit_number or 'N/A'}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.write(
                    "**Requested By:**",
                    audit.get("audit_employee_id") or "N/A",
                )
                st.write(
                    "**Target Employee:**",
                    audit.get("target_employee_id") or "N/A",
                )
                st.write(
                    "**Operation:**",
                    audit.get("audit_operation") or "N/A",
                )

            with col2:
                st.write("**Date:**", audit.get("audit_date") or "N/A")
                st.write("**Time:**", audit.get("audit_time") or "N/A")
                st.write("**Status:**", status)

            # Collapsible proposed employee details
            with st.expander("Proposed Employee Details"):
                if employee:
                    name_parts = [
                        employee.get("first_name"),
                        employee.get("middle_name"),
                        employee.get("last_name"),
                    ]
                    full_name = " ".join(
                        part for part in name_parts if part
                    )

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write(
                            "**Employee ID:**",
                            employee.get("employee_id") or "N/A",
                        )
                        st.write("**Full Name:**", full_name or "N/A")
                        st.write("**Email:**", employee.get("email") or "N/A")
                        st.write("**Phone:**", employee.get("phone") or "N/A")
                        st.write(
                            "**Date of Birth:**",
                            employee.get("date_of_birth") or "N/A",
                        )
                        st.write("**Gender:**", employee.get("gender") or "N/A")
                        st.write("**Address:**", employee.get("address") or "N/A")
                        st.write("**City:**", employee.get("city") or "N/A")
                        st.write("**State:**", employee.get("state") or "N/A")
                        st.write(
                            "**Postal Code:**",
                            employee.get("postal_code") or "N/A",
                        )

                    with col2:
                        st.write(
                            "**Department:**",
                            employee.get("department") or "N/A",
                        )
                        st.write(
                            "**Designation:**",
                            employee.get("designation") or "N/A",
                        )
                        st.write(
                            "**Employee Type:**",
                            employee.get("employee_type") or "N/A",
                        )
                        st.write("**Branch:**", employee.get("branch") or "N/A")
                        salary = employee.get("salary")
                        st.write(
                            "**Salary:**",
                            salary if salary is not None else "N/A",
                        )
                        st.write(
                            "**Joining Date:**",
                            employee.get("joining_date") or "N/A",
                        )
                        st.write(
                            "**Reporting Manager:**",
                            employee.get("reporting_manager") or "N/A",
                        )
                        st.write(
                            "**Employment Status:**",
                            employee.get("status") or "N/A",
                        )
                        st.write("**Role:**", employee.get("role") or "N/A")
                        st.write(
                            "**Request Status:**",
                            employee.get("audit_status") or "N/A",
                        )
                        st.write(
                            "**Request Operation:**",
                            employee.get("audit_operation") or "N/A",
                        )
                else:
                    st.info("No proposed employee details were found.")

            # Approval/rejection actions
            if status == "Request Pending":
                approve_col, reject_col = st.columns(2)

                with approve_col:
                    if st.button(
                        "Approve",
                        key=f"approve_{audit_number}",
                        type="primary",
                        use_container_width=True,
                    ):
                        st.session_state["audit_confirmation"] = {
                            "audit": audit,
                            "employee": employee,
                            "audit_number": audit_number,
                            "action": "approve",
                        }
                        st.rerun()

                with reject_col:
                    if st.button(
                        "Reject",
                        key=f"reject_{audit_number}",
                        use_container_width=True,
                    ):
                        st.session_state["audit_confirmation"] = {
                            "audit": audit,
                            "employee": employee,
                            "audit_number": audit_number,
                            "action": "reject",
                        }
                        st.rerun()

            else:
                st.caption(f"This request is already marked: {status}")

# Confirmation panel
confirmation = st.session_state["audit_confirmation"]

if confirmation:
    audit = confirmation["audit"]
    audit_number = confirmation["audit_number"]
    action = confirmation["action"]
    employee = confirmation["employee"]

    
    st.warning(
        f"Are you sure you want to {action} audit request "
        f"{audit_number}?"
    )

    yes_col, no_col = st.columns(2)

    with yes_col:
        if st.button(
            f"Confirm {action.title()}",
            key="confirm_audit_action",
            type="primary",
            use_container_width=True,
        ):
            # ---- route by action first ----
            if action == "reject":
                url = f"{API_URL}/audits/reject"
                body = {"audit_number": audit_number}
    
            else:  # approve
                operation = (audit.get("audit_operation") or "").lower()
    
                if "add" in operation:
                    url = f"{API_URL}/audits/add-employee/approve"
                elif "update" in operation:
                    url = f"{API_URL}/audits/update-employee/approve"
                else:
                    st.error(f"Unsupported operation: {audit.get('audit_operation')}")
                    st.stop()
    
                body = {
                    "employee_id": employee.get("employee_id"),
                    "first_name": employee.get("first_name"),
                    "middle_name": employee.get("middle_name"),
                    "last_name": employee.get("last_name"),
                    "email": employee.get("email"),
                    "phone": employee.get("phone"),
                    "date_of_birth": employee.get("date_of_birth"),
                    "gender": employee.get("gender"),
                    "address": employee.get("address"),
                    "city": employee.get("city"),
                    "state": employee.get("state"),
                    "postal_code": employee.get("postal_code"),
                    "salary": employee.get("salary"),
                    "department": employee.get("department"),
                    "designation": employee.get("designation"),
                    "employee_type": employee.get("employee_type"),
                    "branch": employee.get("branch"),
                    "joining_date": employee.get("joining_date"),
                    "reporting_manager": employee.get("reporting_manager"),
                    "status": employee.get("status"),
                    "role": employee.get("role"),

                    "audit_number": audit_number,
                    "audit_employee_id": st.session_state["employee_id"],
                }
    
            # ---- send ----
            try:
                action_response = requests.post(url, json=body, timeout=15)
    
                if action_response.status_code == 401:
                    st.error("Session expired. Please log in again.")
                    st.stop()
    
                if not action_response.ok:
                    try:
                        detail = action_response.json().get("detail", action_response.text)
                    except ValueError:
                        detail = action_response.text
                    st.error(
                        f"Could not {action} request "
                        f"({action_response.status_code}): {detail}"
                    )
                    st.stop()
    
                st.success(
                    action_response.json().get(
                        "message", f"Request {action}d successfully."
                    )
                )
                st.session_state["audit_confirmation"] = None
    
            except requests.exceptions.RequestException as exc:
                st.error(f"Network error: {exc}")

    with no_col:
        if st.button(
            "Cancel",
            key="cancel_audit_action",
            use_container_width=True,
        ):
            st.session_state["audit_confirmation"] = None
            st.rerun()

else:
    if not audits:
        st.info("No audit requests found.")

# Pagination
total_pages = max(1, (total + limit - 1) // limit)
page = st.session_state["audit_page"]

st.write(
    f"Page {page + 1} of {total_pages} "
    f"• {total} audit requests"
)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button(
        "← Previous",
        disabled=(page == 0),
        use_container_width=True,
    ):
        st.session_state["audit_page"] -= 1
        st.rerun()

with col2:
    start = offset + 1 if total else 0
    end = min(offset + len(audits), total)
    st.write(f"Showing {start}–{end}")

with col3:
    if st.button(
        "Next →",
        disabled=(page >= total_pages - 1),
        use_container_width=True,
    ):
        st.session_state["audit_page"] += 1
        st.rerun()