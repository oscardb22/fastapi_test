from fastapi import FastAPI
from mangum import Mangum


app = FastAPI()
headers = Mangum(app)

@app.get("/")
async def index():
    return {"response": "my test"}
