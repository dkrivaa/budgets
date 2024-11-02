import streamlit as st
import pandas as pd


def budget_types():
    return ['מקורי', 'מאושר', 'ביצוע']


def data_from_session():
    data_dict = st.session_state['data']
    years = list(data_dict.keys())
    return data_dict, years


def get_budget(budget=None, pre_war=False, criteria1=None, criteria2=None,
               criteria3=None, criteria4=None, criteria5=None, criteria6=None):
    budget_status = budget_types()
    # Getting the data from session state
    data_dict, years = data_from_session()

    # Remove pre war 2024 budget
    if pre_war is False:
        years.remove(20241)
    # List to hold annual data
    annual = []
    for year in years:
        df = data_dict[year]

        # Parts for getting relevant budget data according to the optional levels
        # Budget status
        original_start = (df['סוג תקציב'] == budget_status[0])
        approved_start = (df['סוג תקציב'] == budget_status[1])
        executed_start = (df['סוג תקציב'] == budget_status[2])
        # Total, Wage, Other
        budget_part = [(df['שם מיון רמה 1'] == 'שכר') if budget == 'wage' else
                       (df['שם מיון רמה 1'] != 'שכר') if budget == 'other' else
                       (True)][0]
        level1_part = [(df['קוד רמה 1'] == criteria1) if criteria1 else (True)][0]
        level2_part = [(df['קוד רמה 2'] == criteria2) if criteria2 else (True)][0]
        level3_part = [(df['קוד סעיף'] == criteria3) if criteria3 else (True)][0]
        level4_part = [(df['קוד תחום'] == criteria4) if criteria4 else (True)][0]
        level5_part = [(df['קוד תכנית'] == criteria5) if criteria5 else (True)][0]
        level6_part = [(df['קוד תקנה'] == criteria6) if criteria6 else (True)][0]

        original = int(df[original_start & budget_part & level1_part & level2_part & level3_part &
                          level4_part & level5_part & level6_part]['הוצאה נטו'].sum())
        approved = int(df[approved_start & budget_part & level1_part & level2_part &
                          level3_part & level4_part & level5_part &
                          level6_part]['הוצאה נטו'].sum())
        executed = int(df[executed_start & budget_part & level1_part & level2_part &
                          level3_part & level4_part & level5_part &
                          level6_part]['הוצאה נטו'].sum())

        annual.append([original, approved, executed])

    return pd.DataFrame(annual, columns=['1-original', '2-approved', '3-executed'],
                        index=[str(year) for year in years])


def mops_budget(budget=None, pre_war=False, criteria4=None, ):
    budget_status = budget_types()
    data_dict, years = data_from_session()

    # Remove pre war 2024 budget
    if pre_war is False:
        years.remove(20241)
    # List to hold annual data
    annual = []
    for year in years:
        df = data_dict[year]
        # Only MOPS
        df = df[(df['קוד רמה 1'] == 1) & (df['קוד רמה 2'] == 12)]
        # Parts for getting relevant budget data according to the optional levels
        # Budget status
        original_start = (df['סוג תקציב'] == budget_status[0])
        approved_start = (df['סוג תקציב'] == budget_status[1])
        executed_start = (df['סוג תקציב'] == budget_status[2])
        # Total, Wage, Other
        budget_part = [(df['שם מיון רמה 1'] == 'שכר') if budget == 'wage' else
                       (df['שם מיון רמה 1'] != 'שכר') if budget == 'other' else
                       (True)][0]
        if criteria4 in [755, 760]:
            level4_part = [(df['קוד תחום'] == criteria4) if criteria4 else (True)][0]
        else:
            level4_part = [((df['קוד תחום'] == criteria4[0]) | (df['קוד תחום'] == criteria4[1]))
                           if criteria4 else (True)][0]
        original = int(df[original_start & budget_part &
                          level4_part]['הוצאה נטו'].sum())
        approved = int(df[approved_start & budget_part & level4_part]['הוצאה נטו'].sum())
        executed = int(df[executed_start & budget_part & level4_part]['הוצאה נטו'].sum())

        annual.append([original, approved, executed])

    return pd.DataFrame(annual, columns=['1-original', '2-approved', '3-executed'],
                        index=[str(year) for year in years])


def budget_2025():
    data_dict, years = data_from_session()
    years = [year for year in years if year > 2021]

    types_of_budgets = budget_types()

    data = []

    ministry_list = data_dict[st.session_state['latest_year']]['קוד סעיף'].unique().tolist()
    ministry_names = data_dict[st.session_state['latest_year']]['שם סעיף'].unique().tolist()

    df_names = pd.DataFrame([ministry_list, ministry_names])
    st.dataframe(df_names)

    for ministry in ministry_list:
        budget_data = []
        for year in years:
            df = data_dict[year]
            df = df[df['סוג תקציב'] == types_of_budgets[0]]

            budget = df[df['קוד סעיף'] == ministry]['הוצאה נטו'].sum()
            budget_data.append([year, ministry, budget])
        data.append(budget_data)

    # st.write(data)

    # Initialize lists to hold columns, indices, and values
    columns = []
    indices = []
    values = []

    # Process each item in data
    for sublist in data:
        for item in sublist:
            if len(item) == 3:
                columns.append(item[0])  # Column name
                indices.append(item[1])  # Row index
                values.append(int(item[2]))  # Cell value, cast to int if np.int64

    # Create a DataFrame from the lists
    df = pd.DataFrame({'Column': columns, 'Index': indices, 'Value': values})

    # Pivot the DataFrame to get the desired structure
    df_pivot = df.pivot(index='Index', columns='Column', values='Value')

    st.dataframe(df_pivot)






