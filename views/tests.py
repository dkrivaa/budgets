import streamlit as st
import pandas as pd

from file_functions import connection_level2_level3
from budget_functions import budget_2025


def test1():
    data_dict = st.session_state['data']

    years = list(data_dict.keys())
    years.remove(st.session_state['latest_year'])

    dataset_latest = set()
    dataset = set()
    difference = set()

    df = data_dict[st.session_state['latest_year']]
    items = (df['קוד סעיף'].unique().tolist())

    for item in items:
        dataset_latest.add(item)

    for year in years:

        df = data_dict[year]

        items = df['קוד סעיף'].unique().tolist()
        for item in items:
            dataset.add(int(item))
            if item not in dataset_latest:
                st.write(year, item, df[df['קוד סעיף'] == item]['שם סעיף'].unique(),
                         df[df['קוד סעיף'] == item]['הוצאה נטו'].sum())

    for item in dataset:
        if item not in dataset_latest:
            difference.add(item)

    # st.write(dataset_latest)
    # st.write(dataset)
    # st.write(difference)

    df = data_dict[st.session_state['latest_year']]
    st.write(df['שם סעיף'].unique())

# test1()


connection_level2_level3()

