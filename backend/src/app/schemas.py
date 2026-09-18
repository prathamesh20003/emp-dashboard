from pydantic import BaseModel
from datetime import date

from sqlalchemy.sql.crud import roles

class EmployeeCreate(BaseModel):
    employee_id: str
    first_name:str
    last_name:str
    email:str 
    phone:str | None
    department:str 
    designation:str 
    branch:str
    joining_date: date 
    status: str = "Active"
    role: str = "Employee"


class Credentials(BaseModel):
    employee_id: str
    password_hash: str = "default"
    role: str
    session_no: int = 0

class EmployeeUpdate(BaseModel):
    employee_id: str
    first_name: str
    last_name: str 
    email: str
    phone: str | None 
    department: str
    designation: str
    branch: str
    joining_date: date
    status: str

class LoginRequest(BaseModel):
    employee_id: str
    password: str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str