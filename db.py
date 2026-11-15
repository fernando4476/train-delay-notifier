from sqlalchemy import create_engine, Column, Integer, Text, DateTime
from sqlalchemy.orm import declarative_base

engine = create_engine("sqlite:///train_notifier.db")
Base = declarative_base()


class DelayEvent(Base):
    __tablename__ = "delay_events"

    id = Column(Integer, primary_key=True)
    # your other five columns go here


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database created")
    