import streamlit as st

def get_overview_page():

    st.header("Overview")

    requirements_col, overview_img_col = st.columns(2)

    with requirements_col:
        st.write("Our purpose here is to see any changes made from the frontend to be reflected in our dashboard. Here we define 2 strategies via which we can do that.")

        st.subheader("What use-case are we solving?")
        st.write("- Product wants click events from the FE to understand user behaviour and thus formulate nudge strategies.\n- Product wants to know the number of orders that are in open state in real time and create alerts.")

        st.subheader("Requirements")
        st.write("- Fetch real time event data from the frontend.\n- Fetch Historical event data from the frontend")

    with overview_img_col:
        st.image("./images/overview_brief.png")

    st.divider()
    st.subheader("What are our strategies?")
    st.write("We have specified 2 ways to achieve our above requirements. Below is their brief overview. For more details, head over to the `Strategies` tab.")

    be_datasource_col, kafka_datasource_col = st.columns(2)

    with be_datasource_col:
        st.write("### Using BE Server as our data source")
        st.write("Here, we pass the data from the FE to BE, and then fetch the required data from BE.")
        st.image("./images/overview_strategy_be.png")

    with kafka_datasource_col:
        st.write("### Using Kafka Pipeline as our data source")
        st.write("Here, we pass the data from the FE to BE. BE pushes this data to the Kafka pipeline. The dashboard gets its data by subscribing to topics in this pipline.")  
        st.image("./images/overview_strategy_kafka.png")  
        