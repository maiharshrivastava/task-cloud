from fastapi import FastAPI
from route import router

app = FastAPI(title="Student Management System", version="1.0.0")

# Register the router
app.include_router(router)
