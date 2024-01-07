import streamlit as st
import pandas as pd
import asyncio

from ..utilities.Poller import poll_endpoint, populate_cse_metrics

CSE_DS = []


def get_be_historical_strategy():
    with st.expander("Here, there will be a cron running that will fetch the data that is stored in Redis at the BE and push it to a more permanent storage in S3"):

        st.image("./images/be_historical.png")

        st.write("### Why a cron?")
        st.write("The Redis DB that the BE writes to persists data only for a limited time (Expiry set to 5 minutes for now). Hence pushing data to a more permanent storage makes sense. Depending on the expiry set, the frequency of the cron could be adjusted so that none of the data is lost.")

def get_be_live_startegy():
    with st.expander("Here the consumer will keep on polling the `ese-server` to get the real time event updates"):

        st.image("./images/be_live.png")

        st.write("- Using of Redis at the BE now makes sense as there will be a lot of read requests made. Using redis will help keep the latency in check.\n- The disdavantage here is that there will be unnecessary load on our server.")

    ESE_SERVER_URL = st.sidebar.text_input("Provide Server URL to start polling", placeholder="http://localhost:2000/events")
    POLLING_FREQUENCY = st.sidebar.number_input("Provide polling frequency", placeholder="Default value is 5s", value=5)

    if ESE_SERVER_URL == "":
        st.error("Pass an endpoint from where the dashboard could poll the server")
    else:
        asyncio.run(poll_endpoint(ESE_SERVER_URL, POLLING_FREQUENCY))
