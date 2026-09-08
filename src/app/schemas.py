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


class EmployeeUpdate(BaseModel):
    first_name: str
    last_name: str 
    email: str
    phone: str | None 
    department: str
    designation: str
    branch: str
    joining_date: date
    status: str