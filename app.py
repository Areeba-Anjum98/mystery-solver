import streamlit as st
from cases import CASES
from csp_engine import CSPEngine

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mystery Solver",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
#  CUSTOM CSS
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
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
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
    color: #a0d4b8 !important;
}

.badge-easy { background:#0d2b1e; color:#4ade80; padding:3px 10px; border-radius:4px; }
.badge-medium { background:#2b1e0d; color:#fb923c; padding:3px 10px; border-radius:4px; }
.badge-hard { background:#2b0d0d; color:#f87171; padding:3px 10px; border-radius:4px; }
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
        "verdict_correct": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def stars_from_clues(clues_used, total):
    ratio = clues_used / total
    if ratio <= 0.5:
        return 3
    elif ratio <= 0.75:
        return 2
    return 1

def badge_html(difficulty):
    return f'<span class="badge-{difficulty.lower()}">{difficulty}</span>'

# SAFE FIX (IMPORTANT)
def domain_pills(active, all_items):
    active = active or []
    html = ""
    for item in all_items:
        if item in active:
            html += f'<span style="color:#4ade80">✓ {item}</span> '
        else:
            html += f'<span style="color:#555;text-decoration:line-through">{item}</span> '
    return html

def start_case(cid):
    case = CASES[cid]
    st.session_state.current_case_id = cid
    st.session_state.csp = CSPEngine(case)
    st.session_state.clues_revealed = 0
    st.session_state.wrong_attempts = 0
    st.session_state.screen = "game"

def go_home():
    st.session_state.screen = "home"
    st.session_state.current_case_id = None
    st.session_state.csp = None

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🕵️ Mystery Solver")

    st.markdown(f"Score: `{st.session_state.score}`")
    st.markdown(f"Cases: `{len(st.session_state.completed_cases)}`")

    st.divider()

    for cid, case in CASES.items():
        label = f"{case['title']}"
        if st.button(label, key=f"sb_{cid}"):
            start_case(cid)
            st.rerun()

    if st.session_state.screen != "home":
        if st.button("🏠 Home"):
            go_home()
            st.rerun()

# ─────────────────────────────────────────────────────────────
# HOME SCREEN
# ─────────────────────────────────────────────────────────────
if st.session_state.screen == "home":

    st.title("🕵️ Mystery Solver")

    st.markdown("Solve cases using logic + CSP elimination.")

    for cid, case in CASES.items():
        st.markdown(f"""
        <div class="case-card">
        <h3>{case['title']}</h3>
        <p>{case['description'][:100]}...</p>
        <p>{badge_html(case['difficulty'])}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Start {case['title']}", key=f"start_{cid}"):
            start_case(cid)
            st.rerun()

# ─────────────────────────────────────────────────────────────
# GAME SCREEN
# ─────────────────────────────────────────────────────────────
elif st.session_state.screen == "game":

    case = CASES[st.session_state.current_case_id]
    csp = st.session_state.csp

    st.title(case['title'])

    st.markdown("### Suspects")
    state = csp.get_current_state()

    for s in case["suspects"]:
        status = "ACTIVE" if s in state["suspect_domain"] else "ELIMINATED"
        st.write(f"{s} - {status}")

    st.divider()

    if st.button("Reveal Clue"):
        if st.session_state.clues_revealed < len(case["clues"]):
            clue = case["clues"][st.session_state.clues_revealed]
            csp.apply_clue(clue)
            st.session_state.clues_revealed += 1
            st.rerun()

    st.divider()

    st.markdown("### Accusation")

    suspect = st.selectbox("Suspect", case["suspects"])
    location = st.selectbox("Location", case["locations"])
    weapon = st.selectbox("Weapon", case["weapons"])

    if st.button("Submit"):
        if csp.verify_accusation(suspect, location, weapon):
            st.success("Correct!")

            stars = stars_from_clues(
                st.session_state.clues_revealed,
                len(case["clues"])
            )

            st.session_state.score += stars * 100
            st.session_state.completed_cases.append(st.session_state.current_case_id)

            st.session_state.screen = "home"
            st.rerun()
        else:
            st.error("Wrong accusation")

# ─────────────────────────────────────────────────────────────
# END
# ─────────────────────────────────────────────────────────────
