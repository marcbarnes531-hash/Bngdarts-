import streamlit as st

# --- APP CONFIG ---
st.set_page_config(page_title="BNG DARTS PRO", layout="centered")

# --- CUSTOM NEON CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; font-family: 'sans-serif'; }
    
    /* Neon Glow Score */
    .score-container {
        text-align: center;
        padding: 20px;
        margin-bottom: 10px;
    }
    .score-display {
        font-size: 120px !important;
        font-weight: 800;
        color: #00d4ff;
        text-shadow: 0 0 10px #00d4ff, 0 0 30px #00d4ff;
        line-height: 1;
    }
    
    /* Quick Hit Buttons */
    div.stButton > button {
        width: 100%; height: 70px;
        background-color: #161b22;
        color: white;
        border: 2px solid #00d4ff;
        border-radius: 15px;
        font-size: 22px !important;
        font-weight: bold;
        transition: 0.2s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    div.stButton > button:active {
        transform: scale(0.95);
        border-color: #ff0055;
        box-shadow: 0 0 20px #ff0055;
    }

    /* Input Field Styling */
    .stNumberInput input {
        background-color: #1a1f26 !important;
        color: #ff0055 !important;
        border: 2px solid #ff0055 !important;
        font-size: 30px !important;
        text-align: center !important;
        border-radius: 15px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'score' not in st.session_state: st.session_state.score = 501
if 'history' not in st.session_state: st.session_state.history = []
if 'input_key' not in st.session_state: st.session_state.input_key = 0

# --- LOGIC ---
def subtract_score():
    # Fetch value from session state via key
    val = st.session_state[f"manual_{st.session_state.input_key}"]
    if val:
        rem = st.session_state.score - val
        if rem < 0 or rem == 1:
            st.toast("🚨 BUST!")
        else:
            st.session_state.score = rem
            st.session_state.history.append(val)
    
    # Reset input field by changing the key
    st.session_state.input_key += 1

def quick_add(val):
    rem = st.session_state.score - val
    if rem < 0 or rem == 1:
        st.toast("🚨 BUST!")
    else:
        st.session_state.score = rem
        st.session_state.history.append(val)

# --- UI DISPLAY ---
st.markdown("<h3 style='text-align: center; color: #555;'>BNG DARTS</h3>", unsafe_allow_html=True)
st.markdown(f'<div class="score-container"><div class="score-display">{st.session_state.score}</div></div>', unsafe_allow_html=True)

# Checkout Suggestion
if st.session_state.score <= 170:
    # Logic for common checkouts
    checkouts = {170: "T20, T20, Bull", 100: "T20, D20", 80: "T16, D16", 40: "D20", 32: "D16"}
    msg = checkouts.get(st.session_state.score, "Focus on the finish!")
    st.info(f"🎯 Checkout: {msg}")

# Immediate Input Field
st.number_input(
    "Enter Score & Hit Enter:", 
    min_value=0, max_value=180, step=1, value=0,
    key=f"manual_{st.session_state.input_key}", 
    on_change=subtract_score
)

st.write("---")

# Quick Buttons (Grid)
col1, col2, col3 = st.columns(3)
quick_scores = [26, 41, 45, 60, 81, 85, 100, 140, 180]

for i, v in enumerate(quick_scores):
    with [col1, col2, col3][i % 3]:
        if st.button(f"{v}"):
            quick_add(v)
            st.rerun()

# Controls
st.write("")
c1, c2 = st.columns(2)
with c1:
    if st.button("Undo ↩️"):
        if st.session_state.history:
            st.session_state.score += st.session_state.history.pop()
            st.rerun()
with c2:
    if st.button("Reset 🔄"):
        st.session_state.score = 501
        st.session_state.history = []
        st.rerun()

# Stats
if st.session_state.history:
    avg = round((501 - st.session_state.score) / len(st.session_state.history), 1)
    st.write(f"**PPR:** {avg} | **Darts Thrown:** {len(st.session_state.history) * 3}")
