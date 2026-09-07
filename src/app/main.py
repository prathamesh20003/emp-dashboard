from fastapi import FastAPI, HTTPException
from database import SessionLocal
from schemas import EmployeeCreate
from crud import create_employee

app = FastAPI()

@app.post("/employees/")
def add_employee(employee: EmployeeCreate):

    db = SessionLocal()

    try:
        new_employee = create_employee(
            db=db,
            employee_id=employee.employee_id,
            first_name=employee.first_name,
            last_name=employee.last_name,
            email=employee.email,
            phone=employee.phone,
            department=employee.department,
            designation=employee.designation,
            branch=employee.branch,
            joining_date=employee.joining_date,
            status=employee.status,
        )

        return {
            "message": "Employee added successfully",
            "employee_id": new_employee.employee_id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
        
    finally:
        db.close()