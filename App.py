import streamlit as st

# --- APP CONFIG ---
st.set_page_config(page_title="BNG DARTS PRO", layout="centered")

# --- CUSTOM CSS (Mobile Optimized) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    /* Tighten spacing for mobile */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
    
    /* Active Player Glow */
    .active-p { border: 2px solid #00d4ff; box-shadow: 0 0 15px #00d4ff; border-radius: 10px; padding: 5px; background: #161b22; }
    .inactive-p { opacity: 0.5; padding: 5px; }

    .score-val { font-size: 45px !important; font-weight: 800; color: #00d4ff; text-align: center; }
    .player-name { font-size: 16px; text-align: center; color: #eee; margin-bottom: -10px; }

    /* Keypad Style Buttons */
    div.stButton > button {
        width: 100%; height: 55px;
        background-color: #161b22; color: white;
        border: 1px solid #444; border-radius: 8px;
        font-size: 18px !important; margin-bottom: -10px;
    }
    div.stButton > button:active { border-color: #ff0055; color: #ff0055; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'num_players' not in st.session_state: st.session_state.num_players = 1
if 'turn' not in st.session_state: st.session_state.turn = 0 # 0 = Player 1, 1 = Player 2...
if 'scores' not in st.session_state: st.session_state.scores = {0: 501, 1: 501, 2: 501, 3: 501}
if 'history' not in st.session_state: st.session_state.history = {0: [], 1: [], 2: [], 3: []}

# --- FUNCTIONS ---
def add_score(val):
    p = st.session_state.turn
    current = st.session_state.scores[p]
    if current - val >= 0 and current - val != 1:
        st.session_state.scores[p] -= val
        st.session_state.history[p].append(val)
        # Auto-switch player after each input
        st.session_state.turn = (st.session_state.turn + 1) % st.session_state.num_players
    else:
        st.toast("Invalid Score / Bust!")

def reset_game():
    st.session_state.scores = {0: 501, 1: 501, 2: 501, 3: 501}
    st.session_state.history = {0: [], 1: [], 2: [], 3: []}
    st.session_state.turn = 0

# --- SIDEBAR MENU ---
with st.sidebar:
    st.header("Settings")
    st.session_state.num_players = st.number_input("How many players?", 1, 4, st.session_state.num_players)
    if st.button("Reset Entire Game"): reset_game()

# --- SCOREBOARD ---
cols = st.columns(st.session_state.num_players)
for i in range(st.session_state.num_players):
    with cols[i]:
        style = "active-p" if st.session_state.turn == i else "inactive-p"
        st.markdown(f"""<div class='{style}'>
            <div class='player-name'>P{i+1}</div>
            <div class='score-val'>{st.session_state.scores[i]}</div>
        </div>""", unsafe_allow_html=True)

st.write("---")

# --- KEYPAD LAYOUT ---
st.markdown("<p style='text-align:center; color:#888;'>Select Score</p>", unsafe_allow_html=True)
k_col1, k_col2, k_col3 = st.columns(3)

# Common Scores arranged in a grid
keypad_scores = [26, 41, 45, 60, 81, 85, 100, 121, 140]
for idx, val in enumerate(keypad_scores):
    target_col = [k_col1, k_col2, k_col3][idx % 3]
    if target_col.button(str(val)):
        add_score(val)
        st.rerun()

# Bottom Row for high score and manual
b_col1, b_col2, b_col3 = st.columns([1,1,1])
with b_col1:
    if st.button("180 🔥"):
        add_score(180)
        st.rerun()
with b_col2:
    if st.button("Undo ↩️"):
        # Undo logic for previous player
        prev_p = (st.session_state.turn - 1) % st.session_state.num_players
        if st.session_state.history[prev_p]:
            last = st.session_state.history[prev_p].pop()
            st.session_state.scores[prev_p] += last
            st.session_state.turn = prev_p
            st.rerun()
with b_col3:
    # Manual Input (Small & Tidy)
    manual = st.number_input("Custom", 0, 180, 0, label_visibility="collapsed")
    if manual > 0:
        add_score(manual)
        st.rerun()
