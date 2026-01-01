import streamlit as st

# --- APP CONFIG ---
st.set_page_config(page_title="BNG DARTS PRO", layout="centered")

# --- MOBILE-FIRST COMPACT CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .block-container { padding: 0.5rem 0.5rem !important; }
    
    /* Compact Scoreboard Grid */
    .p-card { 
        background: #161b22; border-radius: 8px; padding: 8px; 
        text-align: center; border: 1px solid #333;
    }
    .active-p { border: 2px solid #00d4ff !important; box-shadow: 0 0 10px #00d4ff; }
    .p-score { font-size: 36px; font-weight: 900; color: #00d4ff; line-height: 1; }
    .p-name { font-size: 10px; color: #888; }
    
    /* FORCE 3rd-COLUMN GRID FOR KEYPAD */
    .stButton > button {
        width: 100% !important;
        height: 60px !important;
        background-color: #1a1f26 !important;
        color: white !important;
        border: 1px solid #444 !important;
        border-radius: 12px !important;
        font-size: 22px !important;
        font-weight: bold !important;
        margin-bottom: -15px !important;
    }
    .stButton > button:active { border-color: #ff0055 !important; color: #ff0055 !important; }

    /* Remove extra space between columns */
    [data-testid="column"] { padding: 0px 4px !important; }
    
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'num_players' not in st.session_state: st.session_state.num_players = 1
if 'turn' not in st.session_state: st.session_state.turn = 0
if 'scores' not in st.session_state: st.session_state.scores = {i: 501 for i in range(4)}
if 'history' not in st.session_state: st.session_state.history = {i: [] for i in range(4)}

def add_score(val):
    p = st.session_state.turn
    current = st.session_state.scores[p]
    if current - val >= 0 and current - val != 1:
        st.session_state.scores[p] -= val
        st.session_state.history[p].append(val)
        st.session_state.turn = (st.session_state.turn + 1) % st.session_state.num_players
    else:
        st.toast("Bust!")

# --- SCOREBOARD (Top Row) ---
st.markdown("<div style='text-align:center; font-size:14px; color:#555; margin-bottom:5px;'>BNG DARTS PRO</div>", unsafe_allow_html=True)
s_cols = st.columns(st.session_state.num_players)
for i in range(st.session_state.num_players):
    with s_cols[i]:
        active_class = "active-p" if st.session_state.turn == i else ""
        st.markdown(f"""<div class='p-card {active_class}'>
            <div class='p-name'>P{i+1}</div>
            <div class='p-score'>{st.session_state.scores[i]}</div>
        </div>""", unsafe_allow_html=True)

# --- THE 3x4 KEYPAD GRID ---
# Most common darts scores
keypad_scores = [26, 41, 45, 60, 81, 85, 100, 121, 125, 140, 160, 180]

st.write("") # Spacer
# This creates 4 rows of 3 columns
for i in range(0, len(keypad_scores), 3):
    row_scores = keypad_scores[i : i + 3]
    cols = st.columns(3)
    for j, val in enumerate(row_scores):
        if cols[j].button(str(val), key=f"btn_{val}_{i}_{j}"):
            add_score(val)
            st.rerun()

# --- UTILITY ROW ---
st.write("---")
u_cols = st.columns([1, 1.5, 1])
with u_cols[0]:
    if st.button("Undo"):
        prev_p = (st.session_state.turn - 1) % st.session_state.num_players
        if st.session_state.history[prev_p]:
            st.session_state.scores[prev_p] += st.session_state.history[prev_p].pop()
            st.session_state.turn = prev_p
            st.rerun()
with u_cols[1]:
    m_val = st.number_input("Other", 0, 180, 0, label_visibility="collapsed")
    if m_val > 0:
        add_score(m_val)
        st.rerun()
with u_cols[2]:
    if st.button("Reset"):
        st.session_state.scores[st.session_state.turn] = 501
        st.session_state.history[st.session_state.turn] = []
        st.rerun()

# --- SETTINGS (Bottom) ---
with st.expander("Player Settings"):
    st.session_state.num_players = st.number_input("Players", 1, 4, st.session_state.num_players)
