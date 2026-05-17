import streamlit as st
from cases import CASES
from csp_engine import CSPEngine

# ─────────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mystery Solver",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
# CASE ACCENTS
# ─────────────────────────────────────────────────────────────
CASE_ACCENTS = {
    1: "#F59E0B",
    2: "#38BDF8",
    3: "#10B981",
    4: "#8B5CF6",
    5: "#D4A017",
    6: "#84CC16",
    7: "#DC2626",
}

COLORS = {
    "interactable": "#4FD1C5",
    "solved": "#10B981",
    "hidden": "#8B5CF6",
    "danger": "#EF4444",
    "fun": "#F59E0B",
    "premium": "#D4A017",
}

# ─────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp {
    background: linear-gradient(160deg, #0B0F14 0%, #111827 100%);
}
.case-card {
    background: #18202A;
    border: 1px solid #1E2A38;
    border-radius: 12px;
    padding: 18px;
    margin: 8px 0;
}
.solved-card {
    background: #0D2B1E;
    border: 1px solid #10B981;
    border-radius: 12px;
    padding: 18px;
}
.prop-step {
    background: #0D1117;
    border: 1px solid #1E2A38;
    border-radius: 8px;
    padding: 10px;
    margin: 5px 0;
    font-family: monospace;
}
.badge-easy { color:#34D399; }
.badge-medium { color:#FBBF24; }
.badge-hard { color:#F87171; }
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
def get_accent(case_id):
    return CASE_ACCENTS.get(case_id, "#4FD1C5")

def stars_from_clues(clues_used, total):
    ratio = clues_used / total
    if ratio <= 0.5:
        return 3
    elif ratio <= 0.75:
        return 2
    return 1

def badge_html(diff):
    return f'<span class="badge-{diff.lower()}">{diff}</span>'

def start_case(cid):
    st.session_state.current_case_id = cid
    st.session_state.csp = CSPEngine(CASES[cid])
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

    st.write("Score:", st.session_state.score)

    st.divider()
    for cid, case in CASES.items():
        if st.button(case["title"], key=f"sb_{cid}"):
            start_case(cid)
            st.rerun()

    if st.session_state.screen != "home":
        if st.button("Back"):
            go_home()
            st.rerun()


# ─────────────────────────────────────────────────────────────
# HOME SCREEN
# ─────────────────────────────────────────────────────────────
if st.session_state.screen == "home":
    st.title("Mystery Solver")
    st.write("Solve cases using CSP logic")

    cols = st.columns(2)
    fun_cases = {k:v for k,v in CASES.items() if v["level"]=="fun"}

    for i,(cid,case) in enumerate(fun_cases.items()):
        with cols[i%2]:
            st.markdown(f"""
            <div class="case-card">
                <h3>{case['title']}</h3>
                <p>{case['description'][:100]}...</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Start", key=f"start_{cid}"):
                start_case(cid)
                st.rerun()


# ─────────────────────────────────────────────────────────────
# GAME SCREEN
# ─────────────────────────────────────────────────────────────
elif st.session_state.screen == "game":

    case = CASES[st.session_state.current_case_id]
    csp = st.session_state.csp
    total = len(case["clues"])
    revealed = st.session_state.clues_revealed
    accent = get_accent(st.session_state.current_case_id)

    st.markdown(f"# {case['title']}")
    st.markdown(f"*{case['location']}*")

    st.progress(revealed/total if total else 0)

    st.divider()

    # Suspects
    state = csp.get_current_state()

    st.subheader("Suspects")
    for s in case["suspects"]:
        st.write(s)

    st.subheader("Clues")

    for i in range(revealed):
        st.write(case["clues"][i]["text"])

    if revealed < total:
        if st.button("Reveal Clue"):
            csp.apply_clue(case["clues"][revealed])
            st.session_state.clues_revealed += 1
            st.rerun()

    st.divider()

    st.subheader("Accusation")

    s = st.selectbox("Suspect", case["suspects"])
    l = st.selectbox("Location", case["locations"])
    w = st.selectbox("Weapon", case["weapons"])

    if st.button("Submit"):
        if csp.verify_accusation(s,l,w):
            st.success("Correct!")
            st.session_state.score += 100
            st.session_state.screen = "verdict"
            st.rerun()
        else:
            st.error("Wrong!")


# ─────────────────────────────────────────────────────────────
# VERDICT
# ─────────────────────────────────────────────────────────────
elif st.session_state.screen == "verdict":

    case = CASES[st.session_state.current_case_id]
    solution = case["solution"]

    st.title("Case Closed")

    st.write("Culprit:", solution["culprit"])
    st.write("Location:", solution["location"])
    st.write("Weapon:", solution["weapon"])

    if st.button("Home"):
        go_home()
        st.rerun()

    if st.button("Replay"):
        start_case(st.session_state.current_case_id)
        st.rerun()
