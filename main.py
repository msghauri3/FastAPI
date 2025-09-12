from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from employees_routes import router as employees_router
from leaves_routes import router as leaves_router
from allowance_routes import router as allowance_router
from configuration_routes import router as configuration_router
from deductions_routes import router as deductions_router
from departments_routes import router as departments_router
from salary_payment_routes import router as salary_payment_router
from taxslab_routes import router as taxslabs_router
from login_routes import router as login_router 
from user_routes import router as users_router 
from employee_leave_summary_routes import router as leave_summary_router
from employee_tax_routes import router as employee_tax_router
from gazetted_holidays_routes import router as gazetted_holidays_router
from leave_quota_routes import router as leave_quota_router
from promotion_routes import router as promotion_router


app = FastAPI(title="Employee Management API", version="1.0.0")

# Configure CORS middleware
origins = [
    "http://localhost:3000",
    "http://172.20.228.2:3000",
    "http://localhost:8000",
    "http://172.20.228.2:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(employees_router)
app.include_router(leaves_router)
app.include_router(allowance_router)
app.include_router(configuration_router)
app.include_router(deductions_router)
app.include_router(departments_router)
app.include_router(salary_payment_router)
app.include_router(taxslabs_router)
app.include_router(login_router)   
app.include_router(users_router)
app.include_router(leave_summary_router)
app.include_router(employee_tax_router)
app.include_router(gazetted_holidays_router)
app.include_router(leave_quota_router)
app.include_router(promotion_router)


@app.get("/")
async def root():
    return {
        "message": "Employee Management API",
        "endpoints": {
            "employees": "/employees",
            "leaves": "/leaves", 
            "allowance": "/allowance", 
             "configuration": "/configuration", 
             "deductions": "/deductions",
             "departments": "/departments",
             "salary-payments": "/salary-payments",
             "taxslabs": "/taxslabs",  
              "logins": "/logins",
                 "users": "/users",

            "leaves": "/leaves",
            "allowance": "/allowance",
            "configuration": "/configuration",
            "deductions": "/deductions",
            "departments": "/departments",
            "leave-summary": "/leave-summary",  
            "employee-tax": "/employee-tax",
            "gazetted-holidays": "/gazetted-holidays",
            "leave-quota": "/leave-quota",
            "promotions": "/promotions",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0",
        port=8000,
        reload=False
    )