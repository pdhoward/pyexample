from fastapi import FastAPI, Depends, Path

from datetime import datetime, timedelta
from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ValidationError
import json
from src.dtos.User import User
from src.dtos.DayNumber import DayNumber

app = FastAPI()

def daynumber_to_date(daynumber: int) -> int:
    return (datetime.strptime(f"01/01/{datetime.now().year}", "%d/%m/%Y")+timedelta(daynumber-1)).date()

@app.exception_handler(RequestValidationError)

@app.exception_handler(ValidationError)

async def validation_exception_handler(request, exc):
    print(f"YIKES! The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(error['loc'][-1]+f": {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

@app.post("/hello")
async def hello_message(dto: User):
    return {"message": f"Hello {dto.phone}"}

@app.get("/v1/api/date/{day_number}")
async def get_date(day_number: DayNumber=Depends(DayNumber)):
    response = {}
    day_number = day_number.day_number
    print(day_number,"DAY")
    response['data'] = daynumber_to_date(day_number)
    response['message'] = "Successfully Computed!"
    return response