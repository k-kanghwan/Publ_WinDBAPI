from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from models.models import EtcCountryCode, User
from schemas.country_code import CountryCodeCreate, CountryCodeRead, CountryCodeUpdate
from dependencies.dependencies import get_db, get_password_hash, verify_password
from schemas.user import UserCreate, UserLogin

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def read_root():
    return templates.TemplateResponse("home.html", {"request": {}})


@router.get("/about")
def read_about():
    return templates.TemplateResponse("about.html", {"request": {}})


@router.get("/country-codes/", response_model=List[CountryCodeRead])
def read_country_codes(search_country_name: str, db: Session = Depends(get_db)):
    query = db.query(EtcCountryCode)
    if search_country_name:
        query = query.filter(
            EtcCountryCode.country_name_ko.ilike(f"%{search_country_name}%")
        )
    country_codes = query.all()
    return country_codes


@router.get("/country-codes/{first_char}")
def search_country_code(
    request: Request, first_char: str, db: Session = Depends(get_db)
):
    country_codes = (
        db.query(EtcCountryCode)
        .filter(EtcCountryCode.country_code_2char.ilike(f"%{first_char}%"))
        .all()
    )
    if not country_codes:
        raise HTTPException(status_code=404, detail="Country code not found")
    return templates.TemplateResponse(
        "result.html", {"request": request, "result": country_codes}
    )


@router.post("/country-codes/")
def create_country_code(country_code: CountryCodeCreate, db: Session = Depends(get_db)):
    db_country_code = EtcCountryCode(**country_code.model_dump())
    print(f"Creating country code: {db_country_code}")
    db.add(db_country_code)
    db.commit()
    db.refresh(db_country_code)
    return db_country_code


@router.put("/country-codes/{country_code_2char}")
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


@router.delete("/country-codes/{country_code_2char}")
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


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login")
async def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    else:
        request.session["user_id"] = db_user.id
        return {"message": "Login successful"}


@router.post("/logout")
async def logout(request: Request):
    request.session.pop("user_id", None)
    return {"message": "Logout successful"}


@router.get("/get_curr_user")
async def get_curr_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"user_id": user_id}
