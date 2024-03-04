import streamlit as st

from components.view.Sidebar import BE_DATA_SOURCE, HISTORICAL_FEED_TYPE

from .strategies.BEStrategy import get_be_historical_strategy, get_be_live_startegy
from .strategies.KafkaStrategy import get_kafka_historical_startegy, get_kafka_live_strategy

def get_strategies_page(data_source, feed_type):

    st.header(f"{data_source} as data source with {feed_type} feed")

    if data_source == BE_DATA_SOURCE:
        if feed_type == HISTORICAL_FEED_TYPE:
            get_be_historical_strategy()
        else:
            get_be_live_startegy()
    else:
        if feed_type == HISTORICAL_FEED_TYPE:
            get_kafka_historical_startegy()
        else:
            get_kafka_live_strategy()
