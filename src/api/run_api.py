from fastapi import FastAPI
from src.api.category_routes import router as category_router
from src.api.payment_methods_routes import router as payment_methods_router
from src.api.expenses_routes import router as expenses_router
from dotenv import load_dotenv


load_dotenv()

app = FastAPI(
    title="Expense Tracker API",
    description="API for managing expenses",
    version="1.0.0",
    contact={
        "name": "Subash Pandey",
        "email": "axlesubash111@gmail.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

@app.get("/")
async def root():
    return {"message": "Welcome to the Expense Tracker API"}

app.include_router(category_router)
app.include_router(payment_methods_router)
app.include_router(expenses_router)

