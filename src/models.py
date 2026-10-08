from sqlalchemy import Column, Integer, String, Date, Float
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