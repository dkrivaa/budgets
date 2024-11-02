import streamlit as st
import pandas as pd

from menu_functions import menu
from budget_functions import mops_budget
from menu_functions import mops_menu

if 'data' in st.session_state:
    menu4, numbers4 = mops_menu()

level4 = st.selectbox('Choose Organization', options=menu4, index=None)
st.write('---')
col1, col2, col3, col4 = st.columns([1, 1.2, 1.5, 1])
with col1:
    total = st.button('Total Budget')
with col2:
    wage = st.button('Only Wage Budget')
with col3:
    other = st.button('Only Non-Wage Budget')


pre_war = st.checkbox('Include 2024 budget approved prior to 7.10.2023 (named 20241)')
st.write('---')

if level4:
    criteria4 = numbers4[menu4.index(level4)]
    if criteria4 not in [755, 760]:
        if criteria4 == 750:
            criteria4 = [750, 5230]
        elif criteria4 == 770:
            criteria4 = [770, 5240]
        elif criteria4 == 780:
            criteria4 = [780, 5250]
else:
    criteria4 = None

if wage:
    budget = 'wage'
elif other:
    budget = 'other'
else:
    budget = 'total'

if pre_war and criteria4 is None:
    df = mops_budget(budget, True, )
elif pre_war and criteria4 is not None:
    df = mops_budget(budget, True, criteria4)
elif criteria4 is not None:
    df = mops_budget(budget, False, criteria4)
else:
    df = mops_budget(budget, False,)


with st.container(border=True):
    st.bar_chart(df, stack=False, y_label='(Thousands Ils)')
    if pre_war:
        st.dataframe(df, height=423)
    else:
        st.dataframe(df, )

