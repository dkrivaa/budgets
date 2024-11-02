import streamlit as st
import pandas as pd


def menu(level_to_get=1, criteria1=None, criteria2=None, criteria3=None,
         criteria4=None, criteria5=None, level6=None):

    # Getting all latest_code_dicts
    dict1 = st.session_state['latest_code_dict1']
    dict2 = st.session_state['latest_code_dict2']
    dict3 = st.session_state['latest_code_dict3']
    dict4 = st.session_state['latest_code_dict4']
    dict5 = st.session_state['latest_code_dict5']
    dict6 = st.session_state['latest_code_dict6']

    # Function to make menu level 3 according to chosen level2
    def menu3():
        dict = st.session_state['connection_2_3']
        return dict[criteria2]


    if level_to_get == 1:
        return list(dict1.values()), list(dict1.keys())

    elif level_to_get == 2:
        menu2 = [v for k, v in dict2.items() if str(k)[0] == str(criteria1)]
        numbers2 = [x for x in list(dict2.keys()) if dict2[x] in menu2]
        return menu2, numbers2

    elif level_to_get == 3:
        return [dict3[x] for x in menu3()], menu3()

    elif level_to_get == 4:
        menu4 = [v for k, v in dict4.items()
                 if (len(str(k)) == 3 and str(k)[0] == str(criteria3)) or
                 (len(str(k)) == 4 and str(k)[0:2] == str(criteria3))]
        if 'חשבון מעבר' in menu4:
            menu4.remove('חשבון מעבר')
        numbers4 = [k for k, v in dict4.items()
                 if (len(str(k)) == 3 and str(k)[0] == str(criteria3)) or
                 (len(str(k)) == 4 and str(k)[0:2] == str(criteria3))]
        return menu4, numbers4

    elif level_to_get == 5:
        menu5 = [v for k, v in dict5.items()
                if (len(str(int(k))) == 5 and str(k)[:3] == str(criteria4)) or
                (len(str(int(k))) == 6 and str(k)[:4] == str(criteria4))]
        numbers5 = [k for k, v in dict5.items()
                if (len(str(int(k))) == 5 and str(k)[:3] == str(criteria4)) or
                (len(str(int(k))) == 6 and str(k)[:4] == str(criteria4))]
        return menu5, numbers5

    elif level_to_get == 6:
        menu6 = [v for k, v in dict6.items()
                if (len(str(int(k))) == 7 and str(k)[:5] == str(criteria5)) or
                (len(str(int(k))) == 8 and str(k)[:6] == str(criteria5))]
        numbers6 = [k for k, v in dict6.items()
                if (len(str(int(k))) == 7 and str(k)[:5] == str(criteria5)) or
                (len(str(int(k))) == 8 and str(k)[:6] == str(criteria5))]
        return menu6, numbers6


def mops_menu(criteria3=None):
    dict4 = st.session_state['latest_code_dict4']

    menu4 = [v for k, v in dict4.items()
             if (len(str(k)) == 3 and str(k)[0] == '7') ]
    if 'חשבון מעבר' in menu4:
        menu4.remove('חשבון מעבר')
    numbers4 = [k for k, v in dict4.items()
                if (len(str(k)) == 3 and str(k)[0] == '7') or
                (len(str(k)) == 4 and str(k)[0:2] == '52')]

    return menu4, numbers4
