import streamlit as st
from cases import CASES
from csp_engine import CSPEngine

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mystery Solver",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# CSS (ORIGINAL — unchanged)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background-color: #0f0f1a; }

[data-testid="stSidebar"] {
    background-color: #16213e;
    border-right: 1px solid #2a2a4a;
}

.stApp, .stMarkdown, p, span, label { color: #e0dff0 !important; }

h1, h2, h3 { color: #ffffff !important; }

.stButton > button {
    background-color: #e94560;
    color: white !important;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    width: 100%;
}

.case-card {
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
}

.solved-card {
    background: #0d2b1e;
    border: 1px solid #1d9e75;
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
}

.clue-card-done {
    background: #0d2b1e;
    border-left: 3px solid #1d9e75;
    padding: 12px;
    margin: 6px 0;
}

.prop-step {
    background: #12122a;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 8px;
    margin: 4px 0;
    font-family: monospace;
}

.badge-easy { color:#4ade80; }
.badge-medium { color:#fb923c; }
.badge-hard { color:#f87171; }
.badge-expert { color:#c084fc; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "screen": "home",
        "current_case_id": None,
        "csp": None,
        "clues_revealed": 0,
        "score": 0,
        "completed_cases": [],
        "case_stars": {},
        "wrong_attempts": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def start_case(cid):
    case = CASES[cid]
    st.session_state.current_case_id = cid
    st.session_state.csp = CSPEngine(case)
    st.session_state.clues_revealed = 0
    st.session_state.screen = "game"

def go_home():
    st.session_state.screen = "home"
    st.session_state.current_case_id = None
    st.session_state.csp = None

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Mystery Solver")

    st.write(f"Score: {st.session_state.score}")

    st.divider()

    for cid, case in CASES.items():
        if st.button(case["title"], key=f"sb_{cid}"):
            start_case(cid)
            st.rerun()

    if st.button("Home"):
        go_home()
        st.rerun()

# ─────────────────────────────────────────────────────────────
# HOME SCREEN
# ─────────────────────────────────────────────────────────────
if st.session_state.screen == "home":

    st.title("Mystery Solver")

    st.subheader("Cases")

    fun_cases = {k: v for k, v in CASES.items() if v["level"] == "fun"}
    serious_cases = {k: v for k, v in CASES.items() if v["level"] == "serious"}

    st.markdown("## Fun Cases")

    for cid, case in fun_cases.items():
        st.markdown(f"""
        <div class="case-card">
        <h3>{case['title']}</h3>
        <p>{case['description'][:120]}...</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Start {case['title']}", key=f"start_fun_{cid}"):
            start_case(cid)
            st.rerun()

    st.markdown("## Serious Cases")

    # FIXED GRID (IMPORTANT)
    serious_list = list(serious_cases.items())

    for i in range(0, len(serious_list), 3):
        cols = st.columns(3)
        row = serious_list[i:i+3]

        for j, (cid, case) in enumerate(row):
            with cols[j]:

                st.markdown(f"""
                <div class="case-card">
                    <h4>{case['title']}</h4>
                    <p>{case['location']}</p>
                    <p>{case['description'][:100]}...</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"Start {case['title']}", key=f"start_ser_{cid}"):
                    start_case(cid)
                    st.rerun()

# ─────────────────────────────────────────────────────────────
# GAME SCREEN
# ─────────────────────────────────────────────────────────────
elif st.session_state.screen == "game":

    case = CASES[st.session_state.current_case_id]
    csp = st.session_state.csp

    st.title(case["title"])

    st.write(case["description"])

    st.divider()

    revealed = st.session_state.clues_revealed

    for i in range(revealed):
        clue = case["clues"][i]
        st.write("Clue:", clue["text"])

    if revealed < len(case["clues"]):
        if st.button("Next Clue"):
            csp.apply_clue(case["clues"][revealed])
            st.session_state.clues_revealed += 1
            st.rerun()

    st.divider()

    st.subheader("Accusation")

    s = st.selectbox("Suspect", case["suspects"])
    l = st.selectbox("Location", case["locations"])
    w = st.selectbox("Weapon", case["weapons"])

    if st.button("Submit"):
        if csp.verify_accusation(s, l, w):
            st.success("Correct!")
            st.session_state.screen = "home"
        else:
            st.error("Wrong!")
