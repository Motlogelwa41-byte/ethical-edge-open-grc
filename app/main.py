from fastapi import FastAPI

app = FastAPI(title="Ethical Edge Open GRC")

@app.get("/")
def home():
    return {"message": "home"}

@app.get("/proof")
def proof():
    return {"message": "REAL FILE RUNNING"}
