from datetime import datetime
from sqlalchemy.orm import Session
from db import engine, DelayEvent


def record_delays(delays):
    now = datetime.now()

    with Session(engine) as session:
        open_events = session.query(DelayEvent).filter(DelayEvent.ended_at.is_(None)).all()

        open_lines = []
        for event in open_events:
            open_lines.append(event.line)

        for d in delays:
            if d["line"] not in open_lines:
                new_event = DelayEvent(
                    line=d["line"],
                    status=d["status"],
                    message=d["message"],
                    started_at=now,
                )
                session.add(new_event)

        session.commit()

if __name__ == "__main__":
    fake = [{"line": "Chiyoda", "status": "Delay", "message": "Test delay"}]
    record_delays(fake)
    record_delays(fake)