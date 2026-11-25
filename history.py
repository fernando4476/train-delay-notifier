from datetime import datetime, timezone
from sqlalchemy.orm import Session
from db import engine, DelayEvent


def record_delays(delays):
    now = datetime.now(timezone.utc)

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

def as_utc(dt):
    if dt is None:
        return None
    return dt.replace(tzinfo=timezone.utc)

def recent_events():
    with Session(engine) as session:
        rows = session.query(DelayEvent).order_by(DelayEvent.started_at.desc()).limit(20).all()
        recent_evnt = []
        for row in rows:
            recent_evnt.append({
                "line": row.line,
                "status": row.status,
                "message": row.message,
                "started_at": as_utc(row.started_at),
                "ended_at": as_utc(row.ended_at),
                "ongoing": row.ended_at is None,
            })
        
        return recent_evnt


if __name__ == "__main__":
    fake = [{"line": "Chiyoda", "status": "Delay", "message": "Test delay"}]
    record_delays(fake)
    record_delays([])