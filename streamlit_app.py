import streamlit as st
from random import choice, shuffle

st.set_page_config(page_title="気候人狼", page_icon="🐺", layout="centered")

st.title("🐺 気候人狼")

# 気候設定
s = choice(["A","B","C","D","E"])
d = {
"A":["Af","Am","Aw"],
"B":["BW","BS"],
"C":["Cfa","Cfb","Cs","Cw"],
"D":["Dw","Df"],
"E":["ET","EF"]
}

li = d[s]

simin = choice(li)
li.remove(simin)
werewolf = choice(li)

st.subheader("人数設定")

number = st.number_input("全体人数",0,step=1)
number_werewolf = st.number_input("人狼人数",0,step=1)
number_fortune = st.number_input("占い師人数",0,step=1)
number_knight = st.number_input("騎士人数",0,step=1)

# ゲーム開始
if st.button("🎮 Start Game"):

    roles = []

    roles += ['人狼 , '+werewolf] * number_werewolf
    roles += ["占い師"] * number_fortune
    roles += ["騎士"] * number_knight

    while len(roles) < number:
        roles.append('市民 , '+simin)

    shuffle(roles)

    st.session_state.roles = roles
    st.session_state.player = 0
    st.session_state.show = False
    st.session_state.phase = "confirm"


# ===== 役職確認フェーズ =====

if "phase" in st.session_state and st.session_state.phase == "confirm":

    roles = st.session_state.roles
    p = st.session_state.player

    if p < len(roles):

        st.header(f"プレイヤー {p+1}")

        if not st.session_state.show:

            st.info("自分の番の人だけ画面を見てください")

            if st.button("役職を見る 👀"):
                st.session_state.show = True
                st.rerun()

        else:

            role = roles[p]

            # 陣営判定
            if role[0] == '人':
                team = "🐺 人狼陣営"
                color = "red"
            elif role in ["占い師","騎士"]:
                team = "👥 市民陣営"
                color = "green"
            else:
                team = "👥 市民陣営"
                color = "blue"

            st.markdown(f"### 役職: **{role}**")
            st.markdown(f"**陣営:** :{color}[{team}]")

            if st.button("▶ 次の人へ"):
                st.session_state.player += 1
                st.session_state.show = False
                st.rerun()

    else:
        st.success("全員の確認が終わりました")
        st.session_state.phase = "game"
        st.rerun()


# ===== ゲーム用役職確認 =====

if "phase" in st.session_state and st.session_state.phase == "game":
    st.header('全員の確認が終了しました')
    st.header("ゲーム中 役職確認")

    roles = st.session_state.roles

    player = st.number_input("プレイヤーを選択",1)

    if st.button("役職確認"):

        role = roles[player-1]

        if role[0] == '人':
            team = "🐺 人狼陣営"
            color = "red"
        elif role in ["占い師","騎士"]:
            team = "👥 市民陣営"
            color = "green"
        else:
            team = "👥 市民陣営"
            color = "blue"

        st.markdown(f"### プレイヤー {player}")
        st.markdown(f"役職: **{role}**")
        st.markdown(f"陣営: :{color}[{team}]")