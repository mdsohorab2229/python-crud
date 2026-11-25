from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base



# DATABASE_URL="mysql+pymysql://root:root@localhost:3306/training"
# DATABASE_URL="mysql+pymysql://root:@localhost:3307/sms"
# DATABASE_URL="postgresql+psycopg2://sms_ska4_user:2uVOIvIsEm8v4JplzXynPpPPwO5ypKwB@dpg-dc35d0m7bikc73c55ff0-a.ohio-postgres.render.com/sms_ska4"
# DATABASE_URL="mysql+pymysql://root:@localhost:3307/final_project_fastapi"
DATABASE_URL="postgresql+psycopg2://sms_ska4_user:2uVOIvIsEm8v4JplzXynPpPPwO5ypKwB@dpg-dc35d0m7bikc73c55ff0-a.ohio-postgres.render.com/sms_ska4"

engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit =False, autoflush=False, bind=engine)
base = declarative_base()


# def get_connection():
#     db = session_local
#     try:
#         yield db
#     finally:
#         db.close    