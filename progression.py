import streamlit as st
import pandas as pd

excel_file=st.file_uploader("Excelファイルを選択してください",type=['xlsx'])

if excel_file:
    df=pd.read_excel(excel_file)
    problem_number_list=df['問題番号']
    problem_number=st.number_input('問題番号を選択してください',problem_number_list)
    problem_data=df.iloc[problem_number]
    now_count=0
    for i in range(3):
        if problem_data[str(i+1)+'回目']=='-':
            now_count=i+1
            break
    else:
        st.text('回数が3回を超過しています')
    if "choice" not in st.session_state:
        st.session_state.choice = None

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("o"):
            st.session_state.choice = "o"

    with col2:
        if st.button("△"):
            st.session_state.choice = "△"

    with col3:
        if st.button("x"):
            st.session_state.choice = "x"