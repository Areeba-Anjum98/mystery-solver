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
# ORIGINAL DETECTIVE CYAN THEME (RESTORED)
# ─────────────────────────────────────────────
st.markdown("""
<style>
.stApp {
    background: linear-gradient(160deg, #0B0F14 0%, #111827 100%);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #0D1117;
    border-right: 1px solid #1E2A38;
}

/* Text */
.stApp, .stMarkdown, p, span, label, div {
    color: #E6EDF3 !important;
}

h1, h2, h3 {
    color: #F9FAFB !important;
}

/* Buttons */
.stButton > button {
    background-color: #4FD1C5;
    color: #0B0F14 !important;
    border-radius: 8px;
    font-weight: 700;
    width: 100%;
    transition: 0.2s;
}
.stButton > button:hover {
    background-color: #38B2AC;
    transform: translateY(-1px);
}

/* Cards */
.case-card {
    background: #1B2430;
    border: 1px solid #1E2A38;
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
}

.solved-card {
    background: #0D2B1E;
    border: 1px solid #10B981;
    border-radius: 12px;
    padding: 16px;
}

/* Clues */
.clue-card-done {
    background: #111827;
    border-left: 3px solid #10B981;
    padding: 12px;
    border-radius: 0 10px 10px 0;
}

/* CSP logs */
.prop-step {
    background: #0D1117;
    border: 1px solid #1E2A38;
    border-radius: 8px;
    padding: 10px;
    font-family: monospace;
    font-size: 12px;
}

/* Badges */
.badge-easy {background:#064E3B;color:#34D399;padding:3px 8px;border-radius:4px;}
.badge-medium {background:#451A03;color:#FBBF24;padding:3px 8px;border-radius:4px;}
.badge-hard {background:#450A0A;color:#F87171;padding:3px 8px;border-radius:4px;}
.badge-expert {background:#2E1065;color:#C084FC;padding:3px 8px;border-radius:4px;}

/* Domains */
.domain-active {
    background:#0D2B1E;color:#34D399;padding:4px 10px;
    border-radius:4px;display:inline-block;margin:2px;
}
.domain-elim {
    background:#111827;color:#374151;text-decoration:line-through;
    padding:4px 10px;border-radius:4px;display:inline-block;margin:2px;
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
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def stars_from_clues(u, t):
    return 3 if u/t <= 0.5 else 2 if u/t <= 0.75 else 1

def badge(d):
    return f'<span class="badge-{d.lower()}">{d}</span>'

def domain(items, all_items):
    return "".join(
        f'<span class="domain-active">{i}</span>' if i in items
        else f'<span class="domain-elim">{i}</span>'
        for i in all_items
    )

def start_case(cid):
    st.session_state.current_case_id = cid
    st.session_state.csp = CSPEngine(CASES[cid])
    st.session_state.clues_revealed = 0
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
    st.write("CSP Detective Game")
    st.divider()

    st.write(f"🏆 Score: {st.session_state.score}")
    st.write(f"✅ Solved: {len(st.session_state.completed_cases)}")
    st.divider()

    for cid, case in CASES.items():
        label = f"{case['title']}"
        if st.button(label, key=f"s_{cid}"):
            start_case(cid)
            st.rerun()

    st.divider()
    if st.button("🏠 Home"):
        go_home()
        st.rerun()


# ─────────────────────────────────────────────
# HOME SCREEN
# ─────────────────────────────────────────────
if st.session_state.screen == "home":

    st.title("🔍 Mystery Solver")

    st.subheader("Fun Cases")
    for cid, case in CASES.items():
        if case["level"] == "fun":
            st.markdown(f"""
            <div class="case-card">
                <h3>{case['title']}</h3>
                <p>{case['description'][:120]}...</p>
                <p>{badge(case['difficulty'])}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Start {case['title']}", key=f"f_{cid}"):
                start_case(cid)
                st.rerun()

    st.subheader("Serious Cases")
    for cid, case in CASES.items():
        if case["level"] == "serious":
            st.markdown(f"""
            <div class="case-card">
                <h3>{case['title']}</h3>
                <p>{case['description'][:120]}...</p>
                <p>{badge(case['difficulty'])}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Start {case['title']}", key=f"c_{cid}"):
                start_case(cid)
                st.rerun()


# ─────────────────────────────────────────────
# GAME SCREEN
# ─────────────────────────────────────────────
elif st.session_state.screen == "game":

    case = CASES[st.session_state.current_case_id]
    csp = st.session_state.csp
    total = len(case["clues"])
    revealed = st.session_state.clues_revealed

    st.title(f"{case['title']}")

    st.progress(revealed / total if total else 0)

    state = csp.get_current_state()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Suspects")
        for s in case["suspects"]:
            st.write("🟡 " + s if s in state["suspect_domain"] else "❌ " + s)

        st.subheader("Locations")
        st.markdown(domain(state["location_domain"], case["locations"]), unsafe_allow_html=True)

        st.subheader("Weapons")
        st.markdown(domain(state["weapon_domain"], case["weapons"]), unsafe_allow_html=True)

    with col2:
        st.subheader("Clues")

        for i in range(revealed):
            st.markdown(f'<div class="clue-card-done">Clue {i+1}: {case["clues"][i]["text"]}</div>',
                        unsafe_allow_html=True)

        if revealed < total:
            if st.button("Reveal Clue"):
                csp.apply_clue(case["clues"][revealed])
                st.session_state.clues_revealed += 1
                st.rerun()

        st.subheader("CSP Log")
        for log in state["propagation_log"]:
            st.markdown(f'<div class="prop-step">{log["propagation"]}</div>',
                        unsafe_allow_html=True)

    st.divider()

    st.subheader("Accusation")

    s = st.selectbox("Suspect", case["suspects"])
    l = st.selectbox("Location", case["locations"])
    w = st.selectbox("Weapon", case["weapons"])

    if st.button("Submit"):
        if csp.verify_accusation(s, l, w):
            stars = stars_from_clues(revealed, total)
            st.session_state.score += stars * 100
            st.session_state.completed_cases.append(st.session_state.current_case_id)
            st.session_state.screen = "verdict"
            st.rerun()
        else:
            st.error("Wrong accusation!")


# ─────────────────────────────────────────────
# VERDICT SCREEN
# ─────────────────────────────────────────────
elif st.session_state.screen == "verdict":

    case = CASES[st.session_state.current_case_id]
    csp = st.session_state.csp
    sol = case["solution"]

    st.success("Case Solved!")

    st.markdown(f"""
    <div class="solved-card">
        <h3>Solution</h3>
        <p>Culprit: {sol['culprit']}</p>
        <p>Location: {sol['location']}</p>
        <p>Weapon: {sol['weapon']}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Home"):
        go_home()
        st.rerun()
