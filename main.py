from fastapi import Depends, FastAPI
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session, declarative_base, Mapped, mapped_column
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Text,
    VARCHAR,
)
from pydantic import BaseModel
from typing import List, Optional


app = FastAPI()
templates = Jinja2Templates(directory="templates")

password = "local"
DATABASE_URL = (
    f"mysql+pymysql://root:{password}@localhost/fastapi_db"  # MySQL 데이터베이스 URL
)
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()


# fmt: off
class EtcCountryCode(Base):
    __tablename__ = 'etc__country_code'
    __table_args__ = {'comment': '국가부호정보'}

    country_code_2char: Mapped[str] = mapped_column(VARCHAR(2), primary_key=True, comment='국가부호_2자리')
    country_code_3char: Mapped[str] = mapped_column(VARCHAR(3), primary_key=True, comment='국가부호_3자리')
    country_name_kr: Mapped[str] = mapped_column(VARCHAR(100), comment='국가명_한글')
    country_name_en: Mapped[str] = mapped_column(VARCHAR(100), comment='국가명_영문')
    country_code_numeric: Mapped[Optional[int]] = mapped_column(Integer, comment='국가코드_숫자')

class CountryCodeCreate(BaseModel):
    country_code_2char: str
    country_code_3char: str
    country_name_kr: str
    country_name_en: str
    country_code_numeric: Optional[int] = None 
    
class CountryCodeUpdate(BaseModel):
    country_code_2char: Optional[str] = None
    country_code_3char: Optional[str] = None
    country_name_kr: Optional[str] = None
    country_name_en: Optional[str] = None
    country_code_numeric: Optional[int] = None

    @classmethod
    def validate_one_of_two(cls, values):
        if not (values.get('country_code_2char') or values.get('country_code_3char')):
            raise ValueError('country_code_2char 또는 country_code_3char 중 하나는 필수입니다.')
        return values

    _validate_one_of_two = __import__('pydantic').root_validator(pre=True, allow_reuse=True)(validate_one_of_two)

# fmt: on


def get_db():

    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return templates.TemplateResponse("home.html", {"request": {}})


@app.get("/about")
def read_about():
    return templates.TemplateResponse("about.html", {"request": {}})


@app.post("/country-codes/")
def create_country_code(country_code: CountryCodeCreate, db: Session = Depends(get_db)):
    db_country_code = EtcCountryCode(**country_code.dict())
    print(f"Creating country code: {db_country_code}")
    db.add(db_country_code)
    db.commit()
    db.refresh(db_country_code)
    return db_country_code
