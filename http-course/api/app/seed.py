from datetime import date

from sqlalchemy.orm import Session

from .models import Department, Employee

DEPARTMENTS = [
    ("Human Resources", "Pleasanton"),
    ("Engineering", "San Jose"),
    ("Finance", "Pleasanton"),
    ("Sales", "Austin"),
]

# (name, title, department, manager name or None, hire date, salary)
EMPLOYEES = [
    ("Priya Raman", "Head of HR", "Human Resources", None, date(2015, 3, 2), 185000),
    ("Marcus Lee", "Engineering Director", "Engineering", "Priya Raman", date(2016, 6, 13), 210000),
    ("Elena Garcia", "Finance Director", "Finance", "Priya Raman", date(2017, 1, 9), 195000),
    ("Tom Becker", "Sales Director", "Sales", "Priya Raman", date(2017, 9, 18), 190000),
    ("Aisha Khan", "HR Generalist", "Human Resources", "Priya Raman", date(2019, 4, 22), 82000),
    ("Daniel Wu", "Recruiter", "Human Resources", "Priya Raman", date(2021, 2, 1), 76000),
    ("Sofia Rossi", "Senior Engineer", "Engineering", "Marcus Lee", date(2018, 5, 7), 165000),
    ("Ravi Patel", "Engineer", "Engineering", "Marcus Lee", date(2020, 8, 24), 135000),
    ("Hannah Cole", "Engineer", "Engineering", "Marcus Lee", date(2021, 10, 4), 128000),
    ("Omar Hassan", "QA Engineer", "Engineering", "Marcus Lee", date(2022, 1, 17), 112000),
    ("Grace Kim", "DevOps Engineer", "Engineering", "Marcus Lee", date(2022, 7, 11), 140000),
    ("Lucas Meyer", "Accountant", "Finance", "Elena Garcia", date(2019, 11, 4), 88000),
    ("Nina Petrova", "Financial Analyst", "Finance", "Elena Garcia", date(2020, 3, 16), 97000),
    ("James O'Neil", "Payroll Specialist", "Finance", "Elena Garcia", date(2021, 6, 28), 79000),
    ("Mei Chen", "Account Executive", "Sales", "Tom Becker", date(2019, 2, 11), 92000),
    ("Carlos Mendes", "Account Executive", "Sales", "Tom Becker", date(2020, 9, 7), 90000),
    ("Zara Ahmed", "Sales Development Rep", "Sales", "Tom Becker", date(2022, 4, 4), 64000),
    ("Ben Foster", "Sales Development Rep", "Sales", "Tom Becker", date(2023, 1, 23), 62000),
    ("Leah Brooks", "Customer Success Manager", "Sales", "Tom Becker", date(2021, 12, 6), 85000),
    ("Arjun Nair", "Junior Engineer", "Engineering", "Sofia Rossi", date(2023, 6, 12), 105000),
]


def seed_if_empty(db: Session) -> None:
    if db.query(Department).count() > 0:
        return
    depts = {}
    for name, location in DEPARTMENTS:
        d = Department(name=name, location=location)
        db.add(d)
        depts[name] = d
    db.flush()

    by_name: dict[str, Employee] = {}
    for name, title, dept, manager, hired, salary in EMPLOYEES:
        email = name.lower().replace("'", "").replace(" ", ".") + "@example.com"
        e = Employee(
            name=name,
            email=email,
            title=title,
            department_id=depts[dept].id,
            manager_id=by_name[manager].id if manager else None,
            hire_date=hired,
            salary=salary,
        )
        db.add(e)
        db.flush()
        by_name[name] = e
    db.commit()
