import streamlit as st

# --- APP CONFIG ---
st.set_page_config(page_title="BNG DARTS PRO", layout="centered")

# --- MOBILE-FIRST VERTICAL CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .block-container { padding: 0.5rem 0.5rem !important; }
    
    /* Scoreboard */
    .p-card { 
        background: #161b22; border-radius: 10px; padding: 10px; 
        text-align: center; margin-bottom: 5px; border: 1px solid #333;
    }
    .active-p { border: 2px solid #00d4ff !important; box-shadow: 0 0 12px #00d4ff; }
    .p-score { font-size: 44px; font-weight: 900; color: #00d4ff; line-height: 1; }
    
    /* Checkout Box */
    .checkout-box {
        background: rgba(0, 212, 255, 0.1);
        border: 1px dashed #00d4ff;
        border-radius: 8px;
        padding: 8px;
        text-align: center;
        margin: 10px 0;
        color: #00d4ff;
        font-weight: bold;
        font-size: 18px;
    }

    /* 3x4 Button Grid */
    div.stButton > button {
        width: 100%; height: 58px;
        background-color: #1a1f26; color: white;
        border: 1px solid #444; border-radius: 10px;
        font-size: 20px !important; margin-bottom: -12px;
        font-weight: bold;
    }
    div.stButton > button:active { border-color: #ff0055; color: #ff0055; }
    
    /* Hide UI */
    #MainMenu, footer, header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- CHECKOUT DATA ---
CHECKOUTS = {
    170: "T20-T20-BULL", 167: "T20-T19-BULL", 164: "T20-T18-BULL", 161: "T20-T17-BULL",
    160: "T20-T20-D20", 158: "T20-T20-D19", 140: "T20-T20-D10", 121: "T20-T15-D8",
    100: "T20-D20", 80: "T16-D16", 60: "S20-D20", 40: "D20", 32: "D16", 16: "D8", 8: "D4", 4: "D2", 2: "D1"
} # Note: This list can be expanded to all numbers 2-170

# --- SESSION STATE ---
if 'num_players' not in st.session_state: st.session_state.num_players = 1
if 'turn' not in st.session_state: st.session_state.turn = 0
if 'scores' not in st.session_state: st.session_state.scores = {i: 501 for i in range(4)}
if 'history' not in st.session_state: st.session_state.history = {i: [] for i in range(4)}

# --- LOGIC ---
def add_score(val):
    p = st.session_state.turn
    current = st.session_state.scores[p]
    if current - val >= 0 and current - val != 1:
        st.session_state.scores[p] -= val
        st.session_state.history[p].append(val)
        if st.session_state.scores[p] == 0:
            st.balloons()
        else:
            st.session_state.turn = (st.session_state.turn + 1) % st.session_state.num_players
    else:
        st.toast("Bust!")

# --- UI SIDEBAR ---
with st.sidebar:
    st.title("BNG SETTINGS")
    st.session_state.num_players = st.number_input("Players", 1, 4, st.session_state.num_players)
    if st.button("New Game"):
        st.session_state.scores = {i: 501 for i in range(4)}
        st.session_state.history = {i: [] for i in range(4)}
        st.session_state.turn = 0
        st.rerun()

# --- SCOREBOARD ---
s_cols = st.columns(2) if st.session_state.num_players > 1 else st.columns(1)
for i in range(st.session_state.num_players):
    with s_cols[i % 2]:
        active_class = "active-p" if st.session_state.turn == i else ""
        st.markdown(f"""<div class='p-card {active_class}'>
            <div style='font-size:10px; color:#888;'>PLAYER {i+1}</div>
            <div class='p-score'>{st.session_state.scores[i]}</div>
        </div>""", unsafe_allow_html=True)

# --- CHECKOUT GUIDE ---
current_p_score = st.session_state.scores[st.session_state.turn]
if current_p_score <= 170:
    route = CHECKOUTS.get(current_p_score, "No 3-Dart Finish")
    st.markdown(f"<div class='checkout-box'>🎯 {route}</div>", unsafe_allow_html=True)
else:
    st.write("") # Spacer to keep layout consistent

# --- 3x4 KEYPAD ---
keypad_scores = [26, 41, 45, 60, 81, 85, 100, 121, 125, 140, 160, 180]
k_cols = st.columns(3)
for idx, val in enumerate(keypad_scores):
    with k_cols[idx % 3]:
        if st.button(str(val)):
            add_score(val)
            st.rerun()

# --- UTILITY ROW ---
st.write("---")
u1, u2, u3 = st.columns([1, 1.5, 1])
with u1:
    if st.button("Undo"):
        prev_p = (st.session_state.turn - 1) % st.session_state.num_players
        if st.session_state.history[prev_p]:
            st.session_state.scores[prev_p] += st.session_state.history[prev_p].pop()
            st.session_state.turn = prev_p
            st.rerun()
with u2:
    m_val = st.number_input("Other", 0, 180, 0, label_visibility="collapsed")
    if m_val > 0:
        add_score(m_val)
        st.rerun()
with u3:
    if st.button("Reset"):
        st.session_state.scores[st.session_state.turn] = 501
        st.session_state.history[st.session_state.turn] = []
        st.rerun()
