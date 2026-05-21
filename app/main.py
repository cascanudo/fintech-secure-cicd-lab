from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="Fintech Secure CI/CD Lab")

users = {
    "juan": {
        "password": "admin123",
        "balance": 1500.00
    },
    "maria": {
        "password": "user123",
        "balance": 900.00
    }
}

transactions = []


class LoginRequest(BaseModel):
    username: str
    password: str


class TransferRequest(BaseModel):
    from_user: str
    to_account: str
    amount: float


@app.get("/")
def home():
    return {
        "message": "Fintech Secure CI/CD Lab",
        "status": "running"
    }


@app.post("/login")
def login(data: LoginRequest):
    user = users.get(data.username)

    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "message": "Login successful",
        "user": data.username
    }


@app.get("/balance/{username}")
def get_balance(username: str):
    user = users.get(username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user": username,
        "balance": user["balance"]
    }


@app.post("/api/transfer")
def transfer(data: TransferRequest):
    user = users.get(data.from_user)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    if user["balance"] < data.amount:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    user["balance"] -= data.amount

    transaction = {
        "from_user": data.from_user,
        "to_account": data.to_account,
        "amount": data.amount,
        "date": datetime.utcnow().isoformat()
    }

    transactions.append(transaction)

    return {
        "message": "Transfer completed",
        "transaction": transaction
    }


@app.get("/transactions")
def list_transactions():
    return transactions
