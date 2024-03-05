import streamlit as st

from components.models import DataSource, Usecase
from components.constants import DATA_SOURCE, DATA_SOURCE_BE, DATA_SOURCE_KAFKA
from components.constants import USECASE, EMAIL_USECASE_1, DUMMY_USECASE


def get_data_source() -> DataSource:
    result = st.sidebar.selectbox(DATA_SOURCE, (DATA_SOURCE_BE.option, DATA_SOURCE_KAFKA.option))
    ds = DATA_SOURCE_BE if result == DATA_SOURCE_BE.option else DATA_SOURCE_KAFKA
    st.sidebar.markdown(ds.description)
    st.sidebar.divider()
    return ds

def get_usecase() -> Usecase:
    result = st.sidebar.selectbox(USECASE, (DUMMY_USECASE.option, EMAIL_USECASE_1.option))
    uc = EMAIL_USECASE_1 if result == EMAIL_USECASE_1.option else DUMMY_USECASE
    st.subheader(uc.option)
    return uc