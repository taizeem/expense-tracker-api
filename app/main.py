from fastapi import FastAPI
from app.api.expenses import router as expenses_router


app = FastAPI(
    title= "Expense Tracker Api",
    version= "1.0.0"
)

@app.get("/")
def root():
    return {"message" : "Expense tracker api is running"}
app.include_router(expenses_router, prefix="/expenses")