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
from passlib.context import CryptContext
from starlette.middleware.sessions import SessionMiddleware


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


app = FastAPI()
templates = Jinja2Templates(directory="templates")

password = "local"
DATABASE_URL = (
    f"mysql+pymysql://root:{password}@localhost/win_db"  # MySQL 데이터베이스 URL
)
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()


# fmt: off
class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'comment': '사용자 정보'}

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, comment='사용자 ID')
    email: Mapped[str] = mapped_column(VARCHAR(100), unique=True, comment='이메일')
    full_name: Mapped[str] = mapped_column(VARCHAR(100), comment='이름')
    hashed_password: Mapped[str] = mapped_column(Text, comment='해시된 비밀번호')

class EtcCountryCode(Base):
    __tablename__ = 'etc__country_code'
    __table_args__ = {'comment': '국가부호정보'}

    country_code_2char: Mapped[str] = mapped_column(VARCHAR(2), primary_key=True, comment='국가부호_2자리')
    country_code_3char: Mapped[str] = mapped_column(VARCHAR(3), primary_key=True, comment='국가부호_3자리')
    country_name_kr: Mapped[str] = mapped_column(VARCHAR(100), comment='국가명_한글')
    country_name_en: Mapped[str] = mapped_column(VARCHAR(100), comment='국가명_영문')
    country_code_numeric: Mapped[Optional[int]] = mapped_column(Integer, comment='국가코드_숫자')

class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str

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

class CountryCodeRead(BaseModel):
    country_code_2char: str
    country_code_3char: str
    country_name_kr: str
    country_name_en: str
    country_code_numeric: Optional[int] = None


# fmt: on


def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


Base.metadata.create_all(bind=engine)


# TODO: 회원가입
# TODO: 로그인
# TODO: 로그아웃


@app.get("/")
def read_root():
    return templates.TemplateResponse("home.html", {"request": {}})


@app.get("/about")
def read_about():
    return templates.TemplateResponse("about.html", {"request": {}})


@app.get("/country-codes/", response_model=List[CountryCodeRead])
def read_country_codes(search_country_name: str, db: Session = Depends(get_db)):
    query = db.query(EtcCountryCode)
    if search_country_name:
        query = query.filter(
            EtcCountryCode.country_name_kr.ilike(f"%{search_country_name}%")
        )
    country_codes = query.all()
    return country_codes


@app.post("/country-codes/")
def create_country_code(country_code: CountryCodeCreate, db: Session = Depends(get_db)):
    db_country_code = EtcCountryCode(**country_code.model_dump())
    print(f"Creating country code: {db_country_code}")
    db.add(db_country_code)
    db.commit()
    db.refresh(db_country_code)
    return db_country_code


@app.put("/country-codes/{country_code_2char}")
def update_country_code(
    country_code_2char: str,
    country_code: CountryCodeUpdate,
    db: Session = Depends(get_db),
):
    db_country_code = (
        db.query(EtcCountryCode)
        .filter(EtcCountryCode.country_code_2char == country_code_2char)
        .first()
    )
    if not db_country_code:
        return {"error": "Country code not found"}
    for key, value in country_code.model_dump().items():
        if value is not None:
            setattr(db_country_code, key, value)
    db.commit()
    db.refresh(db_country_code)
    return db_country_code


@app.delete("/country-codes/{country_code_2char}")
def delete_country_code(
    country_code_2char: str,
    db: Session = Depends(get_db),
):
    db_country_code = (
        db.query(EtcCountryCode)
        .filter(EtcCountryCode.country_code_2char == country_code_2char)
        .first()
    )
    if not db_country_code:
        return {"error": "Country code not found"}
    db.delete(db_country_code)
    db.commit()
    return {"message": "Country code deleted successfully"}
