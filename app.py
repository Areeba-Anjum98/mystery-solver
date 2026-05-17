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
# ORIGINAL DARK THEME CSS (RESTORED)
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background-color: #0f0f1a; }

[data-testid="stSidebar"] {
    background-color: #16213e;
    border-right: 1px solid #2a2a4a;
}

.stApp, .stMarkdown, p, span, label, div {
    color: #e0dff0 !important;
}

h1, h2, h3 { color: #ffffff !important; }

/* Buttons */
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

/* Cards */
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

/* Badges */
.badge-easy   { background:#0d2b1e; color:#4ade80; padding:3px 10px; border-radius:4px; font-size:12px; }
.badge-medium { background:#2b1e0d; color:#fb923c; padding:3px 10px; border-radius:4px; font-size:12px; }
.badge-hard   { background:#2b0d0d; color:#f87171; padding:3px 10px; border-radius:4px; font-size:12px; }
.badge-expert { background:#1e0d2b; color:#c084fc; padding:3px 10px; border-radius:4px; font-size:12px; }

/* Domains */
.domain-active {
    background: #1d3a2a;
    color: #4ade80;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 12px;
    display: inline-block;
    margin: 2px;
}

.domain-elim {
    background: #1a1a2e;
    color: #555577;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 12px;
    display: inline-block;
    margin: 2px;
    text-decoration: line-through;
}

/* Progress */
.stProgress > div > div {
    background-color: #e94560 !important;
}
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
def stars_from_clues(u, t):
    r = u / t
    if r <= 0.5: return 3
    if r <= 0.75: return 2
    return 1

def badge_html(d):
    return f'<span class="badge-{d.lower()}">{d}</span>'

def domain_pills(active, all_items):
    html = ""
    for i in all_items:
        html += f'<span class="domain-active">{i}</span>' if i in active else f'<span class="domain-elim">{i}</span>'
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
    st.markdown("## Mystery Solver")
    st.markdown(f"Score: `{st.session_state.score}`")
    st.markdown(f"Solved: `{len(st.session_state.completed_cases)}`")

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
    st.write("Solve cases using CSP logic and deduction.")
    
    for cid, case in CASES.items():
        st.markdown(f"""
        <div class="case-card">
            <h3>{case['title']}</h3>
            <p>{case['description'][:120]}...</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Start Case {cid}", key=f"start_{cid}"):
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

    state = csp.get_current_state()

    st.subheader("Suspects")
    for s in case["suspects"]:
        st.write("✔" if s in state["suspect_domain"] else "✖", s)

    st.subheader("Clues")

    for i in range(st.session_state.clues_revealed):
        st.write(case["clues"][i]["text"])

    if st.button("Reveal Clue"):
        csp.apply_clue(case["clues"][st.session_state.clues_revealed])
        st.session_state.clues_revealed += 1
        st.rerun()

    st.subheader("Accusation")

    s = st.selectbox("Suspect", case["suspects"])
    l = st.selectbox("Location", case["locations"])
    w = st.selectbox("Weapon", case["weapons"])

    if st.button("Submit"):
        if csp.verify_accusation(s, l, w):
            st.success("Correct!")
            st.session_state.completed_cases.append(st.session_state.current_case_id)
            st.session_state.screen = "home"
            st.rerun()
        else:
            st.error("Wrong answer!")


# ─────────────────────────────────────────────────────────────
# VERDICT SCREEN
# ─────────────────────────────────────────────────────────────
elif st.session_state.screen == "verdict":
    st.success("Case Solved!")
    if st.button("Back Home"):
        go_home()
        st.rerun()
