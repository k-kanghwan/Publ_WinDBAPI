from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker

# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


password = "local"
# DATABASE_URL = (
#     f"mysql+pymysql://root:{password}@localhost/win_db"  # MySQL 데이터베이스 URL
# )
DATABASE_URL = f"mysql+aiomysql://root:{password}@localhost/win_db"  # MySQL 비동기 데이터베이스 URL

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()
