from sqlalchemy import Column, Integer, String, Date, Float, DateTime
from datetime import date, datetime
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    
    employee_id = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)

    date_of_birth = Column(Date)
    gender = Column(String, default="")

    address = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)

    salary = Column(Float, default=0.0)
    
    department = Column(String)
    designation = Column(String)
    employee_type = Column(String, default="Full Time")
    branch = Column(String)
    joining_date = Column(Date)
    reporting_manager = Column(String)
    
    status = Column(String, default="active")
    role = Column(String, default="Employee")

class Credentials(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    
    employee_id = Column(String, unique=True, nullable=False)
    password_hash = Column(String, default="default")
    role = Column(String, default="Employee")
    session_no = Column(Integer, default=0)

class auditEmployee(Base):
    __tablename__ = "audit_employee_details"

    id = Column(Integer, primary_key=True, index=True)
    
    employee_id = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=True)
    last_name = Column(String, nullable=False)
    
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)

    date_of_birth = Column(Date)
    gender = Column(String, default="")

    address = Column(String)
    city = Column(String)
    state = Column(String)
    postal_code = Column(String)

    salary = Column(Float, default=0.0)
    
    department = Column(String)
    designation = Column(String)
    employee_type = Column(String, default="Full Time")
    branch = Column(String)
    joining_date = Column(Date)
    reporting_manager = Column(String)
    
    status = Column(String, default="Active")
    role = Column(String, default="Employee")

    audit_number = Column(String, default="0")
    audit_status = Column(String, default="Request Pending")
    audit_employee_id = Column(String)
    audit_operation = Column(String)

class Audit(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)

    audit_number = Column(String(50), unique=True, nullable=False, index=True)
    audit_date = Column(Date, nullable=False, default=date.today)
    audit_time = Column(DateTime, nullable=False, default=datetime.utcnow)

    audit_operation = Column(String(50), nullable=False)
    audit_status = Column(String(30), nullable=False, default="Request Pending")
    audit_employee_id = Column(String(50), nullable=False)

    target_employee_id = Column(String(50), nullable=False)

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)

    report_number = Column(String(50), unique=True, nullable=False, index=True)
    report_date = Column(Date, nullable=False, default=date.today)
    report_time = Column(DateTime, nullable=False, default=datetime.utcnow)

    report_operation = Column(String(50), nullable=False)
    report_status = Column(String(30), nullable=False, default="Request Pending")
    reporter_employee_id = Column(String(50), nullable=False)

    target_employee_id = Column(String(50), nullable=False)
    