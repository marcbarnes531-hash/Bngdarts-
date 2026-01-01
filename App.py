import streamlit as st

# --- APP CONFIG ---
st.set_page_config(page_title="BNG DARTS PRO", layout="centered")

# --- MOBILE-FIRST VERTICAL CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .block-container { padding: 0.5rem 0.5rem !important; }
    
    /* Header Scaling */
    .main-title { font-size: 24px; text-align: center; color: #555; margin-bottom: 0px; }
    
    /* Scoreboard - Vertical stack for mobile */
    .p-card { 
        background: #161b22; border-radius: 10px; padding: 10px; 
        text-align: center; margin-bottom: 5px; border: 1px solid #333;
    }
    .active-p { border: 2px solid #00d4ff !important; box-shadow: 0 0 10px #00d4ff; }
    .p-name { font-size: 14px; color: #888; text-transform: uppercase; }
    .p-score { font-size: 40px; font-weight: bold; color: #00d4ff; line-height: 1; }
    
    /* Button Grid Tuning */
    div.stButton > button {
        width: 100%; height: 50px;
        background-color: #1a1f26; color: white;
        border: 1px solid #444; border-radius: 8px;
        font-size: 18px !important; margin-bottom: -15px;
    }
    div.stButton > button:active { border-color: #ff0055; color: #ff0055; }
    
    /* Hide some Streamlit padding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'num_players' not in st.session_state: st.session_state.num_players = 1
if 'turn' not in st.session_state: st.session_state.turn = 0
if 'scores' not in st.session_state: st.session_state.scores = {0: 501, 1: 501, 2: 501, 3: 501}
if 'history' not in st.session_state: st.session_state.history = {0: [], 1: [], 2: [], 3: []}

# --- LOGIC ---
def add_score(val):
    p = st.session_state.turn
    current = st.session_state.scores[p]
    if current - val >= 0 and current - val != 1:
        st.session_state.scores[p] -= val
        st.session_state.history[p].append(val)
        st.session_state.turn = (st.session_state.turn + 1) % st.session_state.num_players
    else:
        st.toast("Bust!")

# --- UI SIDEBAR ---
with st.sidebar:
    st.title("Menu")
    st.session_state.num_players = st.number_input("Players", 1, 4, st.session_state.num_players)
    if st.button("New Game"):
        st.session_state.scores = {0: 501, 1: 501, 2: 501, 3: 501}
        st.session_state.history = {0: [], 1: [], 2: [], 3: []}
        st.session_state.turn = 0
        st.rerun()

# --- HEADER ---
st.markdown("<div class='main-title'>BNG DARTS PRO</div>", unsafe_allow_html=True)

# --- VERTICAL SCOREBOARD ---
# 1-2 players: side by side. 3-4 players: 2x2 grid.
if st.session_state.num_players <= 2:
    s_cols = st.columns(st.session_state.num_players)
else:
    s_cols = st.columns(2) # Grid for more players

for i in range(st.session_state.num_players):
    col_idx = i % 2 if st.session_state.num_players > 2 else i
    with s_cols[col_idx]:
        active_class = "active-p" if st.session_state.turn == i else ""
        st.markdown(f"""<div class='p-card {active_class}'>
            <div class='p-name'>Player {i+1}</div>
            <div class='p-score'>{st.session_state.scores[i]}</div>
        </div>""", unsafe_allow_html=True)

# --- KEYPAD GRID ---
st.write("")
k_col1, k_col2, k_col3 = st.columns(3)
keypad_scores = [26, 41, 45, 60, 81, 85, 100, 121, 140]

for idx, val in enumerate(keypad_scores):
    with [k_col1, k_col2, k_col3][idx % 3]:
        if st.button(str(val)):
            add_score(val)
            st.rerun()

# --- BOTTOM ROW ---
b1, b2, b3 = st.columns(3)
with b1:
    if st.button("180"):
        add_score(180)
        st.rerun()
with b2:
    if st.button("Undo"):
        prev_p = (st.session_state.turn - 1) % st.session_state.num_players
        if st.session_state.history[prev_p]:
            st.session_state.scores[prev_p] += st.session_state.history[prev_p].pop()
            st.session_state.turn = prev_p
            st.rerun()
with b3:
    # Manual tiny input
    m_val = st.number_input("Amt", 0, 180, 0, label_visibility="collapsed")
    if m_val > 0:
        add_score(m_val)
        st.rerun()

# --- FOOTER STATS (Very Small) ---
cur_p = st.session_state.turn
p_history = st.session_state.history[cur_p]
if p_history:
    avg = round((501 - st.session_state.scores[cur_p]) / len(p_history), 1)
    st.markdown(f"<p style='text-align:center; color:#555; font-size:12px;'>P{cur_p+1} PPR: {avg}</p>", unsafe_allow_html=True)
