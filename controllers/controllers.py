from sqlalchemy import select
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
async def read_root():
    return templates.TemplateResponse("home.html", {"request": {}})


@router.get("/about")
async def read_about():
    return templates.TemplateResponse("about.html", {"request": {}})


@router.get("/country-codes/", response_model=List[CountryCodeRead])
async def read_country_codes(country_name_filter: str, db: Session = Depends(get_db)):
    result = await db.execute(
        select(EtcCountryCode).where(
            EtcCountryCode.country_name_ko.ilike(f"%{country_name_filter}%")
        )
    )
    country_codes = result.scalars().all()
    return country_codes
    # query = db.query(EtcCountryCode)
    # if search_country_name:
    #     query = query.filter(
    #         EtcCountryCode.country_name_ko.ilike(f"%{search_country_name}%")
    #     )
    # country_codes = query.all()
    # return country_codes


@router.get("/country-codes/{first_char}")
async def search_country_code(
    request: Request, first_char: str, db: Session = Depends(get_db)
):
    stmt = select(EtcCountryCode).where(
        EtcCountryCode.country_code_2char.ilike(f"%{first_char}%")
    )
    result = await db.execute(stmt)
    country_codes = result.scalars().all()
    if not country_codes:
        raise HTTPException(status_code=404, detail="Country code not found")
    return templates.TemplateResponse(
        "result.html", {"request": request, "result": country_codes}
    )


@router.post("/country-codes/")
async def create_country_code(
    country_code: CountryCodeCreate, db: Session = Depends(get_db)
):
    db_country_code = EtcCountryCode(**country_code.model_dump())
    print(f"Creating country code: {db_country_code}")
    db.add(db_country_code)
    db.commit()
    db.refresh(db_country_code)
    return db_country_code


@router.put("/country-codes/{country_code_2char}")
async def update_country_code(
    country_code_2char: str,
    country_code: CountryCodeUpdate,
    db: Session = Depends(get_db),
):
    stmt = select(EtcCountryCode).where(
        EtcCountryCode.country_code_2char == country_code_2char
    )
    result = await db.execute(stmt)
    db_country_code = result.scalars().first()
    if not db_country_code:
        return {"error": "Country code not found"}
    for key, value in country_code.model_dump().items():
        if value is not None:
            setattr(db_country_code, key, value)
    db.commit()
    db.refresh(db_country_code)
    return db_country_code


@router.delete("/country-codes/{country_code_2char}")
async def delete_country_code(
    country_code_2char: str,
    db: Session = Depends(get_db),
):
    stmt = select(EtcCountryCode).where(
        EtcCountryCode.country_code_2char == country_code_2char
    )
    result = await db.execute(stmt)
    db_country_code = result.scalars().first()
    if not db_country_code:
        return {"error": "Country code not found"}
    print("===============================")
    print(db_country_code)
    print(db_country_code.country_code_2char)
    print("===============================")
    await db.delete(db_country_code)
    await db.commit()
    return {"message": "Country code deleted successfully"}


@router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login")
async def login(request: Request, user: UserLogin, db: Session = Depends(get_db)):
    stmt = select(User).where(User.email == user.email)
    result = await db.execute(stmt)
    db_user = result.scalars().first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    else:
        request.session["user_id"] = db_user.id
        request.session["email"] = db_user.email
        request.session["password"] = db_user.hashed_password
        return {"message": "Login successful"}


@router.post("/logout")
async def logout(request: Request):
    request.session.pop("user_id", None)
    request.session.pop("email", None)
    request.session.pop("password", None)
    return {"message": "Logout successful"}


@router.get("/get_curr_user")
async def get_curr_user(request: Request):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    # 보안상 password는 반환하지 않음, email도 세션에 저장되어 있지 않으면 None
    return {
        "user_id": user_id,
        "user_email": request.session.get("email"),
        "user_password": request.session.get("password"),
    }
