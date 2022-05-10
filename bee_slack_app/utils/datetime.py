from datetime import datetime, timedelta, timezone


def now():
    return datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")
