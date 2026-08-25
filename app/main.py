import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def say_hello():
    return {"message": "Hello FastAPI 高级进阶"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)