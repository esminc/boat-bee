from datetime import datetime, timezone, timedelta


def now():
    return datetime.now(timezone(timedelta(hours=9))).isoformat(timespec="seconds")
