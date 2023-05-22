app = FastAPI()

class SomeDto(BaseModel):
    data: str = Field(min_length=1, description="Minimum length must be greater than 1",
                      title="Minimum length must be greater than 1")
class User(BaseModel):
    phone: str

    @validator('phone')
    def phone_validator(cls, v):
        if v and len(v) != 9 or not v.isdigit():
            raise ValueError('Invalid phone number')
        return v
    
@app.post(path="/")
async def get_response(request: SomeDto):
    return "some response"

@app.exception_handler(RequestValidationError)
async def handle_error(request: Request, exc: RequestValidationError) -> PlainTextResponse:
    return PlainTextResponse(str(exc.errors()), status_code=400)


{
  "detail": [
    {
      "loc": [
        "body",
        "phone"
      ],
      "msg": "Invalid phone number",
      "type": "value_error"
    }
  ]
}