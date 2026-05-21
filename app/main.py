from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from datetime import datetime
import os
import subprocess

app = FastAPI(title="Fintech Secure CI/CD Lab")

# Vulnerabilidad intencional: credenciales hardcodeadas para laboratorio AppSec.
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

# Secretos simulados no reales para laboratorio.
DATABASE_PASSWORD = "LabPasswordForTraining123"
APP_DEBUG_TOKEN = "LabDebugTokenForTraining123"


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
        "status": "running",
        "security_note": "Intentional vulnerable lab for AppSec/DevSecOps training"
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
    # Vulnerabilidad intencional: Broken Access Control.
    user = users.get(username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user": username,
        "balance": user["balance"]
    }


@app.post("/api/transfer")
def transfer(data: TransferRequest):
    # Vulnerabilidad intencional: el backend confía en from_user enviado por el cliente.
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
    # Vulnerabilidad intencional: exposición de transacciones sin autenticación.
    return transactions


@app.get("/debug/config")
def debug_config():
    # Vulnerabilidad intencional: endpoint debug expone datos sensibles.
    return {
        "debug": True,
        "database_password": DATABASE_PASSWORD,
        "debug_token": APP_DEBUG_TOKEN
    }


@app.get("/debug/env")
def debug_env():
    # Vulnerabilidad intencional: exposición de variables de entorno.
    return dict(os.environ)


@app.get("/debug/ping")
def debug_ping(host: str = Query(...)):
    # Vulnerabilidad intencional: command injection por shell=True.
    command = f"ping -c 1 {host}"
    output = subprocess.check_output(command, shell=True, text=True)
    return {
        "command": command,
        "output": output
    }


@app.get("/vulnerable/search")
def vulnerable_search(q: str = Query("")):
    # Vulnerabilidad intencional: refleja entrada del usuario.
    html = f"""
    <html>
        <head>
            <title>Search</title>
        </head>
        <body>
            <h1>Search result</h1>
            <p>You searched for: {q}</p>
        </body>
    </html>
    """
    return {"html": html}
