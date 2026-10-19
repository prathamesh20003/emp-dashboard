#uv run uvicorn main:app --reload


from fastapi import FastAPI, HTTPException, Query
from database import SessionLocal, Base, engine
from schemas import EmployeeCreate,EmployeeRequest, EmployeeUpdate, CreateCredentials, LoginRequest,ChangePassword, AuditCreate, CreateAudit, CreateLog
from crud import (
    create_employee,
    create_audit,
    create_log,
    get_all_employees,
    update_employee,
    create_audit_request,
    get_active_employee_count,
    get_department_count,
    get_inactive_employee_count,
    get_total_employee_count,
    generate_temporary_password,
    hash_password,
    find_employee,
    verify_password,
    create_credential,
    delete_employee,
    generate_report_number,
    generate_audit_number
)
from models import Employee, Credentials, auditEmployee, Audit, Log
from datetime import date, datetime
from sqlalchemy import or_

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

@app.post("/add-audit-request/") #create audit
def add_audit_request(add_request: AuditCreate):

    db = SessionLocal()
    generated_audit_number = generate_audit_number()
    
    add_request.audit_number = generated_audit_number
    print(add_request)
    
    try:
        
        create_audit_request(
            db=db,
            employee_data=add_request
        )

        audit = CreateAudit(
        audit_number= generated_audit_number,
        audit_date= datetime.now().date(),
        audit_time= datetime.now(),
        
        audit_operation= "Add Request",
        audit_status= "Request Pending",
        audit_employee_id= add_request.audit_employee_id,
    
        target_employee_id=  add_request.employee_id,
        )

        create_audit(
            db=db,
            audit_data = audit
        )

        log_report_number = generate_report_number()
        log = CreateLog(
            report_number= log_report_number,
            report_date= datetime.now().date(),
            report_time= datetime.now(),
            
            report_operation= "Add Request",
            report_status= "Request Pending",
            reporter_employee_id= add_request.audit_employee_id,
    
            target_employee_id= add_request.employee_id
        )

        create_log(
            db,
            log_data = log
        )

        return {
                    "message": "Request to add employee sent",
                    "employee_id": add_request.employee_id
                }
        
    except Exception as e:

        db.rollback()
        print("employee audit adding error")

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )    
        
    finally:
        db.close()

@app.post("/add-employees/") #add employee
def add_employee(employee: EmployeeRequest):

    db = SessionLocal()
    
    try:

        employee_req = EmployeeCreate(
            employee_id=employee.employee_id,
            first_name=employee.first_name,
            middle_name=employee.middle_name,
            last_name=employee.last_name,
            email=employee.email,
            phone=employee.phone,
            date_of_birth=employee.date_of_birth,
            gender=employee.gender,
            address=employee.address,
            city=employee.city,
            state=employee.state,
            postal_code=employee.postal_code,
            salary=employee.salary,
            department=employee.department,
            designation=employee.designation,
            employee_type=employee.employee_type,
            branch=employee.branch,
            joining_date=employee.joining_date,
            reporting_manager=employee.reporting_manager,
            status=employee.status,
            role=employee.role,
        )
        
        new_employee = create_employee(
            db=db,
            employee_data = employee_req
        )

        password = generate_temporary_password()
        print(password)
        hashed_password = hash_password(password)

        credentials = {
            "employee_id": employee.employee_id,
            "password_hash": hashed_password,
            "role": employee.role,
            "session_no": 0
        }
        
        create_credential(
            db=db,
            credential_data = credentials
        )

        log_report_number = generate_report_number()
        log = CreateLog(
            report_number= log_report_number,
            report_date= datetime.now().date(),
            report_time= datetime.now(),
            
            report_operation= "Added Employee",
            report_status= "Request Pending",
            reporter_employee_id= employee.audit_employee_id,
    
            target_employee_id= employee.employee_id
        )
    
        create_log(
            db,
            log_data = log
        )
        
        return {
            "message": "Employee added successfully and password sent to email",
            "employee_id": new_employee.employee_id
        }

    except Exception as e:
        db.rollback()
        print("employee adding error")
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
    finally:
        db.close()

@app.get("/audits/")
def get_audits(
    search: str = "",
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)):
    db = SessionLocal()

    try:
        query = db.query(Audit)

        if search.strip():
            keyword = f"%{search.strip()}%"

            query = query.filter(
                or_(
                    Audit.audit_number.ilike(keyword),
                    Audit.audit_employee_id.ilike(keyword),
                    Audit.target_employee_id.ilike(keyword),
                    Audit.audit_operation.ilike(keyword),
                    Audit.audit_status.ilike(keyword),
                )
            )

        total = query.count()

        audits = (
            query
            .order_by(Audit.id.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        results = []

        for audit in audits:
            # Find the proposed employee data for this audit
            employee = (
                db.query(auditEmployee)
                .filter(
                    auditEmployee.audit_number == audit.audit_number
                )
                .first()
            )

            audit_data = {
                # Audit table fields
                "id": audit.id,
                "audit_number": audit.audit_number,
                "audit_date": audit.audit_date,
                "audit_time": audit.audit_time,
                "audit_operation": audit.audit_operation,
                "audit_status": audit.audit_status,
                "audit_employee_id": audit.audit_employee_id,
                "target_employee_id": audit.target_employee_id,

                # Proposed employee fields
                "employee": None,
            }

            if employee:
                audit_data["employee"] = {
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
                    "role": employee.role,
                    "audit_number": employee.audit_number,
                    "audit_status": employee.audit_status,
                    "audit_employee_id": employee.audit_employee_id,
                    "audit_operation": employee.audit_operation,
                }

            results.append(audit_data)

        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "audits": results,
        }

    finally:
        db.close()



@app.post("/audits/{audit_number}/approve")
def approve_audit_request(
    employee_data: EmployeeRequest):
        
    db = SessionLocal()

    employee_req = EmployeeCreate(
        employee_id=employee_data.employee_id,
        first_name=employee_data.first_name,
        middle_name=employee_data.middle_name,
        last_name=employee_data.last_name,
        email=employee_data.email,
        phone=employee_data.phone,
        date_of_birth=employee_data.date_of_birth,
        gender=employee_data.gender,
        address=employee_data.address,
        city=employee_data.city,
        state=employee_data.state,
        postal_code=employee_data.postal_code,
        salary=employee_data.salary,
        department=employee_data.department,
        designation=employee_data.designation,
        employee_type=employee_data.employee_type,
        branch=employee_data.branch,
        joining_date=employee_data.joining_date,
        reporting_manager=employee_data.reporting_manager,
        status=employee_data.status,
        role=employee_data.role,
    )
    try:
        audit = db.query(Audit).filter(
            Audit.audit_number == employee_data.audit_number
        ).first()
        if not audit:
            raise HTTPException(404, "Audit request not found")

        # must be pending
        if (audit.audit_status or "").lower() != "request pending":
            raise HTTPException(
                400, f"Audit already marked: {audit.audit_status}"
            )

        operation = (audit.audit_operation or "").lower()

        # ---- branch by operation ----
        if "add" in operation:
            existing = db.query(Employee).filter(
                Employee.employee_id == employee_req.employee_id
            ).first()
            if existing:
                raise HTTPException(400, "Employee already exists")


            create_employee(
                db=db,
                employee_data = employee_req
            )
    
            password = generate_temporary_password()
            print(password)
            hashed_password = hash_password(password)
    
            credentials = {
                "employee_id": employee_req.employee_id,
                "password_hash": hashed_password,
                "role": employee_req.role,
                "session_no": 0
            }
            
            create_credential(
                db=db,
                credential_data = credentials
            )
    
            log_report_number = generate_report_number()
            log = CreateLog(
                report_number= log_report_number,
                report_date= datetime.now().date(),
                report_time= datetime.now(),
                
                report_operation= "Added Employee",
                report_status= "Request Pending",
                reporter_employee_id= employee_data.audit_employee_id,
        
                target_employee_id= employee_data.employee_id
            )
        
            create_log(
                db,
                log_data = log
            )

            

        elif "update" in operation:
            existing = db.query(Employee).filter(
                Employee.employee_id == employee_data.employee_id
            ).first()
            if not existing:
                raise HTTPException(404, "Employee to update not found")

            
            update_employee(db=db, employee_data=employee_req)

        else:
            raise HTTPException(
                400, f"Unsupported operation: {audit.audit_operation}"
            )


    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        print("approve_audit error:", repr(e))
        raise HTTPException(400, str(e))
    finally:
        db.close()
        

@app.get("/logs/")
def get_logs(
    search: str = "",
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)):
    db = SessionLocal()

    try:
        query = db.query(Log)

        if search.strip():
            keyword = f"%{search.strip()}%"

            query = query.filter(
                or_(
                    Log.audit_number.ilike(keyword),
                    Log.audit_employee_id.ilike(keyword),
                    Log.target_employee_id.ilike(keyword),
                    Log.audit_operation.ilike(keyword),
                    Log.audit_status.ilike(keyword),
                )
            )

        total = query.count()

        logs = (
            query
            .order_by(Log.id.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "total": total,
            "offset": offset,
            "limit": limit,
            "logs": [
                {
                    "id": log.id,
                    "report_number": log.report_number,
                    "report_date": log.report_date,
                    "report_time": log.report_time,
                    "report_operation": log.report_operation,
                    "report_status": log.report_status,
                    "reporter_employee_id": log.reporter_employee_id,
                    "target_employee_id": log.target_employee_id,
                }
                for log in logs
            ],
        }
  
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
            "employee_id": employee.employee_id
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


@app.post("/update-audit-request/{employee_id}") #update employee details
def edit_employee_request(update_request: AuditCreate):

    db = SessionLocal()
    
    generated_audit_number = generate_audit_number()

    update_request.audit_number = generated_audit_number

    try:

        create_audit_request(
            db=db,
            employee_data=update_request
        )
        
        audit = CreateAudit(
        audit_number= generated_audit_number,
        audit_date= datetime.now().date(),
        audit_time= datetime.now(),
        
        audit_operation= "Update Employee",
        audit_status= "Request Pending",
        audit_employee_id= update_request.audit_employee_id,
    
        target_employee_id=  update_request.employee_id,
        )

        create_audit(
            db=db,
            audit_data = audit
        )

        log_report_number = generate_report_number()
        log = CreateLog(
            report_number= log_report_number,
            report_date= datetime.now().date(),
            report_time= datetime.now(),
            
            report_operation= "Update Employee",
            report_status= "Request Pending",
            reporter_employee_id= update_request.audit_employee_id,
    
            target_employee_id= update_request.employee_id
        )

        create_log(
            db,
            log_data = log
        )

        return{
            "detail": "update request added"
        }
        
        #print("updated_employee", employee.employee_id)

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

        hashed_password = hash_password(data.new_password)

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
