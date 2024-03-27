from typing import List
from datetime import datetime


def format_timestamp(timestamp: int) ->List[str]: 
    return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]


def timestamp_delta_to_string(timestamp: int) -> str: 
    seconds      = timestamp         // 1000
    milliseconds = timestamp % 1000
    return f"{seconds}s {milliseconds}ms"