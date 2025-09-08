from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from employees_routes import router as employees_router
from leaves_routes import router as leaves_router

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

@app.get("/")
async def root():
    return {
        "message": "Employee Management API",
        "endpoints": {
            "employees": "/employees",
            "leaves": "/leaves", 
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