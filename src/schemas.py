from pydantic import BaseModel
from datetime import date, datetime

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

class EmployeeRequest(BaseModel):
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

    audit_number: str = "0"
    audit_status: str = "Request Pending"
    audit_employee_id: str
    audit_operation: str

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

class AuditCreate(BaseModel):
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

        audit_number: str = "0"
        audit_status: str = "Request Pending"
        audit_employee_id: str
        audit_operation: str

class AuditApprove(BaseModel):
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

        audit_number: str = "0"
        audit_employee_id: str

class CreateAudit(BaseModel):
    audit_number: str
    audit_date: date
    audit_time: datetime
    audit_operation: str
    audit_status: str = "Request Pending"
    audit_employee_id: str

    target_employee_id: str 

class AuditMarkRequest(BaseModel):
    audit_number: str
    audit_status: str

class CreateLog(BaseModel):
    report_number: str
    report_date: date
    report_time: datetime
    report_operation: str
    report_status: str = "Request Pending"
    reporter_employee_id: str

    target_employee_id: str

    