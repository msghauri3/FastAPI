import pyodbc
from typing import Optional

def get_db_connection():
    connection = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=172.20.228.2;'
        'DATABASE=Payroll;'
        'UID=sa;'
        'PWD=Pakistan@786'
    )
    return connection