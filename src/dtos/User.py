from pydantic import BaseModel, validator


class User(BaseModel):
    phone: str
    @validator('phone')
    def phone_validator(cls, v):        
        if v and len(v) != 10 or not v.isdigit():
            raise ValueError('Invalid phone number')
        return v

print(User(phone='9145005391'))