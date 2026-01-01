import streamlit as st

# --- APP CONFIG ---
st.set_page_config(page_title="BNG DARTS PRO", layout="centered")

# --- MOBILE-FIRST VERTICAL CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .block-container { padding: 0.5rem 0.5rem !important; }
    
    /* Header Scaling */
    .main-title { font-size: 22px; text-align: center; color: #555; margin-bottom: 5px; font-weight: bold;}
    
    /* Scoreboard - Vertical stack */
    .p-card { 
        background: #161b22; border-radius: 10px; padding: 12px; 
        text-align: center; margin-bottom: 5px; border: 1px solid #333;
    }
    .active-p { border: 2px solid #00d4ff !important; box-shadow: 0 0 12px #00d4ff; background: #1c232d; }
    .p-name { font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px;}
    .p-score { font-size: 48px; font-weight: 900; color: #00d4ff; line-height: 1; margin-top: 5px;}
    
    /* 3x4 Button Grid Tuning */
    div.stButton > button {
        width: 100%; height: 60px;
        background-color: #1a1f26; color: white;
        border: 1px solid #444; border-radius: 12px;
        font-size: 22px !important; margin-bottom: -10px;
        font-weight: bold;
    }
    div.stButton > button:active { 
        border-color: #ff0055; 
        color: #ff0055; 
        background-color: #25101a;
    }

    /* Hide Streamlit UI elements for a cleaner 'App' look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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
        st.toast("Bust or Invalid Score!")

# --- UI SIDEBAR ---
with st.sidebar:
    st.title("BNG Menu")
    st.session_state.num_players = st.number_input("Players", 1, 4, st.session_state.num_players)
    if st.button("New Game"):
        st.session_state.scores = {0: 501, 1: 501, 2: 501, 3: 501}
        st.session_state.history = {0: [], 1: [], 2: [], 3: []}
        st.session_state.turn = 0
        st.rerun()

# --- HEADER ---
st.markdown("<div class='main-title'>BNG DARTS PRO</div>", unsafe_allow_html=True)

# --- SCOREBOARD ---
# Displays players in a clean vertical or 2-column grid
if st.session_state.num_players <= 2:
    s_cols = st.columns(st.session_state.num_players)
else:
    s_cols = st.columns(2)

for i in range(st.session_state.num_players):
    col_idx = i % 2 if st.session_state.num_players > 2 else i
    with s_cols[col_idx]:
        active_class = "active-p" if st.session_state.turn == i else ""
        st.markdown(f"""<div class='p-card {active_class}'>
            <div class='p-name'>P{i+1}</div>
            <div class='p-score'>{st.session_state.scores[i]}</div>
        </div>""", unsafe_allow_html=True)

# --- 3x4 KEYPAD GRID ---
# Preset numbers based on your request
keypad_scores = [26, 41, 45, 60, 81, 85, 100, 121, 125, 140, 160, 180]

st.write("") # Spacer
k_cols = st.columns(3)
for idx, val in enumerate(keypad_scores):
    with k_cols[idx % 3]:
        if st.button(str(val)):
            add_score(val)
            st.rerun()

# --- UTILITY ROW ---
st.write("---")
u1, u2, u3 = st.columns(3)
with u1:
    if st.button("Undo"):
        prev_p = (st.session_state.turn - 1) % st.session_state.num_players
        if st.session_state.history[prev_p]:
            st.session_state.scores[prev_p] += st.session_state.history[prev_p].pop()
            st.session_state.turn = prev_p
            st.rerun()
with u2:
    # Small manual input field
    m_val = st.number_input("Other", 0, 180, 0, label_visibility="collapsed")
    if m_val > 0:
        add_score(m_val)
        st.rerun()
with u3:
    if st.button("Clear"):
        st.session_state.scores[st.session_state.turn] = 501
        st.session_state.history[st.session_state.turn] = []
        st.rerun()
