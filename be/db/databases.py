from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./db/sqlite/fastapi-blockchain.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        # if returned finally wont be triggered
        # https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
        yield db
    finally:
        db.close()
