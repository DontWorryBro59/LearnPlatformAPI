from fastapi import FastAPI
import uvicorn

from routes.users import users
app = FastAPI()

app.include_router(users)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)