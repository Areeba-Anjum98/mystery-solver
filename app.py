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
#  PER-CASE ACCENT COLORS
#  Only clue highlights, evidence glow, borders, progress line
#  change per case. Base UI stays constant.
# ─────────────────────────────────────────────────────────────
CASE_ACCENTS = {
    1: "#F59E0B",   # Missing Cake         — Warm Orange  (playful)
    2: "#38BDF8",   # Lost Homework         — Sky Blue     (youthful)
    3: "#10B981",   # Bank Transfer         — Emerald      (finance)
    4: "#8B5CF6",   # Stolen Research       — Purple       (science)
    5: "#D4A017",   # Corporate Sabotage    — Gold         (corruption)
    6: "#84CC16",   # Hospital Poisoning    — Toxic Green  (medical)
    7: "#DC2626",   # Witness Disappearance — Crimson      (tension)
}

# State color system — players learn this subconsciously
COLORS = {
    "interactable": "#4FD1C5",   # Cyan    — buttons, active elements
    "solved":       "#10B981",   # Green   — solved / confirmed
    "hidden":       "#8B5CF6",   # Purple  — hidden clue
    "danger":       "#EF4444",   # Red     — wrong / error
    "fun":          "#F59E0B",   # Orange  — optional / fun
    "premium":      "#D4A017",   # Gold    — rare / premium clue
}

# ─────────────────────────────────────────────────────────────
#  GLOBAL CSS — permanent, never changes per case
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Global base ─────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

.stApp {
    background: linear-gradient(160deg, #0B0F14 0%, #111827 100%);
    font-family: 'Inter', sans-serif;
}

/* ── Sidebar ─────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #0D1117;
    border-right: 1px solid #1E2A38;
}

/* ── Typography ──────────────────────────────── */
.stApp, .stMarkdown, p, span, label, div {
    color: #E6EDF3 !important;
}
h1 { color: #F9FAFB !important; font-size: 2rem !important; letter-spacing: -0.02em; }
h2 { color: #F9FAFB !important; }
h3 { color: #E6EDF3 !important; }

/* ── Buttons — Cyan interactive color ────────── */
.stButton > button {
    background-color: #4FD1C5;
    color: #0B0F14 !important;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    font-size: 13px;
    width: 100%;
    letter-spacing: 0.02em;
    transition: all 0.2s ease;
}
.stButton > button:hover {
    background-color: #38B2AC;
    color: #0B0F14 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(79, 209, 197, 0.3);
}

/* ── Base card — surface color ───────────────── */
.case-card {
    background: #18202A;
    border: 1px solid #1E2A38;
    border-radius: 12px;
    padding: 18px;
    margin: 8px 0;
    transition: border-color 0.2s;
}
.case-card:hover {
    border-color: #2E3E50;
}

/* ── Solved card — green glow ────────────────── */
.solved-card {
    background: #0D2B1E;
    border: 1px solid #10B981;
    border-radius: 12px;
    padding: 18px;
    margin: 8px 0;
}

/* ── Clue cards ──────────────────────────────── */
.clue-card-done {
    background: #111827;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    margin: 6px 0;
    /* accent border injected inline per case */
}

/* ── CSP trace box ───────────────────────────── */
.prop-step {
    background: #0D1117;
    border: 1px solid #1E2A38;
    border-radius: 8px;
    padding: 10px 14px;
    margin: 5px 0;
    font-family: 'Courier New', monospace;
    font-size: 12px;
    color: #9CA3AF !important;
    line-height: 1.7;
}

/* ── Difficulty badges ───────────────────────── */
.badge-easy   { background:#064E3B; color:#34D399; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:600; letter-spacing:0.04em; }
.badge-medium { background:#451A03; color:#FBBF24; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:600; letter-spacing:0.04em; }
.badge-hard   { background:#450A0A; color:#F87171; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:600; letter-spacing:0.04em; }
.badge-expert { background:#2E1065; color:#C084FC; padding:3px 10px; border-radius:4px; font-size:11px; font-weight:600; letter-spacing:0.04em; }

/* ── Domain pills ────────────────────────────── */
.domain-active {
    background: #0D2B1E;
    color: #34D399;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 12px;
    display: inline-block;
    margin: 2px;
    font-weight: 500;
    border: 1px solid #10B981;
}
.domain-elim {
    background: #111827;
    color: #374151;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 12px;
    display: inline-block;
    margin: 2px;
    text-decoration: line-through;
    border: 1px solid #1E2A38;
}

/* ── Locked case style ───────────────────────── */
.locked-card {
    background: #111827;
    border: 1px solid #1F2937;
    border-radius: 12px;
    padding: 18px;
    margin: 8px 0;
    opacity: 0.55;
}

/* ── Selectbox ───────────────────────────────── */
.stSelectbox > div > div {
    background-color: #18202A !important;
    border-color: #1E2A38 !important;
    color: #E6EDF3 !important;
}

/* ── Progress bar ────────────────────────────── */
.stProgress > div > div {
    background-color: #4FD1C5 !important;
}

/* ── Streamlit alerts ────────────────────────── */
.stSuccess { background: #0D2B1E !important; border: 1px solid #10B981 !important; }
.stError   { background: #1C0A0A !important; border: 1px solid #EF4444 !important; }
.stWarning { background: #1C1208 !important; border: 1px solid #F59E0B !important; }
.stInfo    { background: #0D1F2B !important; border: 1px solid #4FD1C5 !important; }

/* ── Divider ─────────────────────────────────── */
hr { border-color: #1E2A38 !important; }

/* ── Section label ───────────────────────────── */
.section-label {
    font-size: 11px;
    font-weight: 600;
    color: #4FD1C5 !important;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  SESSION STATE
# ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "screen":          "home",
        "current_case_id": None,
        "csp":             None,
        "clues_revealed":  0,
        "score":           0,
        "completed_cases": [],
        "case_stars":      {},
        "wrong_attempts":  0,
        "verdict_correct": None,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_state()


# ─────────────────────────────────────────────────────────────
#  HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────
def get_accent(case_id: int) -> str:
    return CASE_ACCENTS.get(case_id, "#4FD1C5")

def stars_from_clues(clues_used: int, total_clues: int) -> int:
    ratio = clues_used / total_clues
    if ratio <= 0.5:   return 3
    if ratio <= 0.75:  return 2
    return 1

def badge_html(difficulty: str) -> str:
    return f'<span class="badge-{difficulty.lower()}">{difficulty}</span>'

def domain_pills(active: list, all_items: list) -> str:
    html = ""
    for item in all_items:
        if item in active:
            html += f'<span class="domain-active">{item}</span>'
        else:
            html += f'<span class="domain-elim">{item}</span>'
    return html

def star_display(count: int) -> str:
    filled = "&#9733;" * count
    empty  = "&#9734;" * (3 - count)
    return (
        f'<span style="color:#D4A017; font-size:24px;">{filled}</span>'
        f'<span style="color:#374151; font-size:24px;">{empty}</span>'
    )

def start_case(case_id: int):
    case = CASES[case_id]
    st.session_state.current_case_id = case_id
    st.session_state.csp             = CSPEngine(case)
    st.session_state.clues_revealed  = 0
    st.session_state.wrong_attempts  = 0
    st.session_state.verdict_correct = None
    st.session_state.screen          = "game"

def go_home():
    st.session_state.screen          = "home"
    st.session_state.current_case_id = None
    st.session_state.csp             = None


# ─────────────────────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<p style="font-size:20px; font-weight:700; color:#F9FAFB; margin:0;">Mystery Solver</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p style="font-size:12px; color:#9CA3AF; margin-top:2px;">A CSP-Based Detective Game</p>',
        unsafe_allow_html=True
    )
    st.divider()

    # Score and progress
    st.markdown(
        f'<p style="font-size:13px; color:#9CA3AF;">Total Score</p>'
        f'<p style="font-size:24px; font-weight:700; color:#4FD1C5; margin-top:-8px;">{st.session_state.score}</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<p style="font-size:13px; color:#9CA3AF;">Cases Solved</p>'
        f'<p style="font-size:20px; font-weight:600; color:#10B981; margin-top:-8px;">'
        f'{len(st.session_state.completed_cases)} / {len(CASES)}</p>',
        unsafe_allow_html=True
    )
    st.divider()

    # Case list
    st.markdown('<p class="section-label">All Cases</p>', unsafe_allow_html=True)
    for cid, case in CASES.items():
        accent   = get_accent(cid)
        stars    = st.session_state.case_stars.get(cid, 0)
        star_str = " [" + ("*" * stars) + "]" if stars else ""
        solved   = cid in st.session_state.completed_cases
        status   = "[Solved]" if solved else "[Open]"
        label    = f"{status} Case {cid} — {case['title']}{star_str}"
        if st.button(label, key=f"sb_{cid}"):
            start_case(cid)
            st.rerun()

    st.divider()

    with st.expander("AI Concepts Used"):
        st.markdown("""
**CSP (Constraint Satisfaction)**
Variables: Suspect, Location, Weapon
Domains: All values possible at start
Constraints: Each clue removes values

**Constraint Propagation**
Each clue triggers chain elimination
Arc consistency maintained throughout

**Backtracking**
Used when red herrings mislead
Explores alternatives automatically

**Logical Agents**
Knowledge base updates each clue
IF-THEN deduction rules applied
        """)

    if st.session_state.screen != "home":
        st.divider()
        if st.button("Back to Home"):
            go_home()
            st.rerun()


# ─────────────────────────────────────────────────────────────
#  SCREEN 1 — HOME
# ─────────────────────────────────────────────────────────────
if st.session_state.screen == "home":

    # Header
    st.markdown("""
<div style="padding: 32px 0 16px;">
    <p style="font-size:11px; font-weight:600; color:#4FD1C5;
              text-transform:uppercase; letter-spacing:0.12em; margin-bottom:6px;">
        CSP Detective Game
    </p>
    <h1 style="font-size:2.4rem; font-weight:700; margin:0; color:#F9FAFB;">
        Mystery Solver
    </h1>
    <p style="color:#9CA3AF; font-size:15px; margin-top:8px;">
        Use logic and constraint propagation to eliminate suspects and solve each case.
    </p>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ── Introductory cases ───────────────────────────────────
    st.markdown('<p class="section-label">Introductory Cases — Warm Up</p>', unsafe_allow_html=True)
    fun_cols  = st.columns(2)
    fun_cases = {k: v for k, v in CASES.items() if v["level"] == "fun"}

    for i, (cid, case) in enumerate(fun_cases.items()):
        accent   = get_accent(cid)
        stars    = st.session_state.case_stars.get(cid, 0)
        star_str = " [" + ("*" * stars) + "]" if stars else ""
        solved   = cid in st.session_state.completed_cases
        status   = "SOLVED" if solved else "OPEN"
        s_color  = COLORS["solved"] if solved else "#9CA3AF"

        with fun_cols[i % 2]:
            st.markdown(f"""
<div class="case-card" style="border-left: 3px solid {accent};">
    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <div>
            <p style="font-size:16px; font-weight:600; color:#F9FAFB; margin:0 0 2px;">
                {case['title']}
            </p>
            <p style="font-size:11px; color:#9CA3AF; margin:0 0 10px;">
                {case['location']}
            </p>
        </div>
        <span style="font-size:11px; font-weight:700; color:{s_color};
                     background:#111827; padding:3px 8px; border-radius:4px;">
            {status}{star_str}
        </span>
    </div>
    <p style="color:#9CA3AF; font-size:13px; margin:0 0 12px; line-height:1.5;">
        {case['description'][:130]}...
    </p>
    <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
        {badge_html(case['difficulty'])}
        <span style="font-size:11px; color:#4B5563;">
            {len(case['suspects'])} suspects &nbsp;·&nbsp;
            {len(case['locations'])} locations &nbsp;·&nbsp;
            {len(case['clues'])} clues
        </span>
    </div>
</div>
""", unsafe_allow_html=True)
            label = f"Replay — {case['title']}" if solved else f"Start — {case['title']}"
            if st.button(label, key=f"start_{cid}"):
                start_case(cid)
                st.rerun()

    st.divider()

    # ── Investigation cases ──────────────────────────────────
    st.markdown('<p class="section-label">Investigation Cases — Real Mysteries</p>', unsafe_allow_html=True)
    serious_cases = {k: v for k, v in CASES.items() if v["level"] == "serious"}
    cols = st.columns(3)

    for i, (cid, case) in enumerate(serious_cases.items()):
        accent   = get_accent(cid)
        stars    = st.session_state.case_stars.get(cid, 0)
        star_str = " [" + ("*" * stars) + "]" if stars else ""
        solved   = cid in st.session_state.completed_cases
        status   = "SOLVED" if solved else "OPEN"
        s_color  = COLORS["solved"] if solved else "#9CA3AF"

        with cols[i % 3]:
            st.markdown(f"""
<div class="case-card" style="border-left: 3px solid {accent};">
    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
        <p style="font-size:15px; font-weight:600; color:#F9FAFB; margin:0 0 2px;">
            {case['title']}
        </p>
        <span style="font-size:10px; font-weight:700; color:{s_color};
                     background:#111827; padding:2px 7px; border-radius:4px; white-space:nowrap;">
            {status}{star_str}
        </span>
    </div>
    <p style="font-size:11px; color:#9CA3AF; margin:0 0 8px;">{case['location']}</p>
    <p style="color:#9CA3AF; font-size:12px; margin:0 0 10px; line-height:1.5;">
        {case['description'][:110]}...
    </p>
    <div style="display:flex; align-items:center; gap:8px;">
        {badge_html(case['difficulty'])}
        <span style="font-size:11px; color:#4B5563;">
            {len(case['suspects'])} suspects · {len(case['clues'])} clues
        </span>
    </div>
</div>
""", unsafe_allow_html=True)
            label = f"Replay — {case['title']}" if solved else f"Start — {case['title']}"
            if st.button(label, key=f"start_{cid}"):
                start_case(cid)
                st.rerun()


# ─────────────────────────────────────────────────────────────
#  SCREEN 2 — GAME
# ─────────────────────────────────────────────────────────────
elif st.session_state.screen == "game":

    case        = CASES[st.session_state.current_case_id]
    csp         = st.session_state.csp
    total_clues = len(case["clues"])
    revealed    = st.session_state.clues_revealed
    accent      = get_accent(st.session_state.current_case_id)

    # ── Case banner — accent color per case ─────────────────
    st.markdown(f"""
<div style="background: linear-gradient(90deg, {accent}18 0%, #111827 100%);
            border-left: 4px solid {accent};
            border-radius: 0 10px 10px 0;
            padding: 16px 20px; margin-bottom: 16px;">
    <p style="font-size:11px; font-weight:600; color:{accent};
              text-transform:uppercase; letter-spacing:0.1em; margin:0 0 4px;">
        Active Case
    </p>
    <p style="font-size:22px; font-weight:700; color:#F9FAFB; margin:0;">
        {case['title']}
    </p>
    <p style="font-size:13px; color:#9CA3AF; margin:4px 0 0;">
        {case['location']}
    </p>
</div>
""", unsafe_allow_html=True)

    # ── Top meta bar ─────────────────────────────────────────
    col_prog, col_score = st.columns([2, 1])
    with col_prog:
        st.markdown(
            f'<p style="font-size:12px; color:#9CA3AF; margin-bottom:4px;">'
            f'Clues Used: {revealed} / {total_clues}</p>',
            unsafe_allow_html=True
        )
        # Accent-colored progress bar via CSS override
        st.markdown(
            f'<style>.stProgress > div > div {{ background-color: {accent} !important; }}</style>',
            unsafe_allow_html=True
        )
        st.progress(revealed / total_clues if total_clues else 0)
    with col_score:
        st.markdown(
            f'<p style="font-size:12px; color:#9CA3AF;">Score</p>'
            f'<p style="font-size:20px; font-weight:700; color:#4FD1C5; margin-top:-6px;">'
            f'{st.session_state.score}</p>',
            unsafe_allow_html=True
        )

    # ── Case description ─────────────────────────────────────
    with st.expander("Case Description", expanded=True):
        st.markdown(f'<p style="color:#D1D5DB; line-height:1.7;">{case["description"]}</p>', unsafe_allow_html=True)
        st.markdown(
            f'<div style="border-left:3px solid {accent}; padding:8px 14px; background:#111827; '
            f'border-radius:0 8px 8px 0; margin-top:8px;">'
            f'<p style="color:{accent}; font-size:13px; font-style:italic; margin:0;">'
            f'"{case["quote"]}"</p></div>',
            unsafe_allow_html=True
        )

    st.divider()

    # ── Main layout ──────────────────────────────────────────
    left_col, right_col = st.columns([1, 1])

    # LEFT — Suspects + Domains
    with left_col:
        st.markdown('<p class="section-label">Suspects</p>', unsafe_allow_html=True)
        state = csp.get_current_state()

        for suspect in case["suspects"]:
            role = case["suspect_roles"][suspect]
            if suspect in state["suspect_domain"]:
                border = accent
                name_color   = "#F9FAFB"
                status_color = accent
                status_label = "ACTIVE"
                bg = "#18202A"
            else:
                border = "#1E2A38"
                name_color   = "#374151"
                status_color = "#374151"
                status_label = "ELIMINATED"
                bg = "#0D1117"
            st.markdown(
                f'<div style="background:{bg}; border-radius:8px; padding:10px 14px; '
                f'margin:5px 0; border-left:3px solid {border};">'
                f'<span style="color:{name_color}; font-weight:600; font-size:13px;">{suspect}</span>'
                f'<span style="color:#4B5563; font-size:11px;"> — {role}</span>'
                f'<span style="float:right; font-size:10px; font-weight:700; '
                f'color:{status_color}; letter-spacing:0.05em;">{status_label}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown('<p class="section-label" style="margin-top:16px;">Locations</p>', unsafe_allow_html=True)
        st.markdown(domain_pills(state["location_domain"], case["locations"]), unsafe_allow_html=True)

        st.markdown('<p class="section-label" style="margin-top:16px;">Methods / Weapons</p>', unsafe_allow_html=True)
        st.markdown(domain_pills(state["weapon_domain"], case["weapons"]), unsafe_allow_html=True)

    # RIGHT — Clues + Propagation Trace
    with right_col:
        st.markdown('<p class="section-label">Evidence Log</p>', unsafe_allow_html=True)

        for i in range(revealed):
            clue = case["clues"][i]
            st.markdown(
                f'<div style="background:#111827; border-left:3px solid {accent}; '
                f'border-radius:0 8px 8px 0; padding:10px 14px; margin:6px 0;">'
                f'<span style="color:{accent}; font-weight:600; font-size:12px;">'
                f'Clue {clue["id"]}</span>'
                f'<p style="color:#D1D5DB; font-size:13px; margin:4px 0 0; line-height:1.5;">'
                f'{clue["text"]}</p>'
                f'</div>',
                unsafe_allow_html=True
            )

        if revealed < total_clues:
            if st.button(f"Reveal Clue {revealed + 1}", use_container_width=True):
                csp.apply_clue(case["clues"][revealed])
                st.session_state.clues_revealed += 1
                st.rerun()
        else:
            st.success("All clues revealed. Make your accusation below.")

        # CSP Trace
        st.markdown('<p class="section-label" style="margin-top:16px;">CSP Propagation Trace</p>', unsafe_allow_html=True)
        log = csp.get_current_state()["propagation_log"]

        if not log:
            st.markdown(
                '<div class="prop-step" style="color:#374151 !important;">'
                'No clues applied yet. Reveal the first clue to begin.'
                '</div>',
                unsafe_allow_html=True
            )
        for entry in log:
            st.markdown(
                f'<div class="prop-step">'
                f'<span style="color:{accent}; font-weight:600;">[ Clue {entry["clue_id"]} ]</span> '
                f'<span style="color:#9CA3AF;">{entry["propagation"]}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

    st.divider()

    # ── Accusation ───────────────────────────────────────────
    st.markdown('<p class="section-label">Final Accusation</p>', unsafe_allow_html=True)

    if csp.get_current_state()["solved"]:
        st.info("CSP has logically resolved the case. Confirm your accusation below.")

    acc_col1, acc_col2, acc_col3 = st.columns(3)
    with acc_col1:
        suspect_choice  = st.selectbox("Culprit",   options=case["suspects"],  index=0)
    with acc_col2:
        location_choice = st.selectbox("Location",  options=case["locations"], index=0)
    with acc_col3:
        weapon_choice   = st.selectbox("Method",    options=case["weapons"],   index=0)

    st.warning("An incorrect accusation will reset your clue progress for this case.")

    if st.button("Submit Accusation", use_container_width=True):
        correct = csp.verify_accusation(suspect_choice, location_choice, weapon_choice)
        if correct:
            stars  = stars_from_clues(revealed, total_clues)
            points = stars * 100 + max(0, (total_clues - revealed) * 20)
            st.session_state.score += points
            st.session_state.case_stars[st.session_state.current_case_id] = stars
            if st.session_state.current_case_id not in st.session_state.completed_cases:
                st.session_state.completed_cases.append(st.session_state.current_case_id)
            st.session_state.screen = "verdict"
            st.rerun()
        else:
            st.session_state.wrong_attempts += 1
            st.error(
                f"Incorrect accusation. ({st.session_state.wrong_attempts} wrong attempt(s)). "
                f"Reveal more clues and try again."
            )


# ─────────────────────────────────────────────────────────────
#  SCREEN 3 — VERDICT
# ─────────────────────────────────────────────────────────────
elif st.session_state.screen == "verdict":

    case     = CASES[st.session_state.current_case_id]
    csp      = st.session_state.csp
    stars    = st.session_state.case_stars.get(st.session_state.current_case_id, 1)
    solution = case["solution"]
    accent   = get_accent(st.session_state.current_case_id)
    points   = stars * 100 + max(0, (len(case["clues"]) - st.session_state.clues_revealed) * 20)

    # Verdict banner
    st.markdown(f"""
<div style="background: linear-gradient(90deg, {COLORS['solved']}18 0%, #111827 100%);
            border-left: 4px solid {COLORS['solved']};
            border-radius: 0 10px 10px 0;
            padding: 16px 20px; margin-bottom: 20px;">
    <p style="font-size:11px; font-weight:600; color:{COLORS['solved']};
              text-transform:uppercase; letter-spacing:0.1em; margin:0 0 4px;">
        Case Closed
    </p>
    <p style="font-size:22px; font-weight:700; color:#F9FAFB; margin:0;">
        {case['title']}
    </p>
</div>
""", unsafe_allow_html=True)

    # Verdict card
    st.markdown(f"""
<div class="solved-card">
    <p style="font-size:16px; font-weight:600; color:{COLORS['solved']}; margin:0 0 16px;">
        Accusation Correct. Case Solved.
    </p>
    <table width="100%" style="border-collapse:separate; border-spacing:0 4px;">
        <tr>
            <td style="color:#6B7280; padding:6px 0; width:160px; font-size:13px;">Culprit</td>
            <td style="color:#F9FAFB; font-weight:600; font-size:14px;">{solution['culprit']}</td>
        </tr>
        <tr>
            <td style="color:#6B7280; padding:6px 0; font-size:13px;">Location</td>
            <td style="color:#F9FAFB; font-weight:600; font-size:14px;">{solution['location']}</td>
        </tr>
        <tr>
            <td style="color:#6B7280; padding:6px 0; font-size:13px;">Method Used</td>
            <td style="color:#F9FAFB; font-weight:600; font-size:14px;">{solution['weapon']}</td>
        </tr>
        <tr>
            <td style="color:#6B7280; padding:6px 0; font-size:13px;">Clues Used</td>
            <td style="color:#F9FAFB; font-weight:600; font-size:14px;">
                {st.session_state.clues_revealed} / {len(case['clues'])}
            </td>
        </tr>
        <tr>
            <td style="color:#6B7280; padding:6px 0; font-size:13px;">CSP Steps</td>
            <td style="color:#F9FAFB; font-weight:600; font-size:14px;">
                {len(csp.get_current_state()['propagation_log'])} propagations
            </td>
        </tr>
        <tr>
            <td style="color:#6B7280; padding:6px 0; font-size:13px;">Points Earned</td>
            <td style="color:#D4A017; font-weight:700; font-size:16px;">{points} pts</td>
        </tr>
    </table>
    <div style="margin-top:16px;">
        <p style="font-size:12px; color:#6B7280; margin-bottom:4px;">Rating</p>
        {star_display(stars)}
    </div>
</div>
""", unsafe_allow_html=True)

    # Full CSP trace
    st.markdown('<p class="section-label" style="margin-top:20px;">Full CSP Reasoning Trace</p>', unsafe_allow_html=True)

    for entry in csp.get_current_state()["propagation_log"]:
        eliminated = []
        if entry["changed"]["suspects"]:
            eliminated.append(f"Suspects removed: {', '.join(entry['changed']['suspects'])}")
        if entry["changed"]["locations"]:
            eliminated.append(f"Locations removed: {', '.join(entry['changed']['locations'])}")
        if entry["changed"]["weapons"]:
            eliminated.append(f"Weapons removed: {', '.join(entry['changed']['weapons'])}")
        elim_text = " | ".join(eliminated) if eliminated else "Contextual reasoning — no direct elimination"

        st.markdown(f"""
<div class="prop-step">
    <span style="color:{accent}; font-weight:600;">[ Clue {entry['clue_id']} ]</span>
    <span style="color:#D1D5DB;"> {entry['clue_text']}</span><br>
    <span style="color:#F59E0B;">&gt;&gt; {entry['propagation']}</span><br>
    <span style="color:#4FD1C5;">&gt;&gt; {elim_text}</span>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # Navigation
    btn_col1, btn_col2, btn_col3 = st.columns(3)

    with btn_col1:
        if st.button("Back to Home", use_container_width=True):
            go_home()
            st.rerun()

    with btn_col2:
        if st.button("Replay This Case", use_container_width=True):
            start_case(st.session_state.current_case_id)
            st.rerun()

    with btn_col3:
        next_case = None
        for cid in CASES:
            if cid not in st.session_state.completed_cases:
                next_case = cid
                break
        if next_case:
            if st.button(f"Next — {CASES[next_case]['title']}", use_container_width=True):
                start_case(next_case)
                st.rerun()
        else:
            st.success("All cases solved. You are the ultimate detective.")
