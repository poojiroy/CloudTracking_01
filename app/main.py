from fastapi import FastAPI
from connect import test_connection

app = FastAPI()

@app.get("/")
def root():
    try:
        test_connection()
        return {"message": "Database connection successful!"}
    except Exception as e:
        return {"message": f"Database connection failed: {e}"}
