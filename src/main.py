from fastapi import FastAPI
from src.routes.v1.towns import router 

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the home page!"}

app.include_router(router, prefix="/v1/towns")  
