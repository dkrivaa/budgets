import pandas as pd
import streamlit as st


def files():
    # These files are downloaded from 'https://www.gov.il/he/departments/policies/tableau'
    # The latest update of files on this site: 23.5.2024
    return {
        2015: 'files/tableau_BudgetData2015.xlsx',
        2016: 'files/tableau_BudgetData2016.xlsx',
        2017: 'files/tableau_BudgetData2017.xlsx',
        2018: 'files/tableau_BudgetData2018.xlsx',
        2019: 'files/tableau_BudgetData2019.xlsx',
        2020: 'files/tableau_BudgetData2020.xlsx',
        2021: 'files/tableau_tableau_BudgetData2021.xlsx',
        2022: 'files/tableau_BudgetData2022.xlsx',
        2023: 'files/tableau_BudgetData2023.xlsx',
        2024: 'files/tableau_BudgetData2024.xls',
        20241: 'files/before0710original2024.xlsx',
        # 2025: 'files/tableau_BudgetData-2025.xlsx'
    }


def read_files():
    # Getting dict of file urls
    url_dict = files()
    years = list(url_dict.keys())
    # Adding latest data year to session state
    st.session_state['latest_year'] = max([x for x in years if len(str(x)) == 4])
    # Dict to hold data
    data = {}
    message_holder = st.empty()
    # Reading the Excel files and adding to data dict
    for year in years:
        if year != 20241:
            message_holder.write(f'Loading data for {year}')
        else:
            message_holder.write(f'Loading data for 2024 (before 7/10/2023)')
        url = url_dict[year]
        df = pd.read_excel(url)

        # Drop rows for 'הכנסות' and 'החזר חוב'
        rows_to_drop = df[(df['קוד רמה 1'] == 8)].index   # | (df['קוד רמה 1'] == 6)].index
        df = df.drop(rows_to_drop)

        # # Replace 'משרד לביטחון פנים' with 'המשרד לביטחון הפנים' in the 'שם סעיף' column
        # df.loc[df['שם סעיף'] == 'משרד לביטחון פנים', 'שם סעיף'] = 'המשרד לביטחון הפנים'
        # df.loc[df['שם סעיף'] == 'פיתוח המשרד לביטחון', 'שם סעיף'] = 'המשרד לביטחון הפנים'
        # df.loc[df['שם סעיף'] == 'המשטרה ובתי הסוהר', 'שם סעיף'] = 'המשרד לביטחון הפנים'
        # df.loc[df['שם תחום'] == 'משרד לביטחון פנים', 'שם תחום'] = 'המשרד לביטחון הפנים'

        if year not in data:
            data[year] = df

    # Emptying message_holder
    message_holder.empty()
    # Adding the data dict to streamlit session state
    st.session_state['data'] = data


def make_code_dict():
    data_dict = st.session_state['data']
    latest_year = st.session_state['latest_year']
    df_latest = data_dict[latest_year]

    def level_dict(df, level):
        code_dict = {}
        level_list = df[level].unique().tolist()
        for item in level_list:
            parts = item.split('-')
            if len(parts) == 2:
                code = parts[0]
                name = parts[1]
            else:
                code = parts[0]
                name = ' '.join(parts[1:])

            if code not in code_dict:
                code = int(code)
                code_dict[code] = name
        return code_dict

    def annual_dict(df):
        levels = ['קוד ושם רמה 1', 'קוד ושם רמה 2', 'קוד ושם סעיף', 'קוד ושם תחום',
                  'קוד ושם תכנית', 'קוד ושם תקנה']

        code_dict1 = level_dict(df, levels[0])
        code_dict2 = level_dict(df, levels[1])
        code_dict3 = level_dict(df, levels[2])
        code_dict4 = level_dict(df, levels[3])
        code_dict5 = level_dict(df, levels[4])
        code_dict6 = level_dict(df, levels[5])

        return code_dict1, code_dict2, code_dict3, code_dict4, code_dict5, code_dict6

    (latest_code_dict1, latest_code_dict2, latest_code_dict3,
     latest_code_dict4, latest_code_dict5, latest_code_dict6) = annual_dict(df_latest)

    years = list(data_dict.keys())
    years.remove(latest_year)
    for year in years:
        df = data_dict[year]
        code_dict1, code_dict2, code_dict3, code_dict4, code_dict5, code_dict6 = annual_dict(df)

        def check_dict(latest_dict, dict):
            latest_dict_keys = latest_dict.keys()
            dict_keys = dict.keys()

            for key in dict_keys:
                if key not in latest_dict_keys:
                    latest_dict[key] = dict[key]

            return latest_dict

        latest_code_dict1 = check_dict(latest_code_dict1, code_dict1)
        latest_code_dict2 = check_dict(latest_code_dict2, code_dict2)
        latest_code_dict3 = check_dict(latest_code_dict3, code_dict3)
        latest_code_dict4 = check_dict(latest_code_dict4, code_dict4)
        latest_code_dict5 = check_dict(latest_code_dict5, code_dict5)
        latest_code_dict6 = check_dict(latest_code_dict6, code_dict6)

    st.session_state['latest_code_dict1'] = latest_code_dict1
    st.session_state['latest_code_dict2'] = latest_code_dict2
    st.session_state['latest_code_dict3'] = latest_code_dict3
    st.session_state['latest_code_dict4'] = latest_code_dict4
    st.session_state['latest_code_dict5'] = latest_code_dict5
    st.session_state['latest_code_dict6'] = latest_code_dict6


def connection_level2_level3():
    data_dict = st.session_state['data']
    years = list(data_dict.keys())

    latest_code_dict2 = st.session_state['latest_code_dict2']
    level2_list = list(latest_code_dict2.keys())

    connection_dict = {}

    for level2 in level2_list:
        level3_set = set()
        for year in years:
            df = data_dict[year]

            df = df[df['קוד רמה 2'] == level2]
            level3_list = df['קוד סעיף'].unique().tolist()
            for item in level3_list:
                level3_set.add(item)

        connection_dict[level2] = list(level3_set)

    st.session_state['connection_2_3'] = connection_dict


def budget_proposal_2025():
    df = pd.read_excel('files/budget2025.xlsx')
    budget_2025_dict = df.set_index('article')[['budget_2024', 'budget_2025']].to_dict().to_dict(orient='index')

    st.session_state['budget_2025_dict'] = budget_2025_dict







