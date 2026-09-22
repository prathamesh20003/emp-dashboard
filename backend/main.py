#uv run uvicorn main:app --reload

from argon2 import _password_hasher
from fastapi import FastAPI, HTTPException, Query
from database import SessionLocal, Base, engine
from schemas import EmployeeCreate, EmployeeUpdate, LoginRequest, CreateCredentials, ChangePassword
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
    find_employee,
    verify_password,
    create_credential,
    delete_employee
)
from models import Employee, Credentials

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

@app.post("/add-employees/") #create employee
def add_employee(employee: EmployeeCreate):

    db = SessionLocal()
    
    try:
        
        new_employee = create_employee(
            db=db,
            employee_data=employee
        )
        

        password = generate_temporary_password()
        print(password)
        hashed_password = hash_password(password)

        credential = CreateCredentials(
            employee_id = employee.employee_id,
            password_hash = hashed_password,
            role = employee.role,
            session_no = 0
        )
        
        credentials = create_credential(
            db=db,
            credential_data=credential
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


@app.get("/all-employees/") #get all employees and their details in json
def all_employees():

    db = SessionLocal()

    try:

        employees = get_all_employees(db)

        return [
                {
                    "employee_id": employee.employee_id,
                    "first_name": employee.first_name,
                    "middle_name": employee.middle_name,
                    "last_name": employee.last_name,
                    
                    "email": employee.email,
                    "phone": employee.phone,

                    "date_of_birth": employee.date_of_birth,
                    "gender": employee.gender,

                    "address": employee.address,
                    "city": employee.city,
                    "state": employee.state,
                    "postal_code": employee.postal_code,

                    "salary": employee.salary,
                    
                    "department": employee.department,
                    "designation": employee.designation,
                    "employee_type": employee.employee_type,
                    "branch": employee.branch,
                    "joining_date": employee.joining_date,
                    "reporting_manager": employee.reporting_manager,
                    
                    
                    "status": employee.status,
                    "role": employee.role
                }
                for employee in employees
            ]

    finally:
        db.close()

@app.get("/employees/") # get paginated list of employees
def get_employees(
    search: str = Query("", description="Search keyword"),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)):
    db = SessionLocal()

    try:

        query = db.query(Employee)

        # Search across employee fields
        if search:

            keyword = f"%{search}%"

            query = query.filter(
                (Employee.employee_id.ilike(keyword)) |
                (Employee.first_name.ilike(keyword)) |
                (Employee.middle_name.ilike(keyword)) |
                (Employee.last_name.ilike(keyword)) |
                
                (Employee.email.ilike(keyword)) |
                (Employee.phone.ilike(keyword)) |

                (Employee.date_of_birth.ilike(keyword)) |
                (Employee.gender.ilike(keyword)) |

                (Employee.address.ilike(keyword)) |
                (Employee.city.ilike(keyword)) |
                (Employee.state.ilike(keyword)) |
                (Employee.postal_code.ilike(keyword)) |

                (Employee.salary.ilike(keyword)) |
                
                (Employee.department.ilike(keyword)) |
                (Employee.designation.ilike(keyword)) |
                (Employee.branch.ilike(keyword)) |
                (Employee.status.ilike(keyword))
            )

        total = query.count()

        employees = (
            query
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "employees": [
                {
                    "employee_id": employee.employee_id,
                    "first_name": employee.first_name,
                    "middle_name": employee.middle_name,
                    "last_name": employee.last_name,
                    
                    "email": employee.email,
                    "phone": employee.phone,

                    "date_of_birth": employee.date_of_birth,
                    "gender": employee.gender,

                    "address": employee.address,
                    "city": employee.city,
                    "state": employee.state,
                    "postal_code": employee.postal_code,

                    "salary": employee.salary,
                    
                    "department": employee.department,
                    "designation": employee.designation,
                    "employee_type": employee.employee_type,
                    "branch": employee.branch,
                    "joining_date": employee.joining_date,
                    "reporting_manager": employee.reporting_manager,
                    
                    "status": employee.status,
                    "role": employee.role
                }
                for employee in employees
            ]
        }

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

@app.post("/login/") #login logic
def login(employee_data: LoginRequest):

    db = SessionLocal()

    try:

        employee = (
            db.query(Employee)
            .filter(
                Employee.employee_id == employee_data.employee_id
            )
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=401,
                detail="Invalid employee ID or password"
            )

        credential = (
            db.query(Credentials)
            .filter(
                Credentials.employee_id == employee.employee_id
            )
            .first()
        )

        if not credential:
            raise HTTPException(
                status_code=401,
                detail="Invalid employee ID or password"
            )

        # Verify password against credentials table
        if not verify_password(
            credential.password_hash,
            employee_data.password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid employee ID or password"
            )

        # Normal login
        credential.session_no += 1
        db.commit()
        db.refresh(credential)
        
        return {
            "employee_id": employee.employee_id,
            "first_name": employee.first_name,
            "middle_name": employee.middle_name,
            "last_name": employee.last_name,
            
            "email": employee.email,
            "phone": employee.phone,

            "date_of_birth": employee.date_of_birth,
            "gender": employee.gender,

            "address": employee.address,
            "city": employee.city,
            "state": employee.state,
            "postal_code": employee.postal_code,
            
            "department": employee.department,
            "designation": employee.designation,
            "employee_type": employee.employee_type,    
            "branch": employee.branch,
            "joining_date": employee.joining_date,
            "reporting_manager": employee.reporting_manager,
            
            "status": employee.status,
            "role": credential.role,
            "session_no": credential.session_no,
        }

    finally:
        db.close()

@app.post("/change-password/") #change password logic
def change_password(data: ChangePassword):

    db = SessionLocal()

    try:

        credential = (
            db.query(Credentials)
            .filter(
                Credentials.employee_id == data.employee_id
            )
            .first()
        )

        if not credential:
            raise HTTPException(
                status_code=404,
                detail="Employee credentials not found"
            )

        # Hash the new password
        hashed_password = hash_password(data.new_password)

        # Update password
        credential.password_hash = hashed_password

        db.commit()
        db.refresh(credential)

        return {
            "message": "Password changed successfully",
            "employee_id": credential.employee_id,
            "session_no": credential.session_no
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

@app.delete("/delete-employees/{employee_id}")
def remove_employee(employee_id: str):

    db = SessionLocal()

    try:

        employee = delete_employee(
            db=db,
            employee_id=employee_id
        )

        if not employee:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        return {
            "message": "Employee deleted successfully",
            "employee_id": employee_id
        }

    finally:

        db.close()