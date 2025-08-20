from fastapi import FastAPI
from mangum import Mangum

from apps.authentication.routes import jose_auth, py_jwt_auth

app = FastAPI()
app.include_router(jose_auth.router)
app.include_router(py_jwt_auth.router)
headers = Mangum(app)


@app.get("/")
async def index():
    return {"response": "my test"}
