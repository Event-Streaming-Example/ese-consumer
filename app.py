import streamlit as st

from components.constants import DATA_SOURCE_BE, DATA_SOURCE_KAFKA, EMAIL_USECASE_1, DUMMY_USECASE
from components.view.Heading import heading
from components.view.Sidebar import get_data_source, get_usecase

from components.usecase.TriggerEmailOnSteadyClick.view_pannel import be_pannel_teosc, kafka_pannel_teosc
from components.usecase.DummyUsecaseExample.view_pannel import be_pannel_dummy, kafka_pannel_dummy

heading()

data_source = get_data_source()
usecase = get_usecase()

description_tab, control_tab, results_tab = st.tabs(["Description", "Configuration", "Results"])
results_space = results_tab.empty()
usecase.display(description_tab)

if data_source == DATA_SOURCE_BE:

    if usecase == EMAIL_USECASE_1:
        usecase.set_control(
            ctx=control_tab,
            view_ctx=results_space,
            pannel=be_pannel_teosc
        )

    elif usecase == DUMMY_USECASE:
        usecase.set_control(
            ctx=control_tab,
            view_ctx=results_space,
            pannel=be_pannel_dummy
        )

elif data_source == DATA_SOURCE_KAFKA:

    if usecase == EMAIL_USECASE_1:
        usecase.set_control(
            ctx=control_tab,
            view_ctx=results_space,
            pannel=kafka_pannel_teosc
        )
        
    elif usecase == DUMMY_USECASE:
        usecase.set_control(
            ctx=control_tab,
            view_ctx=results_space,
            pannel=kafka_pannel_dummy
        )

if not usecase.initiate:
    results_tab.info("Initiate Polling to view results")
else:
    usecase.results(results_tab)