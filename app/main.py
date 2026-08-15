from fastapi import FastAPI

app = FastAPI(
    title= "Expense Tracker Api",
    version= "1.0.0"
)

@app.get("/")
def root():
    return {"message" : "Expense tracker api is running"}