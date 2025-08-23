from fastapi import FastAPI
from app.routers import (client, 
                                 vendor)

app = FastAPI()

app.include_router(client.router, prefix="/client")
app.include_router(vendor.router, prefix="/vendor")


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
