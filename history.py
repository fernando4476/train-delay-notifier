from datetime import datetime

from sqlalchemy.orm import Session

from db import engine, DelayEvent


def record_delays(delays):
    now = datetime.now()

    with Session(engine) as session:
        open_events = session.query(DelayEvent).filter(DelayEvent.ended_at.is_(None)).all()

        # Part A: open new delays
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

        # Part B: close delays that cleared
        current_lines = []
        for d in delays:
            current_lines.append(d["line"])

        for event in open_events:
            if event.line not in current_lines:
                event.ended_at = now

        session.commit()


if __name__ == "__main__":
    fake = [{"line": "Chiyoda", "status": "Delay", "message": "Test delay"}]
    record_delays(fake)
    record_delays([])