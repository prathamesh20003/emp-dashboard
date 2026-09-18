from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.sql.crud import roles
from database import Base

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    
    employee_id = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    department = Column(String)
    designation = Column(String)
    branch = Column(String)
    joining_date = Column(Date)
    status = Column(String, default="active")
    role = Column(String, default="Employee")

class Credentials(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    
    employee_id = Column(String, unique=True, nullable=False)
    password_hash = Column(String, default="default")
    role = Column(String, default="Employee")
    session_no = Column(Integer, default=0)