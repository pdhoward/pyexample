from pydantic import BaseModel, validator
from datetime import datetime
import calendar
from math import gcd
from fastapi import Path

def get_today_day_number() -> int:
    return (datetime.now()-datetime.strptime(f"01/01/{datetime.now().year}", "%d/%m/%Y")).days+1

def is_coprime(val1, val2) -> bool:
    return gcd(val1, val2) == 1

class DayNumber(BaseModel):
    day_number:  int = Path(..., gt=0, lt=367, title="Day number of the present year")

    @validator('day_number')
    def daynumber_validation(cls, day_number):
        if (calendar.isleap(datetime.now().year) is False) and day_number > 365:
            raise  ValueError("Invalid Day Number")
        if (is_coprime(get_today_day_number(), day_number) is False):
            raise  ValueError("The current day-number isn't co-prime with passed day number.")
        return day_number