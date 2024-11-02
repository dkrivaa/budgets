import streamlit as st
import pandas as pd

from menu_functions import menu
from budget_functions import get_budget

# Getting the menus for the different levels
menu1, numbers1 = menu(1)
level1 = st.selectbox('Ministry Group', options=menu1, index=None)
level_list = (level1,)
criteria_list = ()
if level1:
    criteria1 = numbers1[menu1.index(level1)]
    criteria_list = (criteria1, )
    menu2, numbers2 = menu(2, criteria1)
    level2 = st.selectbox('Ministry', options=menu2, index=None)
    if level2:
        level_list = (level1, level2)
        criteria2 = numbers2[menu2.index(level2)]
        criteria_list = (criteria1, criteria2, )
        menu3, numbers3 = menu(3, criteria1, criteria2)
        level3 = st.selectbox('Budget Article', options=menu3, index=None)
        if level3:
            level_list = (level1, level2, level3)
            criteria3 = int(numbers3[menu3.index(level3)])
            criteria_list = (criteria1, criteria2,criteria3, )
            menu4, numbers4 = menu(4, criteria1, criteria2, criteria3)
            level4 = st.selectbox('Budget Area', options=menu4, index=None)
            if level4:
                level_list = (level1, level2, level3, level4)
                criteria4 = numbers4[menu4.index(level4)]
                criteria_list = (criteria1, criteria2, criteria3, criteria4, )
                menu5, numbers5 = menu(5, criteria1, criteria2, criteria3,
                                       criteria4)
                level5 = st.selectbox('Budget Program', options=menu5, index=None)
                if level5:
                    level_list = (level1, level2, level3, level4, level5)
                    criteria5 = numbers5[menu5.index(level5)]
                    criteria_list = (criteria1, criteria2, criteria3, criteria4, criteria5, )
                    menu6, numbers6 = menu(6, criteria1, criteria2, criteria3,
                                           criteria4, criteria5)
                    level6 = st.selectbox('Budget Paragraph', options=menu6, index=None)
                    if level6:
                        level_list = (level1, level2, level3, level4, level5, level6)
                        criteria6 = numbers6[menu6.index(level6)]
                        criteria_list = (criteria1, criteria2, criteria3, criteria4,
                                         criteria5, criteria6)

st.write('---')

col1, col2, col3, col4 = st.columns([1, 1.2, 1.5, 1])
with col1:
    total = st.button('Total Budget')
with col2:
    wage = st.button('Only Wage Budget')
with col3:
    other = st.button('Only Non-Wage Budget')
if wage:
    budget = 'wage'
elif other:
    budget = 'other'
else:
    budget = 'total'

pre_war = st.checkbox('Include 2024 budget approved prior to 7.10.2023 (named 20241)')
# Getting the data according to entries of user
if pre_war:
    df = get_budget(budget, True, *criteria_list)
else:
    df = get_budget(budget, False, *criteria_list)
st.write('---')

with st.container(border=True):
    st.bar_chart(df, stack=False, y_label='(Thousand Ils)')
    st.write('---')
    if pre_war:
        st.dataframe(df, height=423)
    else:
        st.dataframe(df)

