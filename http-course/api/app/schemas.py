from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class DepartmentIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=1, max_length=100)


class DepartmentOut(DepartmentIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class EmployeeIn(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    title: str = Field(min_length=1, max_length=100)
    department_id: int
    manager_id: int | None = None
    hire_date: date
    salary: float = Field(gt=0)


class EmployeePatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    title: str | None = Field(default=None, min_length=1, max_length=100)
    department_id: int | None = None
    manager_id: int | None = None
    hire_date: date | None = None
    salary: float | None = Field(default=None, gt=0)


class EmployeeOut(EmployeeIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
