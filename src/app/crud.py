from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Employee
from schemas import EmployeeCreate, EmployeeUpdate

def create_employee(
    db: Session,
    employee_data: EmployeeCreate):

    employee = Employee(
        employee_id=employee_data.employee_id,
        first_name=employee_data.first_name,
        last_name=employee_data.last_name,
        email=employee_data.email,
        phone=employee_data.phone,
        department=employee_data.department,
        designation=employee_data.designation,
        branch=employee_data.branch,
        joining_date=employee_data.joining_date,
        status=employee_data.status
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

    employee.first_name = employee_data.first_name
    employee.last_name = employee_data.last_name
    employee.email = employee_data.email
    employee.phone = employee_data.phone
    employee.department = employee_data.department
    employee.designation = employee_data.designation
    employee.branch = employee_data.branch
    employee.joining_date = employee_data.joining_date
    employee.status = employee_data.status

    db.commit()
    db.refresh(employee)

    return employee 