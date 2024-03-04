import streamlit as st

from components.constants import DATA_SOURCE_BE, DATA_SOURCE_KAFKA
from components.view.Heading import heading
from components.view.Sidebar import get_data_source, get_usecase
from components.view.ControlPannel import be_pannel, kafka_pannel

heading()

data_source = get_data_source()
usecase = get_usecase()

description_tab, control_tab, results_tab = st.tabs(["Description", "Configuration", "Results"])
results_space = results_tab.empty()
usecase.display(description_tab)

if data_source == DATA_SOURCE_BE:
    usecase.set_control(
        ctx=control_tab,
        view_ctx=results_space,
        pannel=be_pannel
    )
elif data_source == DATA_SOURCE_KAFKA:
    usecase.set_control(
        ctx=control_tab,
        view_ctx=results_space,
        pannel=kafka_pannel
    )

if not usecase.initiate:
    results_tab.info("Initiate Polling to view results")
else:
    usecase.results(results_tab)