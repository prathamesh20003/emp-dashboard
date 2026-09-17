from pydantic import BaseModel
from datetime import date

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
    password_hash: str = "default"
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

class LoginEmployee(BaseModel):
    employee_id: str
    password: str

class ChangePassword(BaseModel):
    current_password: str
    new_password: str