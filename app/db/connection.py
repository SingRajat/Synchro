from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL",
"postgresql://postgre:Rajat%402004@localhost:5432/synchro")

engine=create_engine(DATABASE_URL)

Session_Local=sessionmaker(autocommit=False,
autoflush=False, bind=engine)

Base=declarative_base()

def get_db():
    db=Session_Local()
    try:
        yield db
    finally:
        db.close()
