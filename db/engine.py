from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sqlite_path = "sqlite:///test.db"

engine = create_engine(url=sqlite_path)

Session = sessionmaker(bind=engine)
session = Session()
