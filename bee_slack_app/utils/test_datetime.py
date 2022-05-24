# pylint: disable=non-ascii-name
from bee_slack_app.utils import datetime


def test_ISO8601形式の時刻文字列をPOSIXタイムスタンプに変換できること():  # pylint: disable=invalid-name

    result = datetime.iso_format_to_timestamp("2022-04-01T00:00:00+09:00")

    assert result == 1648738800.0


def test_POSIXタイムスタンプをISO8601形式の時刻文字列に変換できること():  # pylint: disable=invalid-name

    result = datetime.timestamp_to_iso_format(1648738800.0)

    assert result == "2022-04-01T00:00:00+09:00"
