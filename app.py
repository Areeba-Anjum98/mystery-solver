import streamlit as st
from cases import CASES
from csp_engine import CSPEngine

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Mystery Solver",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# DARK THEME CSS (UNCHANGED)
# ─────────────────────────────────────────────
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

.stButton > button:hover {
    background-color: #c73652;
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
    padding: 8px 12px;
    margin: 4px 0;
    font-family: monospace;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
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
        "verdict_correct": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def start_case(case_id):
    case = CASES[case_id]
    st.session_state.current_case_id = case_id
    st.session_state.csp = CSPEngine(case)
    st.session_state.clues_revealed = 0
    st.session_state.wrong_attempts = 0
    st.session_state.screen = "game"


def go_home():
    st.session_state.screen = "home"
    st.session_state.current_case_id = None
    st.session_state.csp = None


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.title("🔍 Mystery Solver")
    st.write(f"🏆 Score: {st.session_state.score}")

    for cid, case in CASES.items():
        if st.button(case["title"], key=f"s_{cid}"):
            start_case(cid)
            st.rerun()

    st.divider()

    # ── UPDATED AI CONCEPTS ──
    with st.expander("🧠 AI Concepts Used"):
        st.markdown("""
**Constraint Satisfaction Problem (CSP)**
- Suspect, Location, Weapon as variables  
- Each clue reduces possible values  

**Constraint Propagation**
- Clues automatically eliminate invalid options  
- Domains shrink step by step  

**Logical Reasoning System**
- Final answer derived through deduction  
- Works like a detective logic engine  
        """)

    if st.button("🏠 Home"):
        go_home()
        st.rerun()


# ─────────────────────────────────────────────
# HOME SCREEN
# ─────────────────────────────────────────────
if st.session_state.screen == "home":
    st.title("🔍 Mystery Solver")
    st.write("Solve mysteries using logic + CSP reasoning.")
    st.info("Select a case from sidebar to start.")


# ─────────────────────────────────────────────
# GAME SCREEN
# ─────────────────────────────────────────────
elif st.session_state.screen == "game":

    case = CASES[st.session_state.current_case_id]
    csp = st.session_state.csp

    st.title(case["title"])
    st.write(case["description"])

    # Reveal clues
    if st.button("👁 Reveal Next Clue"):
        if st.session_state.clues_revealed < len(case["clues"]):
            clue = case["clues"][st.session_state.clues_revealed]
            csp.apply_clue(clue)
            st.session_state.clues_revealed += 1
            st.rerun()

    st.subheader("🔎 Clues")
    for i in range(st.session_state.clues_revealed):
        st.write(case["clues"][i]["text"])

    st.subheader("⚖️ Accusation")

    suspect = st.selectbox("Suspect", case["suspects"])
    location = st.selectbox("Location", case["locations"])
    weapon = st.selectbox("Weapon", case["weapons"])

    if st.button("Submit"):
        if csp.verify_accusation(suspect, location, weapon):
            st.success("Correct! 🎉 Case Solved")
            st.session_state.score += 100
            st.session_state.screen = "home"
            st.rerun()
        else:
            st.error("Wrong! Try again.")


# ─────────────────────────────────────────────
# VERDICT SCREEN
# ─────────────────────────────────────────────
elif st.session_state.screen == "verdict":

    case = CASES[st.session_state.current_case_id]

    st.title("🎉 Case Solved!")

    st.success(f"🕵️ Culprit: {case['solution']['culprit']}")
    st.success(f"📍 Location: {case['solution']['location']}")
    st.success(f"🔧 Weapon: {case['solution']['weapon']}")

    if st.button("🏠 Back Home"):
        go_home()
        st.rerun()
