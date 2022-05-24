from datetime import datetime, timedelta, timezone

from dateutil import parser  # type: ignore

japan_tz = timezone(timedelta(hours=9))


def now() -> str:
    """
    UTC+9の現在時刻をISO 8601形式で取得する

    Returns:
        str : 現在時刻。例 2022-04-01T00:00:00+09:00
    """
    return datetime.now(japan_tz).isoformat(timespec="seconds")


def parse(target: str) -> str:
    """
    ISO 8601形式の時刻文字列をYYYY/mm/dd HH:MM:SSにパースする

    Returns:
        str : YYYY/mm/dd HH:MM:SSの時刻文字列。例 2022/04/01 00:00:00
    """
    return parser.parse(target).strftime("%Y/%m/%d %H:%M:%S")


def timestamp_to_iso_format(timestamp: float) -> str:
    """
    POSIXタイムスタンプをISO 8601形式の時刻文字列に変換する

    例: -> YYYY/mm/dd HH:MM:SS
    """
    return datetime.fromtimestamp(timestamp, tz=japan_tz).isoformat(timespec="seconds")


def iso_format_to_timestamp(iso_format: str) -> float:
    """
    ISO 8601形式の時刻文字列をPOSIXタイムスタンプに変換する
    """
    return datetime.fromisoformat(iso_format).timestamp()


TIMESTAMP_MAX = datetime.max.timestamp()
