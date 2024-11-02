import streamlit as st

# Defining pages
home_page = st.Page(
    page='views/home.py',
    title='Home',
    default=True
)
ministries_page = st.Page(
    page='views/ministries.py',
    title='Ministries'
)

mops_page = st.Page(
    page='views/mops.py',
    title='MOPS'
)

# test_page = st.Page(
#     page='views/tests.py',
#     title='Tests'
# )

# Setup page menu
pg = st.navigation(pages={
    'Home': [home_page],
    'Budgets': [ministries_page, ],
    'MOPS': [mops_page, ],
})
# Run navigation function
pg.run()
