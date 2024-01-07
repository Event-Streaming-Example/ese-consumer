import streamlit as st

HISTORICAL_FEED_TYPE="Historical"
LIVE_FEED_TYPE="Live"

BE_DATA_SOURCE="Backend Server"
KAFKA_DATA_SOURCE="Kafka Pipeline"

def get_sidebar_inputs():
    st.sidebar.subheader("Configure your strategy here")
    data_source = st.sidebar.selectbox(label="Select data source", options=(BE_DATA_SOURCE,KAFKA_DATA_SOURCE))
    feed_type = st.sidebar.selectbox(label="Select Feed Type", options=(HISTORICAL_FEED_TYPE, LIVE_FEED_TYPE))
    return data_source, feed_type

def get_historical_sidebar():
    st.sidebar.subheader("Things to note")
    st.sidebar.write("This project is done mainly to simulate real time functionalities. Hence we have taken the liberty to not configure the dashboard for Historical data.")
    st.sidebar.write("We however have specified what the architecture would look like if one were to provide that functionality.")