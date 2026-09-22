from pyarrow import scalar
from pydantic import BaseModel
from datetime import date


class EmployeeCreate(BaseModel):
    employee_id: str
    first_name:str
    middle_name:str
    last_name:str
    
    email:str 
    phone:str | None

    date_of_birth: date
    gender: str | None = None

    address: str
    city: str
    state: str
    postal_code: str | None = None

    salary: float | None = None
    
    department:str 
    designation:str
    employee_type: str = "Full Time"
    branch:str
    joining_date: date 
    reporting_manager: str | None = None
    
    status: str = "Active"
    role: str = "Employee"


class CreateCredentials(BaseModel):
    employee_id: str
    password_hash: str = "default"
    role: str
    session_no: int = 0

class EmployeeUpdate(BaseModel):
    employee_id: str
    first_name:str
    middle_name:str
    last_name:str
    
    email:str 
    phone:str | None

    date_of_birth: date
    gender: str | None = None

    address: str
    city: str
    state: str
    postal_code: str | None = None

    salary: float | None = None
    
    department:str 
    designation:str
    employee_type: str = "Full Time"
    branch:str
    joining_date: date 
    reporting_manager: str | None = None
    
    status: str = "Active"
    role: str = "Employee"

class LoginRequest(BaseModel):
    employee_id: str
    password: str

class ChangePassword(BaseModel):
    employee_id: str
    new_password: str