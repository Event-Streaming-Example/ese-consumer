import streamlit as st

from components.Heading import create_heading
from components.Sidebar import get_sidebar_inputs, get_historical_sidebar
from components.Sidebar import BE_DATA_SOURCE, HISTORICAL_FEED_TYPE

from components.pages.OverviewPage import get_overview_page
from components.pages.StrategiesPage import get_strategies_page

create_heading()

data_source, feed_type = get_sidebar_inputs()

st.sidebar.divider()

if feed_type == HISTORICAL_FEED_TYPE:
    get_historical_sidebar()

overview_tab, strategies_tab = st.tabs(["Overview","Strategies"])

with overview_tab:
    get_overview_page()     

with strategies_tab:
    get_strategies_page(data_source, feed_type)
    