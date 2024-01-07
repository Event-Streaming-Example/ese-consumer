import streamlit as st
import pandas as pd

import requests
import asyncio
import datetime

from .populate_cse_metrics import populate_cse_metrics
from .get_connections_metrics import get_all_connections, display_connections, get_all_connections_event_count

CSE_DS = []
CONNECTIONS = []
CONN_EVENT_COUNT = {}


async def poll_endpoint(url, polling_frequency):

    
    connection_expander = st.expander("Connection metrics")

    connection_expander.subheader("Rolling Connections")
    connection_expander.write("This chart shows the currently connected IPs and the total number of events emitted by them")
    connections_display = connection_expander.empty()

    connection_expander.subheader("Connection Metric Insights")
    connections_table_text = connection_expander.empty()
    connections_table_display = connection_expander.empty()



    cse_expander = st.expander("Click Stream metrics")

    cse_expander.subheader("Rolling update")
    cse_expander.write("This chart shows the total number of click stream events and their sub-types starting from when the dashboard was initialized.")
    cse_chart_display = cse_expander.empty()

    cse_expander.subheader("Last 5 minute update")
    cse_expander.write("This table shows the latest count of click stream events and when they were last generated.")
    cse_last_5_display = cse_expander.empty()

    
    while True:
        response = requests.get(url).json()

        populate_cse_metrics(response, CSE_DS)
        get_all_connections(response, CONNECTIONS)
        get_all_connections_event_count(CONNECTIONS, CONN_EVENT_COUNT)
        display_conns = display_connections(CONNECTIONS)

        df1 = pd.DataFrame(CSE_DS)
        df2 = pd.DataFrame(display_conns)
        df3 = pd.DataFrame(mask_connection_events(CONN_EVENT_COUNT)).transpose()
        
        try:
            connections_table_text.write(f"Total __{get_total_events()}__ events were emitted, out of which __{get_total_cs_events()}__ were of type `CLICK_STREAM_EVENTS` and __{get_total_ou_events()}__ were of type `ORDER_UPDATE_EVENTS`. Their distribution across clients is as follows.")
        except:
            connections_table_text.write("No events emitted yet.")

        if len(CONNECTIONS)!=0: connections_display.line_chart(df2, x="timestamp", y="count", color="ip")
        if len(CONN_EVENT_COUNT)!=0: connections_table_display.dataframe(df3)

        if len(CSE_DS)!=0:cse_chart_display.line_chart(df1, x="timestamp")
        if len(CSE_DS)!=0:cse_last_5_display.table(CSE_DS[-1])

        await asyncio.sleep(polling_frequency)
    

def get_total_events():
    count = 0
    for items in CONN_EVENT_COUNT.values():
        count += items["total_count"]
    return count

def get_total_cs_events():
    count = 0
    for items in CONN_EVENT_COUNT.values():
        count += items["click_count"]
    return count

def get_total_ou_events():
    count = 0
    for items in CONN_EVENT_COUNT.values():
        count += items["order_count"]
    return count

def mask_connection_events(data_store):
    result = {}
    for key, value in data_store.items():
        result[key] = {
            "total_count" : value["total_count"],
            "click_count" : value["click_count"],
            "order_count" : value["order_count"]
        }
    return result