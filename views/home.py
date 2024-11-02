import streamlit as st

from file_functions import read_files, make_code_dict, connection_level2_level3, budget_proposal_2025

# Reading data into streamlit session state if not already existing
if 'data' in st.session_state:
    pass
else:
    with st.spinner('Loading data. This will just take a minute.....'):
        read_files()

# Making various dicts and saving to session state
make_code_dict()
connection_level2_level3()

# budget_2025_dict = st.session_state['budget_2025_dict']

st.title(f'Budget Data 2015-{st.session_state['latest_year']}')
st.write('Data published by Ministry of Finance')
st.write('---')
with st.container(border=True):
    st.subheader('Ministries:')
    st.write('''
        Here you can find data about annual budgets allocated to groups of ministries or 
        individual ministries.
    ''')
    if st.button('Press Here', key=1):
        st.switch_page('views/ministries.py')

st.write('---')

with st.container(border=True):
    st.subheader('MOPS:')
    st.write('''
        Here you can find data about annual budgets allocated to the various 
        organizations within MOPS.
    ''')
    if st.button('Press Here', key=2):
        st.switch_page('views/mops.py')

