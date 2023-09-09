from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:1234word@localhost/university')


Session = sessionmaker(bind=engine)
session = Session()

