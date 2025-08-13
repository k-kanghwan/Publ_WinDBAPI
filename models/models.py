from typing import List, Optional

from sqlalchemy import Enum, ForeignKeyConstraint, Index, Integer, String, Text
from sqlalchemy.dialects.mysql import TEXT, VARCHAR
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    declarative_base,
)

Base = declarative_base()

# fmt: off
class EtcCageCode(Base):
    __tablename__ = 'etc__cage_code'
    __table_args__ = {'comment': 'cage 정보(전체)'}

    cage_code: Mapped[str] = mapped_column(String(5), primary_key=True, comment='생산자부호')
    country: Mapped[Optional[str]] = mapped_column(Text, comment='국가')
    cage_status_code: Mapped[Optional[str]] = mapped_column(String(2), comment='CAGE상태부호')
    company_name: Mapped[Optional[str]] = mapped_column(String(400), comment='회사명')
    addr_kn: Mapped[Optional[str]] = mapped_column(String(400), comment='주소 한글')
    addr_en: Mapped[Optional[str]] = mapped_column(String(400), comment='주소 영문')
    assignment_dt: Mapped[Optional[str]] = mapped_column(String(20), comment='부여일')
    created_dt: Mapped[Optional[str]] = mapped_column(String(20), comment='생성일')
    modified_dt: Mapped[Optional[str]] = mapped_column(String(20), comment='변경일')
    application_dt: Mapped[Optional[str]] = mapped_column(String(20))
    processing_period: Mapped[Optional[str]] = mapped_column(Text, comment='처리기간')
    representative: Mapped[Optional[str]] = mapped_column(Text, comment='대표자')
    representative_phone_number: Mapped[Optional[str]] = mapped_column(Text, comment='대표전화번호')
    website: Mapped[Optional[str]] = mapped_column(Text, comment='홈페이지')
    alter_cage_code1: Mapped[Optional[str]] = mapped_column(String(5), comment='대체생산자부호1')
    alter_cage_code2: Mapped[Optional[str]] = mapped_column(String(5), comment='대체생산자부호2')
    alter_cage_code3: Mapped[Optional[str]] = mapped_column(String(5), comment='대체생산자부호3')
    alter_cage_code4: Mapped[Optional[str]] = mapped_column(String(5), comment='대체생산자부호4')
    alter_cage_code5: Mapped[Optional[str]] = mapped_column(String(5), comment='대체생산자부호5')


class EtcCageCodeKr(Base):
    __tablename__ = 'etc__cage_code_kr'
    __table_args__ = {'comment': 'cage 정보(국내만)'}

    cage_code: Mapped[str] = mapped_column(String(5), primary_key=True, comment='생산자부호')
    country: Mapped[Optional[str]] = mapped_column(Enum('한국'), comment='국가')
    cage_status_code: Mapped[Optional[str]] = mapped_column(String(2), comment='CAGE상태부호')
    company_name: Mapped[Optional[str]] = mapped_column(String(400), comment='회사명')
    addr_kn: Mapped[Optional[str]] = mapped_column(String(400), comment='주소 한글')
    addr_en: Mapped[Optional[str]] = mapped_column(String(400), comment='주소 영문')
    assignment_dt: Mapped[Optional[str]] = mapped_column(String(20), comment='부여일')
    created_dt: Mapped[Optional[str]] = mapped_column(String(20), comment='생성일')
    modified_dt: Mapped[Optional[str]] = mapped_column(String(20), comment='변경일')
    application_dt: Mapped[Optional[str]] = mapped_column(String(20))
    processing_period: Mapped[Optional[str]] = mapped_column(Text, comment='처리기간')
    representative: Mapped[Optional[str]] = mapped_column(Text, comment='대표자')
    representative_phone_number: Mapped[Optional[str]] = mapped_column(Text, comment='대표전화번호')
    website: Mapped[Optional[str]] = mapped_column(Text, comment='홈페이지')
    alter_cage_code1: Mapped[Optional[str]] = mapped_column(String(5), comment='대체생산자부호1')
    alter_cage_code2: Mapped[Optional[str]] = mapped_column(String(5), comment='대체생산자부호2')
    alter_cage_code3: Mapped[Optional[str]] = mapped_column(String(5), comment='대체생산자부호3')
    alter_cage_code4: Mapped[Optional[str]] = mapped_column(String(5), comment='대체생산자부호4')
    alter_cage_code5: Mapped[Optional[str]] = mapped_column(String(5), comment='대체생산자부호5')


class EtcCageStatusCode(Base):
    __tablename__ = 'etc__cage_status_code'
    __table_args__ = {'comment': 'cage 상태 코드'}

    status_code: Mapped[str] = mapped_column(String(1), primary_key=True)
    description: Mapped[Optional[str]] = mapped_column(Text)


class EtcCountryCode(Base):
    __tablename__ = 'etc__country_code'
    __table_args__ = {'comment': '국가부호정보'}

    country_code_2char: Mapped[str] = mapped_column(VARCHAR(2), primary_key=True, comment='국가부호_2자리')
    country_code_3char: Mapped[str] = mapped_column(VARCHAR(3), primary_key=True, comment='국가부호_3자리')
    country_name_kr: Mapped[str] = mapped_column(VARCHAR(100), comment='국가명_한글')
    country_name_en: Mapped[str] = mapped_column(VARCHAR(100), comment='국가명_영문')
    country_code_numeric: Mapped[Optional[int]] = mapped_column(Integer, comment='국가코드_숫자')


class IncFscFscInfo(Base):
    __tablename__ = 'inc_fsc__fsc_info'
    __table_args__ = {'comment': '군급부호표'}

    fsc: Mapped[str] = mapped_column(VARCHAR(4), primary_key=True, comment='군급부호')
    fsc_status: Mapped[str] = mapped_column(VARCHAR(4), comment='군급부호 상태')
    fsc_name_kn: Mapped[Optional[str]] = mapped_column(VARCHAR(255), comment='명칭_한글')
    fsc_name_en: Mapped[Optional[str]] = mapped_column(VARCHAR(255), comment='명칭_영문')
    note_kn: Mapped[Optional[str]] = mapped_column(TEXT, comment='주석_한글')
    note_en: Mapped[Optional[str]] = mapped_column(TEXT, comment='주석_영문')
    included_kn: Mapped[Optional[str]] = mapped_column(TEXT, comment='포함_한글')
    included_en: Mapped[Optional[str]] = mapped_column(TEXT, comment='포함_영문')
    excluded_kn: Mapped[Optional[str]] = mapped_column(TEXT, comment='제외_한글')
    excluded_en: Mapped[Optional[str]] = mapped_column(TEXT, comment='제외_영문')

    inc_fsc__relationship: Mapped[List['IncFscRelationship']] = relationship('IncFscRelationship', back_populates='inc_fsc__fsc_info')


class IncFscIncInfo(Base):
    __tablename__ = 'inc_fsc__inc_info'
    __table_args__ = {'comment': '지정품명부호표'}

    inc: Mapped[str] = mapped_column(VARCHAR(5), primary_key=True, comment='품명부호')
    niin: Mapped[Optional[str]] = mapped_column(VARCHAR(6), comment='품목식별지침부호(NIIN)')
    inc_name_kn: Mapped[Optional[str]] = mapped_column(VARCHAR(255), comment='품명_한글')
    inc_name_en: Mapped[Optional[str]] = mapped_column(VARCHAR(255), comment='품명_영문')
    description_kn: Mapped[Optional[str]] = mapped_column(TEXT, comment='품명정의_한글')
    description_en: Mapped[Optional[str]] = mapped_column(TEXT, comment='품명정의_영문')

    inc_fsc__relationship: Mapped[List['IncFscRelationship']] = relationship('IncFscRelationship', back_populates='inc_fsc__inc_info')


class StdForeignDocumentInfo(Base):
    __tablename__ = 'std_foreign__document_info'

    DocID_Spec_SubPart: Mapped[str] = mapped_column(VARCHAR(100), primary_key=True)
    DocID: Mapped[Optional[str]] = mapped_column(TEXT)
    Spec: Mapped[Optional[str]] = mapped_column(TEXT)
    SubPart: Mapped[Optional[str]] = mapped_column(TEXT)
    DocLastRevID: Mapped[Optional[str]] = mapped_column(TEXT)
    Status: Mapped[Optional[str]] = mapped_column(TEXT)
    Title: Mapped[Optional[str]] = mapped_column(TEXT)
    FSC: Mapped[Optional[str]] = mapped_column(TEXT)
    DocDate: Mapped[Optional[str]] = mapped_column(TEXT)
    HistoryStatus: Mapped[Optional[str]] = mapped_column(TEXT)
    Link: Mapped[Optional[str]] = mapped_column(TEXT)


class StdForeignMergedRev(Base):
    __tablename__ = 'std_foreign__merged_rev'

    ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    DocID_Spec_SubPart: Mapped[Optional[str]] = mapped_column(TEXT)
    doc_id: Mapped[Optional[str]] = mapped_column(TEXT)
    spec: Mapped[Optional[str]] = mapped_column(TEXT)
    sub_part: Mapped[Optional[str]] = mapped_column(TEXT)
    doc_check_id: Mapped[Optional[str]] = mapped_column(TEXT)
    rev_info: Mapped[Optional[str]] = mapped_column(TEXT)
    rev_date: Mapped[Optional[str]] = mapped_column(TEXT)
    rev_pages_info: Mapped[Optional[str]] = mapped_column(TEXT)
    rev_size_info: Mapped[Optional[str]] = mapped_column(TEXT)


class StdForeignRevInfo(Base):
    __tablename__ = 'std_foreign__rev_info'

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, comment='index')
    DocID_Spec_SubPart: Mapped[Optional[str]] = mapped_column(TEXT)
    DocID: Mapped[Optional[str]] = mapped_column(TEXT)
    Spec: Mapped[Optional[str]] = mapped_column(TEXT)
    SubPart: Mapped[Optional[str]] = mapped_column(TEXT)
    DocLastRevID: Mapped[Optional[str]] = mapped_column(TEXT)
    RevInfo: Mapped[Optional[str]] = mapped_column(TEXT)
    RevDate: Mapped[Optional[str]] = mapped_column(TEXT)
    RevPagesInfo: Mapped[Optional[int]] = mapped_column(Integer)
    RevSizeInfo: Mapped[Optional[str]] = mapped_column(TEXT)


class StdForeignStatusCode(Base):
    __tablename__ = 'std_foreign__status_code'

    Code: Mapped[str] = mapped_column(VARCHAR(2), primary_key=True)
    Status: Mapped[Optional[str]] = mapped_column(TEXT)
    Description: Mapped[Optional[str]] = mapped_column(TEXT)


class StdKsDocumentInfo(Base):
    __tablename__ = 'std_ks__document_info'

    std_num: Mapped[str] = mapped_column(VARCHAR(50), primary_key=True, comment='표준번호')
    status: Mapped[Optional[str]] = mapped_column(TEXT, comment='개정상태')
    std_name: Mapped[Optional[str]] = mapped_column(TEXT, comment='표준명')
    rev_confirmation_dt: Mapped[Optional[str]] = mapped_column(TEXT, comment='개정/개정확인일')
    notification_num: Mapped[Optional[str]] = mapped_column(TEXT, comment='고시번호')
    dept: Mapped[Optional[str]] = mapped_column(TEXT, comment='담당부서')
    person_in_charge: Mapped[Optional[str]] = mapped_column(TEXT, comment='담당자')


class StdKsExample(Base):
    __tablename__ = 'std_ks__example'

    ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    std_num2: Mapped[Optional[str]] = mapped_column(TEXT, comment='표준번호 + 본문 / 부속서')
    std_num_example: Mapped[Optional[str]] = mapped_column(TEXT, comment='호칭예제')
    Notes: Mapped[Optional[str]] = mapped_column(TEXT, comment='비고')


class StdKsNamingPattern(Base):
    __tablename__ = 'std_ks__naming_pattern'

    std_num2: Mapped[str] = mapped_column(String(500, 'utf8mb4_unicode_ci'), primary_key=True, comment='표준번호 + 본문 / 부속서')
    std_name: Mapped[Optional[str]] = mapped_column(TEXT, comment='표준명칭')
    fsc: Mapped[Optional[str]] = mapped_column(TEXT, comment='군급부호')
    inc: Mapped[Optional[str]] = mapped_column(TEXT, comment='품명부호')
    inc_name_kr: Mapped[Optional[str]] = mapped_column(TEXT, comment='품명_한글')
    regex: Mapped[Optional[str]] = mapped_column(TEXT, comment='정규표현식')
    detailed_designation: Mapped[Optional[str]] = mapped_column(TEXT, comment='호칭방법_본문')


class IncFscRelationship(Base):
    __tablename__ = 'inc_fsc__relationship'
    __table_args__ = (
        ForeignKeyConstraint(['fsc'], ['inc_fsc__fsc_info.fsc'], name='FK_inc_fsc__relationship_inc_fsc__fsc_info'),
        ForeignKeyConstraint(['inc'], ['inc_fsc__inc_info.inc'], name='FK_inc_fsc__relationship_inc_fsc__inc_info'),
        Index('FK_inc_fsc__relationship_inc_fsc__fsc_info', 'fsc'),
        Index('FK_inc_fsc__relationship_inc_fsc__inc_info', 'inc'),
        {'comment': '지정품명부호-군급부호 관계표'}
    )

    ID: Mapped[int] = mapped_column(Integer, primary_key=True, comment='index')
    inc: Mapped[str] = mapped_column(VARCHAR(5), comment='품명부호')
    fsc: Mapped[str] = mapped_column(VARCHAR(4), comment='군급부호')

    inc_fsc__fsc_info: Mapped['IncFscFscInfo'] = relationship('IncFscFscInfo', back_populates='inc_fsc__relationship')
    inc_fsc__inc_info: Mapped['IncFscIncInfo'] = relationship('IncFscIncInfo', back_populates='inc_fsc__relationship')
