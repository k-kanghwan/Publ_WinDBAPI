from typing import List, Optional
from database.database import Base


from sqlalchemy import Integer, Text
from sqlalchemy.dialects.mysql import TEXT, VARCHAR
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


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
    country_name_ko: Mapped[str] = mapped_column(VARCHAR(100), comment='국가명_한글')
    country_name_en: Mapped[str] = mapped_column(VARCHAR(100), comment='국가명_영문')
    country_code_numeric: Mapped[Optional[int]] = mapped_column(Integer, comment='국가코드_숫자')
