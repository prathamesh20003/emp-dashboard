from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Employee, Credentials
from schemas import EmployeeCreate, EmployeeUpdate, CreateCredentials, LoginRequest
import string
import secrets
from argon2 import PasswordHasher

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

def get_all_employees(db: Session):
    return db.query(Employee).all()

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

def update_employee(db: Session,employee_data: EmployeeUpdate):
    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_data.employee_id)
        .first()
    )

    if not employee:
        return None

    employee = employee_data.model_dump(exclude_unset=True)

    db.commit()
    db.refresh(employee)

    return employee

def generate_temporary_password(length: int = 12):
    characters = (
        string.ascii_letters
        + string.digits
        + "!@#$%^&*"
    )
    return ''.join(secrets.choice(characters) for _ in range(length))

def hash_password(password: str):
    return ph.hash(password)

def find_employee(db: Session, id):
    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == id)
        .first()
    )

    if not employee:
        return None

    return employee

def verify_password(password, password_hash):
    return ph.verify(password, password_hash)

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