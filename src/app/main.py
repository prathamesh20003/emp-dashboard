#uv run uvicorn main:app --reload

from argon2 import _password_hasher
from fastapi import FastAPI, HTTPException
from database import SessionLocal, Base, engine
from schemas import EmployeeCreate, EmployeeUpdate, LoginEmployee
from crud import (  
    create_employee,
    get_all_employees,
    update_employee,
    get_active_employee_count,
    get_department_count,
    get_inactive_employee_count,
    get_total_employee_count,
    generate_temporary_password,
    hash_password,
    find_employee
)
from src.app.dashboard import password

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/dashboard") #send data to dashboard
def get_dashboard():
    db = SessionLocal()
    try:
        return {
            "total_employees": get_total_employee_count(db),
            "active_employees": get_active_employee_count(db),
            "inactive_employees": get_inactive_employee_count(db),
            "departments": get_department_count(db),
        }
    finally:
        db.close()

@app.post("/employees/") #create employee 
def add_employee(employee: EmployeeCreate):

    db = SessionLocal()

    try:

        password = generate_temporary_password()
        print(password)
        
        employee.password_hash = hash_password(password)
        print(employee.password_hash)
        new_employee = create_employee(
            db=db,
            employee_data=employee
        )
        
        return {
            "message": "Employee added successfully",
            "employee_id": new_employee.employee_id
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    finally:
        db.close()


@app.get("/employees/") #get all employees and their details in json
def get_employees():

    db = SessionLocal()

    try:

        employees = get_all_employees(db)

        return [
            {
                "employee_id": employee.employee_id,
                "first_name": employee.first_name,
                "last_name": employee.last_name,
                "email": employee.email,
                "phone": employee.phone,
                "department": employee.department,
                "designation": employee.designation,
                "branch": employee.branch,
                "joining_date": employee.joining_date,
                "status": employee.status,
                "password_hash": employee.password_hash,
                "session_no": employee.session_no,
            }
            for employee in employees
        ]

    finally:
        db.close()


@app.put("/employees/{employee_id}") #update employee details
def edit_employee(employee: EmployeeUpdate):

    db = SessionLocal()

    #print("request", employee)

    try:

        updated_employee = update_employee(
            db=db,
            employee_data=employee
        )

        #print("updated_employee", employee.employee_id)
        
        if updated_employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        return {
            "message": "Employee updated successfully",
            "employee_id": updated_employee.employee_id
        }

    except HTTPException:
        raise

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    finally:
        db.close()

