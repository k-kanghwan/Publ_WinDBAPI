from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


password = "local"
DATABASE_URL = (
    f"mysql+pymysql://root:{password}@localhost/win_db"  # MySQL 데이터베이스 URL
)
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
