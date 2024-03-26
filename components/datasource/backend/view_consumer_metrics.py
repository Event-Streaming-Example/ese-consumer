import sys

from typing import List
from datetime import timedelta

from components.datasource.backend.models.response import Event


AVG_LAG = []

MAX_PRODUCER_LAG = 0
MAX_CONSUMER_LAG = 0

MIN_PRODUCER_LAG = sys.maxsize
MIN_CONSUMER_LAG = sys.maxsize



def _get_snapshot_stats_avg(data: List[int]): 
    length = len(data) if len(data) != 0 else 1
    return sum(data) / length


def _format_time_delta(milliseconds: int):
    if milliseconds == sys.maxsize:
        return "NA"
    
    delta = timedelta(milliseconds=milliseconds)

    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    formatted_string = ""
    if days > 0:
        formatted_string += f"{days} day, "
    if hours > 0:
        formatted_string += f"{hours} hrs, "
    if minutes > 0:
        formatted_string += f"{minutes} min, "
    if seconds > 0:
        formatted_string += f"{seconds} sec"

    return formatted_string


def calculate_lag(events: List[Event]): 
    global MAX_CONSUMER_LAG, MAX_PRODUCER_LAG, MIN_PRODUCER_LAG, MIN_CONSUMER_LAG
    total_snapshot_producer_lag = []
    total_snapshot_consumer_lag = []

    for event in events:
        MAX_PRODUCER_LAG = max(MAX_PRODUCER_LAG, event.get_producer_delta())
        MAX_CONSUMER_LAG = max(MAX_CONSUMER_LAG, event.get_consumer_delta())
        MIN_PRODUCER_LAG = min(MIN_PRODUCER_LAG, event.get_producer_delta())
        MIN_CONSUMER_LAG = min(MIN_CONSUMER_LAG, event.get_consumer_delta())
        total_snapshot_producer_lag.append(event.get_producer_delta())
        total_snapshot_consumer_lag.append(event.get_consumer_delta())

    AVG_LAG.append({
        "producer lag": _get_snapshot_stats_avg(total_snapshot_producer_lag),
        "consumer lag": _get_snapshot_stats_avg(total_snapshot_consumer_lag)
    })


def view_lag_metrics(ctx): 
    c = ctx.container()

    producer_col, consumer_col = c.columns(2)

    producer_col.markdown("#### Producer Lag")
    producer_col.write("This is the lag between from when the event was generated till when it reached the server")
    producer_metrics = producer_col.expander("Producer Metrics")
    producer_metrics.metric("Max Producer Lag", _format_time_delta(MAX_PRODUCER_LAG))
    producer_metrics.markdown("\n")
    producer_metrics.metric("Min Producer Lag", _format_time_delta(MIN_PRODUCER_LAG))

    consumer_col.markdown("#### Consumer Lag")
    consumer_col.write("This is the lag between from when the event was pulled from the server till it reached the consumer")
    consumer_metrics = consumer_col.expander("Consumer metrics")
    consumer_metrics.metric("Max Consumer Lag", _format_time_delta(MAX_CONSUMER_LAG))
    consumer_metrics.markdown("\n")
    consumer_metrics.metric("Min Consumer Lag", _format_time_delta(MIN_CONSUMER_LAG))

    c.divider()
    c.markdown("#### Rolling Average Lag")
    c.caption("The Lag calculated is in milli seconds against snapshots taken at intervals defined by the polling frequency.")
    c.line_chart(data=AVG_LAG)