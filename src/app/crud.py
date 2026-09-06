from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Employee


def create_employee(
    db: Session,
    employee_id,
    first_name,
    last_name,
    email,
    phone,
    department,
    designation,
    branch,
    joining_date,
    status
):

    employee = Employee(
        employee_id=employee_id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        department=department,
        designation=designation,
        branch=branch,
        joining_date=joining_date,
        status=status
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


def update_employee(
    db: Session,
    employee_id,
    first_name,
    last_name,
    email,
    phone,
    department,
    designation,
    branch,
    joining_date,
    status
):
    employee = (
        db.query(Employee)
        .filter(Employee.employee_id == employee_id)
        .first()
    )

    if not employee:
        return None

    employee.first_name = first_name
    employee.last_name = last_name
    employee.email = email
    employee.phone = phone
    employee.department = department
    employee.designation = designation
    employee.branch = branch
    employee.joining_date = joining_date
    employee.status = status

    db.commit()
    db.refresh(employee)

    return employee 