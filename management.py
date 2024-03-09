from fastapi import FastAPI, HTTPException
from typing import Dict, List
from pydantic import BaseModel
from pymongo import MongoClient
import pytest
from fastapi.testclient import TestClient

# Creating an instance of FastAPI
app = fastapi_instance_for_employee_management_system = FastAPI()

# Defining a Pydantic model for Employee details
class EmployeeDetails(BaseModel):
    employee_name: str
    employee_id: str
    employee_title: str
    employee_department: str

# Defining a Pydantic model for Department details
class DepartmentDetails(BaseModel):
    department_name: str
    department_employees: List[EmployeeDetails] = []


company_information: Dict[str, DepartmentDetails] = {}

# Connecting to MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["employee_management_system"]
employees_collection = mongo_db["employees"]

# Function to add an employee to MongoDB
def add_employee_to_mongodb(employee_details: EmployeeDetails):
    employees_collection.insert_one(employee_details.dict())

# Function to remove an employee from MongoDB
def remove_employee_from_mongodb(employee_id: str):
    employees_collection.delete_one({"employee_id": employee_id})

# Function to list all employees in MongoDB
def list_all_employees_in_mongodb():
    return list(employees_collection.find())

# Function to add a department to the company
def add_department_to_company(department_name: str):
    """
    This function adds a new department to the company.

    Parameters:
    - department_name (str): The name of the new department.

    Raises:
    - HTTPException: If the department already exists.
    """
    if department_name not in company_information:
        company_information[department_name] = DepartmentDetails(department_name=department_name)
    else:
        raise HTTPException(status_code=400, detail="Department already exists")

# Function to remove a department from the company
def remove_department_from_company(department_name: str):
    """
    This function removes a department from the company.

    Parameters:
    - department_name (str): The name of the department to be removed.

    Raises:
    - HTTPException: If the department does not exist.
    """
    if department_name in company_information:
        del company_information[department_name]
    else:
        raise HTTPException(status_code=404, detail="Department not found")

# API endpoint to add an employee to MongoDB
@fastapi_instance_for_employee_management_system.post("/employee/add")
async def add_employee_to_mongodb_api(employee: EmployeeDetails):
    add_employee_to_mongodb(employee)
    return {"message": f"Employee {employee.employee_name} added"}

# API endpoint to remove an employee from MongoDB
@fastapi_instance_for_employee_management_system.delete("/employee/remove/{employee_id}")
async def remove_employee_from_mongodb_api(employee_id: str):
    remove_employee_from_mongodb(employee_id)
    return {"message": f"Employee with ID {employee_id} removed"}

# API endpoint to get all employees from MongoDB
@fastapi_instance_for_employee_management_system.get("/employees")
async def get_all_employees_from_mongodb_api():
    return {"employees": list_all_employees_in_mongodb()}

# API endpoint to update an employee in MongoDB
@fastapi_instance_for_employee_management_system.put("/employee/update/{employee_id}")
async def update_employee_in_mongodb_api(employee_id: str, employee_details: EmployeeDetails):
    remove_employee_from_mongodb(employee_id)
    add_employee_to_mongodb(employee_details)
    return {"message": f"Employee with ID {employee_id} updated"}

# Unit Tests
@pytest.fixture
def test_client_instance():
    with TestClient(fastapi_instance_for_employee_management_system) as test_client_instance:
        yield test_client_instance

# Unit test for adding an employee to MongoDB
def test_add_employee_to_mongodb_api(test_client_instance):
    employee = {"employee_name": "John Doe", "employee_id": "123", "employee_title": "Software Engineer", "employee_department": "Engineering"}
    response = test_client_instance.post("/employee/add", json=employee)
    assert response.status_code == 200
    assert response.json() == {"message": "Employee John Doe added"}

# Unit test for removing an employee from MongoDB
def test_remove_employee_from_mongodb_api(test_client_instance):
    response = test_client_instance.delete("/employee/remove/123")
    assert response.status_code == 200
    assert response.json() == {"message": "Employee with ID 123 removed"}

# Unit test for getting all employees from MongoDB
def test_get_all_employees_from_mongodb_api(test_client_instance):
    response = test_client_instance.get("/employees")
    assert response.status_code == 200
    assert "employees" in response.json()
