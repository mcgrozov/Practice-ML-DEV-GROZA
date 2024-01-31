from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, func, ForeignKey, Float, JSON
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    balance = Column(Integer, default=1000)


class Models(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    cost = Column(Integer)


class Predictions(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    model_id = Column(Integer)
    prediction_date = Column(DateTime(timezone=True), default=func.now())
    is_success = Column(Boolean)
    is_finished = Column(Boolean)
    error_info = Column(String)
    output = Column(JSON, nullable=True)


engine = create_engine('sqlite:///src/infrastructure/mydatabase.db',
                       echo=True)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


# p = Predictions(user_id=1, model_id=1, is_success=True, is_finished=True, output=3)
# session.add_all([p])
# session.commit()

users = session.query(Predictions).all()

# Выведите результаты
for user in users:
    print(f'ID: {user.id}, user_id: {user.user_id}, model_id: {user.model_id}, output: {user.output}')