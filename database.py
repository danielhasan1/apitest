from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#"postgres://wgimorgvsfqcma:bfcebfc7106a528042ac3549ea7fdb7c70214d6b5df4d5f6ddc0184307bbcd8c@ec2-174-129-41-127.compute-1.amazonaws.com:5432/deu7tq1j0qdoig"
#SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:danish@localhost/api"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
