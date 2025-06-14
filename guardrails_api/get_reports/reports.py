import os
from collections import defaultdict
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, func,Any
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from typing import Dict
# --- Environment setup ---
DSN = os.getenv("ANOMALY_DB_DSN")  # Example: postgresql://user:pass@host:5432/db
if not DSN:
    raise ValueError("Set ANOMALY_DB_DSN environment variable")

# --- SQLAlchemy setup ---
Base = declarative_base()

class Anomaly(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    request_id = Column(String(128), nullable=False)
    anomaly_type = Column(String(64), nullable=False)
    details = Column(Text, nullable=True)

engine = create_engine(DSN, echo=False)
Session = sessionmaker(bind=engine)

# --- Report generator ---
def generate_anomaly_report(group_by: str = "day") -> Dict[str, Any]:
    session = Session()
    try:
        if group_by == "day":
            time_format = func.date_trunc("day", Anomaly.timestamp)

            results = (
                session.query(
                    Anomaly.anomaly_type,
                    time_format.label("group_time")
                )
                .filter(Anomaly.anomaly_type.isnot(None))
                .all()
            )

            report = {}

            for raw_types, group_time in results:
                types = [t.strip() for t in raw_types.split(",") if t.strip()]
                time_key = group_time.strftime("%Y-%m-%d")

                for t in types:
                    if t not in report:
                        report[t] = {}
                    if time_key not in report[t]:
                        report[t][time_key] = 0
                    report[t][time_key] += 1

            return report

        elif group_by == "anomaly_type":
            results = (
                session.query(
                    Anomaly.anomaly_type
                )
                .filter(Anomaly.anomaly_type.isnot(None))
                .all()
            )

            counter = {}

            for (raw_types,) in results:
                types = [t.strip() for t in raw_types.split(",") if t.strip()]
                for t in types:
                    counter[t] = counter.get(t, 0) + 1

            return counter

        else:
            raise ValueError("group_by must be 'day' or 'anomaly_type'")

    finally:
        session.close()