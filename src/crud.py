from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Employee, Credentials, AuditEmployee, Audit, Log
from schemas import EmployeeCreate, EmployeeUpdate, CreateCredentials, LoginRequest, AuditCreate, CreateAudit, CreateLog, AuditMarkRequest
import string
import secrets
from argon2 import PasswordHasher
from secrets import token_hex
from datetime import date, datetime

ph = PasswordHasher()
   
 
def create_credential(db: Session, credential_data):
    
    credential = Credentials(
        employee_id=credential_data["employee_id"],
        password_hash=credential_data["password_hash"],
        role=credential_data["role"],
        session_no=credential_data["session_no"]
    )

    db.add(credential)
    db.commit()
    db.refresh(credential)

    return credential

def create_audit_request(db: Session, employee_data: AuditCreate):  
    audit_employee = AuditEmployee(
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

        audit_number = employee_data.audit_number,
        audit_status= employee_data.audit_status,
        audit_employee_id= employee_data.audit_employee_id,
        audit_operation = employee_data.audit_operation
        
    )

    db.add(audit_employee)
    db.commit()
    db.refresh(audit_employee)

    return audit_employee

def create_employee(db: Session, employee_data: EmployeeCreate):    
    employee = Employee(
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
        role=employee_data.role
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee

def update_employee(db: Session, employee_data: EmployeeUpdate):
    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_data.employee_id)
        .first()
    )

    if not employee:
        return None

    # Convert the Pydantic model to a dictionary
    update_data = employee_data.model_dump(exclude_unset=True)

    # Update the SQLAlchemy model attributes
    for key, value in update_data.items():
        if key != "employee_id":
            setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee

def create_audit(db: Session, audit_data:CreateAudit):
    audit = Audit(
        audit_number = audit_data.audit_number,
        audit_date = audit_data.audit_date,
        audit_time = audit_data.audit_time,
    
        audit_operation = audit_data.audit_operation,
        audit_status = audit_data.audit_status,
        audit_employee_id = audit_data.audit_employee_id,
    
        target_employee_id = audit_data.target_employee_id
    )

    db.add(audit)
    db.commit()
    db.refresh(audit)

def create_log(db: Session, log_data:CreateLog):
    log = Log(
        report_number= log_data.report_number,
        report_date= log_data.report_date,
        report_time= log_data.report_time,
        
        report_operation= log_data.report_operation,
        report_status= log_data.report_status,
        reporter_employee_id= log_data.reporter_employee_id,

        target_employee_id= log_data.target_employee_id
    )

    db.add(log)
    db.commit()
    db.refresh(log)

def delete_employee(db: Session, employee_id: str):
    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    if not employee:
        return None

    db.delete(employee)
    db.commit()

    return employee

def mark_audit(db: Session, marked_data: AuditMarkRequest):
    audit = (
        db.query(Audit)
        .filter(Audit.audit_number == marked_data.audit_number)
        .first()
    )
    if not audit:
        return None

    audit_employee = (
        db.query(AuditEmployee)
        .filter(AuditEmployee.audit_number == marked_data.audit_number)
        .first()
    )
    if not audit_employee:
        return None

    audit.audit_status = marked_data.audit_status
    audit_employee.audit_status = marked_data.audit_status

    db.commit()
    db.refresh(audit)
    db.refresh(audit_employee)

    return "audit status changed"

def generate_report_number():
    date_part = datetime.now().strftime("%Y%m%d")
    unique_part = token_hex(4).upper()
    return f"REP-{date_part}-{unique_part}"

def generate_audit_number():
    date_part = datetime.now().strftime("%Y%m%d")
    unique_part = token_hex(4).upper()
    return f"AUD-{date_part}-{unique_part}"

def generate_temporary_password(length: int = 12):
    characters = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*"
    )
    return ''.join(secrets.choice(characters) for _ in range(length))

def hash_password(password: str):
    return ph.hash(password)

def verify_password(password, password_hash):
    return ph.verify(password, password_hash)

def get_all_employees(db: Session):
    return db.query(Employee).all()

def find_employee(db: Session, id):
    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == id)
        .first()
    )

    if not employee:
        return None

    return employee

def get_total_employee_count(db: Session):
    return db.query(Employee).count()

def get_active_employee_count(db: Session):
    return (
        db.query(Employee)
        .filter(Employee.status == "Active")
        .count()
    )

def get_inactive_employee_count(db: Session):
    return (
        db.query(Employee)
        .filter(Employee.status == "Inactive")
        .count()
    )

def get_department_count(db: Session):
    return (
        db.query(func.count(func.distinct(Employee.department)))
        .scalar()
    )