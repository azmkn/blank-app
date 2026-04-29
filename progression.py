import streamlit as st
import pandas as pd
import io

excel_file=st.file_uploader("Excelファイルを選択してください",type=['xlsx'])

if excel_file:
    st.session_state.df=pd.read_excel(excel_file)

    if "changes" not in st.session_state:
        st.session_state.changes=[]

    if "choice" not in st.session_state:
        st.session_state.choice=None

    if "confirm_clear" not in st.session_state:
        st.session_state.confirm_clear=False

    problem_number=st.number_input(
        '問題番号を選択してください',
        1,
        int(st.session_state.df['問題番号'].max())
    )

    st.write("判定を選択")

    # ⭐ 横並び＆大きく
    col1,col2,col3=st.columns(3)

    with col1:
        if st.button("o",use_container_width=True):
            st.session_state.choice="o"

    with col2:
        if st.button("△",use_container_width=True):
            st.session_state.choice="△"

    with col3:
        if st.button("x",use_container_width=True):
            st.session_state.choice="x"

    st.write("現在の選択:",st.session_state.choice)

    if st.button("追加"):
        if st.session_state.choice:
            st.session_state.changes=[
                c for c in st.session_state.changes
                if c["problem"]!=problem_number
            ]
            st.session_state.changes.append({
                "problem":problem_number,
                "choice":st.session_state.choice
            })

    st.write("変更予定")

    if st.session_state.changes:
        changes_df=pd.DataFrame(st.session_state.changes)
        changes_df.columns=["問題番号","判定"]
        st.dataframe(changes_df)
    else:
        st.write("（まだ追加されていません）")

    # ⭐ クリア確認フロー
    if st.button("変更予定をクリア"):
        st.session_state.confirm_clear=True

    if st.session_state.confirm_clear:
        st.warning("本当にクリアしますか？")
        col1,col2=st.columns(2)

        with col1:
            if st.button("はい"):
                st.session_state.changes=[]
                st.session_state.confirm_clear=False

        with col2:
            if st.button("いいえ"):
                st.session_state.confirm_clear=False

    if st.button("変更"):
        for change in st.session_state.changes:
            p=change["problem"]
            c=change["choice"]

            problem_data=st.session_state.df.iloc[p-1]

            for i in range(3):
                col_name=str(i+1)+'回目'
                if problem_data[col_name]=='-':
                    st.session_state.df.at[p-1,col_name]=c
                    break

        st.session_state.changes=[]

    st.dataframe(st.session_state.df)

    buffer=io.BytesIO()
    with pd.ExcelWriter(buffer,engine="openpyxl") as writer:
        st.session_state.df.to_excel(writer,index=False)

    st.download_button(
        "ダウンロード",
        buffer.getvalue(),
        excel_file.name
    )
    st.text("保存方法")
    st.text("ダウンロードしたファイルを開いて共有→開く、保存")