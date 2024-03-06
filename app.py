import streamlit as st

from components.constants import DATA_SOURCE_BE, DATA_SOURCE_KAFKA, EMAIL_USECASE_1, DUMMY_USECASE
from components.view.heading import heading
from components.view.sidebar import get_data_source, get_usecase

from components.usecase.trigger_email_on_steady_click.view_config_pannel import be_pannel, kafka_pannel
from components.usecase.dummy_usecase_example.view_config_pannel import be_pannel_dummy, kafka_pannel_dummy


heading()

data_source = get_data_source()
usecase     = get_usecase()

description_tab, control_tab, consumer_stats_tab, results_tab = st.tabs(["Description", "Configuration", "Consumer Stats", "Results"])

results_space = results_tab.empty()
stats_space   = consumer_stats_tab.empty()

usecase.display(description_tab)

if data_source == DATA_SOURCE_BE:

    if usecase == EMAIL_USECASE_1:
        usecase.set_control(
            config_ctx = control_tab,
            view_ctx   = results_space,
            stats_ctx  = stats_space,
            pannel     = be_pannel
        )

    elif usecase == DUMMY_USECASE:
        usecase.set_control(
            config_ctx = control_tab,
            view_ctx   = results_space,
            stats_ctx  = stats_space,
            pannel     = be_pannel_dummy
        )

elif data_source == DATA_SOURCE_KAFKA:

    if usecase == EMAIL_USECASE_1:
        usecase.set_control(
            config_ctx = control_tab,
            view_ctx   = results_space,
            stats_ctx  = stats_space,
            pannel     = kafka_pannel
        )
        
    elif usecase == DUMMY_USECASE:
        usecase.set_control(
            config_ctx = control_tab,
            view_ctx   = results_space,
            stats_ctx  = stats_space,
            pannel     = kafka_pannel_dummy
        )

if usecase.initiate: 
    usecase.results(results_tab, consumer_stats_tab)
else: 
    results_space.info("Initiate polling/consumption to populate this tab")
    stats_space.info("Initiate polling/consumption to populate this tab")