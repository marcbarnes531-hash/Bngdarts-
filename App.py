import streamlit as st

# --- APP CONFIG ---
st.set_page_config(page_title="BNG DARTS", layout="centered")

# --- CUSTOM NEON STYLE (Matching your image) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    /* Big Neon Buttons */
    div.stButton > button {
        width: 100%;
        height: 70px;
        font-size: 20px !important;
        font-weight: bold;
        border-radius: 12px;
        border: 2px solid #00d4ff;
        background-color: #161b22;
        color: white;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        border-color: #ff0055;
        box-shadow: 0 0 15px #ff0055;
        color: #ff0055;
    }
    /* Large Score Display */
    .score-display {
        font-size: 100px;
        text-align: center;
        font-weight: bold;
        color: #00d4ff;
        text-shadow: 0 0 20px #00d4ff;
        margin-bottom: -20px;
    }
    /* Input Box Styling */
    .stNumberInput input {
        background-color: #161b22 !important;
        color: #00d4ff !important;
        font-size: 24px !important;
        text-align: center !important;
        border: 2px solid #00d4ff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GAME LOGIC ---
if 'score' not in st.session_state:
    st.session_state.score = 501
if 'history' not in st.session_state:
    st.session_state.history = []

def process_score(val):
    if val > 180:
        st.error("Max score is 180!")
    elif st.session_state.score - val < 0 or st.session_state.score - val == 1:
        st.warning("BUST!")
    else:
        st.session_state.score -= val
        st.session_state.history.append(val)

# --- UI HEADER ---
st.markdown("<h1 style='text-align: center; color: white;'>BNG DARTS PRO</h1>", unsafe_allow_html=True)
st.markdown(f'<div class="score-display">{st.session_state.score}</div>', unsafe_allow_html=True)

# Checkout Suggestions
if st.session_state.score <= 170:
    # Example logic - can be expanded to full table
    if st.session_state.score == 40: sug = "D20 (Tops)"
    elif st.session_state.score == 32: sug = "D16"
    elif st.session_state.score == 170: sug = "T20, T20, Bull"
    else: sug = "Focus on the double!"
    st.success(f"Suggested: {sug}")

st.write("### Quick Tap Scores")
# Grid for common scores
col1, col2, col3 = st.columns(3)
quick_scores = [26, 41, 45, 60, 81, 85, 100, 121, 140]

for i, val in enumerate(quick_scores):
    with [col1, col2, col3][i % 3]:
        if st.button(f"{val}"):
            process_score(val)

if st.button("🔥 180"):
    process_score(180)

st.write("---")

# --- CUSTOM INPUT SECTION ---
st.write("### Custom Score")
custom_val = st.number_input("Enter exact score:", min_value=0, max_value=180, step=1, value=0)
if st.button("Submit Custom Score"):
    if custom_val > 0:
        process_score(custom_val)

# --- UTILS ---
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
