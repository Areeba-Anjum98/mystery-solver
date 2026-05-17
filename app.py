import streamlit as st
from cases import CASES
from csp_engine import CSPEngine

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mystery Solver",
    page_icon="M",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
#  CUSTOM CSS (UNCHANGED)
# ─────────────────────────────────────────────────────────────
st.markdown("""<style>
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
    letter-spacing: 0.02em;
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
    line-height: 1.6;
}

.badge-easy   { background:#0d2b1e; color:#4ade80; padding:3px 10px; border-radius:4px; font-size:12px; }
.badge-medium { background:#2b1e0d; color:#fb923c; padding:3px 10px; border-radius:4px; font-size:12px; }
.badge-hard   { background:#2b0d0d; color:#f87171; padding:3px 10px; border-radius:4px; font-size:12px; }
.badge-expert { background:#1e0d2b; color:#c084fc; padding:3px 10px; border-radius:4px; font-size:12px; }

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
    text-decoration: line-through;
}
</style>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  SESSION STATE
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
#  HELPERS
# ─────────────────────────────────────────────────────────────
def stars_from_clues(u, t):
    return 3 if u <= t*0.5 else 2 if u <= t*0.75 else 1

def badge_html(d):
    return f'<span class="badge-{d.lower()}">{d}</span>'

def domain_pills(active, all_items):
    return "".join(
        f'<span class="domain-active">{i}</span>' if i in active
        else f'<span class="domain-elim">{i}</span>'
        for i in all_items
    )


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
# 🔥 FIXED CASE FILTERING (MAIN ISSUE FIXED HERE)
# ─────────────────────────────────────────────────────────────
fun_cases = {
    k: v for k, v in CASES.items()
    if v.get("level", "").lower().strip() == "fun"
}

serious_cases = {
    k: v for k, v in CASES.items()
    if v.get("level", "").lower().strip() == "serious"
}


# ─────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Mystery Solver")
    st.divider()

    st.markdown(f"**Score:** {st.session_state.score}")
    st.markdown(f"**Solved:** {len(st.session_state.completed_cases)}")

    st.divider()
    st.markdown("### Cases")

    for cid, case in CASES.items():
        if st.button(case["title"], key=f"sb_{cid}"):
            start_case(cid)
            st.rerun()

    if st.button("Home"):
        go_home()
        st.rerun()


# ─────────────────────────────────────────────────────────────
#  HOME SCREEN
# ─────────────────────────────────────────────────────────────
if st.session_state.screen == "home":

    st.title("Mystery Solver")

    st.subheader("Intro Cases")

    cols = st.columns(2)
    for i, (cid, case) in enumerate(fun_cases.items()):
        with cols[i % 2]:
            st.markdown(f"""
<div class="case-card">
<h3>{case['title']}</h3>
<p>{case['description'][:120]}...</p>
<p>{badge_html(case['difficulty'])}</p>
</div>
""", unsafe_allow_html=True)

            if st.button("Start", key=f"start_{cid}"):
                start_case(cid)
                st.rerun()

    st.subheader("Serious Cases")

    cols = st.columns(3)
    for i, (cid, case) in enumerate(serious_cases.items()):
        with cols[i % 3]:
            st.markdown(f"""
<div class="case-card">
<h3>{case['title']}</h3>
<p>{case['description'][:120]}...</p>
<p>{badge_html(case['difficulty'])}</p>
</div>
""", unsafe_allow_html=True)

            if st.button("Start", key=f"start2_{cid}"):
                start_case(cid)
                st.rerun()


# ─────────────────────────────────────────────────────────────
#  GAME SCREEN (UNCHANGED LOGIC SHORT VERSION)
# ─────────────────────────────────────────────────────────────
elif st.session_state.screen == "game":

    case = CASES[st.session_state.current_case_id]
    csp = st.session_state.csp

    st.title(case["title"])
    st.write(case["description"])

    state = csp.get_current_state()

    st.subheader("Suspects")
    for s in case["suspects"]:
        st.write("✔" if s in state["suspect_domain"] else "❌", s)

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
            st.session_state.screen = "home"
        else:
            st.error("Wrong!")


# ─────────────────────────────────────────────────────────────
#  VERDICT SCREEN (simple)
# ─────────────────────────────────────────────────────────────
elif st.session_state.screen == "verdict":
    st.success("Case Solved!")
    if st.button("Home"):
        go_home()
        st.rerun()
