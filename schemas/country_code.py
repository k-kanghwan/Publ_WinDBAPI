from pydantic import BaseModel, Field
from typing import Optional


class CountryCodeCreate(BaseModel):
    country_code_2char: str = Field(..., example="KR", max_length=2)
    country_code_3char: str = Field(..., example="KOR", max_length=3)
    country_name_ko: str = Field(..., example="대한민국", max_length=100)
    country_name_en: str = Field(..., example="South Korea", max_length=100)
    country_code_numeric: Optional[int] = Field(..., example=410)


class CountryCodeUpdate(BaseModel):
    country_code_2char: Optional[str] = None
    country_code_3char: Optional[str] = None
    country_name_ko: Optional[str] = None
    country_name_en: Optional[str] = None
    country_code_numeric: Optional[int] = None

    @classmethod
    def validate_one_of_two(cls, values):
        if not (values.get("country_code_2char") or values.get("country_code_3char")):
            raise ValueError(
                "country_code_2char 또는 country_code_3char 중 하나는 필수입니다."
            )
        return values

    _validate_one_of_two = __import__("pydantic").root_validator(
        pre=True, allow_reuse=True
    )(validate_one_of_two)


class CountryCodeRead(BaseModel):
    country_code_2char: str
    country_code_3char: str
    country_name_ko: str
    country_name_en: str
    country_code_numeric: Optional[int] = None
