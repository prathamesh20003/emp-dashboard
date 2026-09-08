from fastapi import FastAPI, HTTPException
from database import SessionLocal
from schemas import EmployeeCreate, EmployeeUpdate
from crud import create_employee, get_all_employees, update_employee

app = FastAPI()

@app.post("/employees/")
def add_employee(employee: EmployeeCreate):

    db = SessionLocal()

    try:

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


@app.get("/employees/")
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
                "status": employee.status
            }
            for employee in employees
        ]

    finally:
        db.close()


@app.put("/employees/{employee_id}")
def edit_employee(
    employee_id: str,
    employee: EmployeeUpdate
):

    db = SessionLocal()

    try:

        updated_employee = update_employee(
            db=db,
            employee_id=employee_id,
            employee_data=employee
        )

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