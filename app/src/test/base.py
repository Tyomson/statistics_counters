
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import CONFIG

engine = create_engine(CONFIG['db_url'])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
