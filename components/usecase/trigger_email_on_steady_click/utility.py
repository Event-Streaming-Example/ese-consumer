from typing import List
from datetime import datetime

def format_timestamps(timestamps: List[int]) ->List[str]: 
    return [datetime.fromtimestamp(ts / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] for ts in timestamps]


def timestamp_delta_to_string(timestamp: int) -> str: 
    seconds      = timestamp         // 1000
    milliseconds = timestamp % 1000
    return f"{seconds}s {milliseconds}ms"