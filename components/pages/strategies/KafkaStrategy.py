import streamlit as st

def get_kafka_historical_startegy():
    with st.expander("Here, there will be a flink consumer that will keep pulling data from the pipeline and write it to a more permanent storage in S3 (or Snowflake). Our consumer (dashboard) will query from S3"):

        st.image("./images/kafka_historical.png")

    st.subheader("Advantage over traditional BE Setup")

    st.write("1. Components such as `ese-server` and our dashboard can now scale-up and be maintained independently.\n2. Over time crons are un-reliable and it can get confusing to understand and maintain. This setup does away with all that.")

def get_kafka_live_strategy():
    with st.expander("Here, the consumer will pull events from the kafka pipeline, thus removing the dependency from backend."):

        st.image("./images/kafka_live.png")

    st.subheader("Advantage over traditional BE Setup")

    st.write("1. Continuously polling the main server is resource intensive and can lead disastrous results. This setup removes the direct dependency the dashboard has with the `ese-server`.\n2. Point of having a Redis DB over at the BE was to accomodate for the dashboard to get live feeds. Now that the dashboard is getting its data from the pipeline, we can do away with redis here. This helps us in reducing costs.")