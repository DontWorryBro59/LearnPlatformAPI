import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager

from myapp.database.database_con import create_db
from myapp.routes.users import users



@asynccontextmanager
async def lifespan(app: FastAPI):
    print('[Start Function] Checking and creating table in database if not exist')
    await create_db()
    yield
    print('The API server has been down')

app = FastAPI(lifespan=lifespan)

app.include_router(users)

@app.get("/")
async def root():
    return {"message": "Server is running"}



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
