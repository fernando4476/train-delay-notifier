from datetime import datetime
from sqlalchemy.orm import Session
from db import engine, DelayEvent

with Session(engine) as session:
    event = DelayEvent(
        line="TestLine",
        status="Delay",
        message="This is a test row",
        started_at=datetime.now(),
    )
    session.add(event)
    session.commit()

    rows = session.query(DelayEvent).all()
    for row in rows:
        print(row.id, row.line, row.ended_at)