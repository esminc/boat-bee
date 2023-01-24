# type: ignore
import inspect
import os
from datetime import datetime


# 実行時間を計測するためのユーティリティ
class StopWatch:
    def __init__(self, location_: str):
        self.start = 0.0
        self.location = location_

    def __enter__(self):
        self.start = datetime.now()

    def __exit__(self, *exc):
        diff = (datetime.now() - self.start).microseconds / 1000
        print(f"time: {diff}ms\t\tlocation: {self.location}")


def location():
    frame = inspect.currentframe().f_back
    return (
        os.path.basename(frame.f_code.co_filename),
        frame.f_code.co_name,
        frame.f_lineno,
    )


# コンテキストマネージャーとして使うことで、実行時間を計測する。
with StopWatch(location_=location()):
    arr = []
    for i in range(10000000):
        arr.append(i)
