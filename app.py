# ─────────────────────────────────────────────────────────────
# app.py
# Mystery Solver — CSP + AC-3 Detective Game
# ─────────────────────────────────────────────────────────────

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
# MODERNIZED ORIGINAL DARK THEME
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0f0f1a;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #2a2a4a;
}

/* All text */
.stApp,
.stMarkdown,
p,
span,
label {
    color: #e0dff0 !important;
}

/* Headings */
h1, h2, h3 {
    color: #ffffff !important;
    letter-spacing: 0.02em;
}

/* Buttons */
.stButton > button {
    background-color: #e94560;
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
    width: 100%;
    letter-spacing: 0.02em;
    transition: all 0.2s ease;
}

/* Button hover */
.stButton > button:hover {
    background-color: #c73652;
    color: white !important;
    transform: translateY(-1px);
}

/* Main cards */
.case-card {
    background: #1a1a2e;
    border: 1px solid #2a2a4a;
    border-radius: 14px;
    padding: 16px;
    margin: 8px 0;
    box-shadow: 0 0 14px rgba(0,0,0,0.22);
    transition: all 0.2s ease;
}

/* Hover effect */
.case-card:hover {
    transform: translateY(-2px);
    border-color: #3a3a5f;
}

/* Solved card */
.solved-card {
    background: #0d2b1e;
    border: 1px solid #1d9e75;
    border-radius: 14px;
    padding: 18px;
    margin: 8px 0;
    box-shadow: 0 0 14px rgba(0,0,0,0.22);
}

/* Revealed clue cards */
.clue-card-done {
    background: #0d2b1e;
    border-left: 4px solid #1d9e75;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    margin: 6px 0;
}

/* CSP propagation trace */
.prop-step {
    background: #12122a;
    border: 1px solid #2a2a4a;
    border-radius: 8px;
    padding: 8px 12px;
    margin: 4px 0;
    font-family: monospace;
    font-size: 13px;
    line-height: 1.7;
    color: #a0d4b8 !important;
}

/* Difficulty badges */
.badge-easy {
    background:#0d2b1e;
    color:#4ade80;
    padding:3px 10px;
    border-radius:4px;
    font-size:12px;
    font-weight:600;
}

.badge-medium {
    background:#2b1e0d;
    color:#fb923c;
    padding:3px 10px;
    border-radius:4px;
    font-size:12px;
    font-weight:600;
}

.badge-hard {
    background:#2b0d0d;
    color:#f87171;
    padding:3px 10px;
    border-radius:4px;
    font-size:12px;
    font-weight:600;
}

.badge-expert {
    background:#1e0d2b;
    color:#c084fc;
    padding:3px 10px;
    border-radius:4px;
    font-size:12px;
    font-weight:600;
}

/* Domain pills */
.domain-active {
    background: #1d3a2a;
    color: #4ade80;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    display: inline-block;
    margin: 3px;
    font-weight: 500;
}

.domain-elim {
    background: #1a1a2e;
    color: #6b7280;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
    display: inline-block;
    margin: 3px;
    text-decoration: line-through;
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(
        90deg,
        #e94560,
        #f59e0b
    ) !important;
}

/* Alerts */
.stSuccess {
    background: #0d2b1e !important;
    border: 1px solid #1d9e75 !important;
}

.stError {
    background: #2b0d0d !important;
    border: 1px solid #e94560 !important;
}

.stWarning {
    background: #2b1e0d !important;
    border: 1px solid #f59e0b !important;
}

.stInfo {
    background: #0d1f2b !important;
    border: 1px solid #378ADD !important;
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
        "wrong_attempts": 0
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────
def badge_html(difficulty):

    return f'<span class="badge-{difficulty.lower()}">{difficulty}</span>'

def domain_pills(active, all_items):

    html = ""

    for item in all_items:

        if item in active:
            html += f'<span class="domain-active">{item}</span>'
        else:
            html += f'<span class="domain-elim">{item}</span>'

    return html

def stars_from_clues(clues_used, total_clues):

    ratio = clues_used / total_clues

    if ratio <= 0.5:
        return 3
    elif ratio <= 0.75:
        return 2

    return 1

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

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:

    st.markdown("# 🕵️ Mystery Solver")

    st.markdown("*A CSP-Based Detective Game*")

    st.divider()

    st.markdown(f"### Score: `{st.session_state.score}`")

    st.markdown(
        f"### Cases Solved: `{len(st.session_state.completed_cases)}`"
    )

    st.divider()

    st.markdown("## Cases")

    for cid, case in CASES.items():

        solved = "✅" if cid in st.session_state.completed_cases else "🕵️"

        if st.button(
            f"{solved} Case {cid}",
            key=f"sidebar_{cid}"
        ):

            start_case(cid)
            st.rerun()

    if st.session_state.screen != "home":

        st.divider()

        if st.button("⬅ Back Home"):

            go_home()
            st.rerun()

# ─────────────────────────────────────────────────────────────
# HOME SCREEN
# ─────────────────────────────────────────────────────────────
if st.session_state.screen == "home":

    st.markdown("# 🕵️ Mystery Solver")

    st.markdown(
        "### Solve mysteries using CSP, AC-3, "
        "constraint propagation and logical deduction."
    )

    st.divider()

    # ───────────────── FUN CASES ─────────────────
    st.markdown("## 🍰 Introductory Cases")

    fun_cases = {
        k: v for k, v in CASES.items()
        if v["level"] == "fun"
    }

    fun_list = list(fun_cases.items())

    for row_start in range(0, len(fun_list), 2):

        cols = st.columns(2)

        row_cases = fun_list[row_start:row_start + 2]

        for col, (cid, case) in zip(cols, row_cases):

            with col:

                solved = cid in st.session_state.completed_cases

                status = "SOLVED" if solved else "NOT STARTED"

                st.markdown(f"""
<div class="case-card">

<h3>{case['emoji']} {case['title']}</h3>

<p style="color:#888; font-size:12px;">
{case['location']}
</p>

<p>
{case['description'][:120]}...
</p>

<p>
{badge_html(case['difficulty'])}
&nbsp;
<span style="font-size:12px;color:#888;">
{status}
</span>
</p>

<p style="font-size:12px;color:#666;">
{len(case['suspects'])} suspects
&nbsp;|&nbsp;
{len(case['locations'])} locations
&nbsp;|&nbsp;
{len(case['clues'])} clues
</p>

</div>
""", unsafe_allow_html=True)

                label = (
                    "Replay Case"
                    if solved
                    else "Start Case"
                )

                if st.button(label, key=f"fun_{cid}"):

                    start_case(cid)
                    st.rerun()

    st.divider()

    # ───────────────── SERIOUS CASES ─────────────────
    st.markdown("## 🏦 Investigation Cases")

    serious_cases = {
        k: v for k, v in CASES.items()
        if v["level"] == "serious"
    }

    serious_list = list(serious_cases.items())

    for row_start in range(0, len(serious_list), 3):

        cols = st.columns(3)

        row_cases = serious_list[row_start:row_start + 3]

        for col, (cid, case) in zip(cols, row_cases):

            with col:

                solved = cid in st.session_state.completed_cases

                status = "SOLVED" if solved else "NOT STARTED"

                st.markdown(f"""
<div class="case-card">

<h3>{case['emoji']} {case['title']}</h3>

<p style="color:#888; font-size:12px;">
{case['location']}
</p>

<p>
{case['description'][:110]}...
</p>

<p>
{badge_html(case['difficulty'])}
&nbsp;
<span style="font-size:12px;color:#888;">
{status}
</span>
</p>

<p style="font-size:12px;color:#666;">
{len(case['suspects'])} suspects
&nbsp;|&nbsp;
{len(case['locations'])} locations
&nbsp;|&nbsp;
{len(case['clues'])} clues
</p>

</div>
""", unsafe_allow_html=True)

                label = (
                    "Replay Case"
                    if solved
                    else "Start Case"
                )

                if st.button(label, key=f"serious_{cid}"):

                    start_case(cid)
                    st.rerun()

# ─────────────────────────────────────────────────────────────
# GAME SCREEN
# ─────────────────────────────────────────────────────────────
elif st.session_state.screen == "game":

    case = CASES[st.session_state.current_case_id]

    csp = st.session_state.csp

    total_clues = len(case["clues"])

    revealed = st.session_state.clues_revealed

    st.markdown(f"# {case['emoji']} {case['title']}")

    st.markdown(f"### {case['location']}")

    st.progress(revealed / total_clues)

    st.info(case["quote"])

    st.markdown(case["description"])

    st.divider()

    left_col, right_col = st.columns([1, 1])

    # ───────────────── LEFT ─────────────────
    with left_col:

        st.markdown("## Suspects")

        state = csp.get_current_state()

        for suspect in case["suspects"]:

            role = case["suspect_roles"][suspect]

            if suspect in state["suspect_domain"]:

                label_color = "#fbbf24"
                status = "ACTIVE"

            else:

                label_color = "#6b7280"
                status = "ELIMINATED"

            st.markdown(
                f'''
<div class="case-card"
style="border-left:4px solid {label_color};">

<span style="
color:{label_color};
font-weight:600;
font-size:16px;">
{suspect}
</span>

<br>

<span style="
color:#888;
font-size:12px;">
{role}
</span>

<span style="
float:right;
font-size:11px;
font-weight:600;
color:{label_color};">
{status}
</span>

</div>
''',
                unsafe_allow_html=True
            )

        st.markdown("## Locations")

        st.markdown(
            domain_pills(
                state["location_domain"],
                case["locations"]
            ),
            unsafe_allow_html=True
        )

        st.markdown("## Methods / Weapons")

        st.markdown(
            domain_pills(
                state["weapon_domain"],
                case["weapons"]
            ),
            unsafe_allow_html=True
        )

    # ───────────────── RIGHT ─────────────────
    with right_col:

        st.markdown("## Clues Revealed")

        for i in range(revealed):

            clue = case["clues"][i]

            st.markdown(
                f'''
<div class="clue-card-done">

<span style="
color:#1d9e75;
font-weight:600;">

Clue {clue["id"]}:

</span>

{clue["text"]}

</div>
''',
                unsafe_allow_html=True
            )

        if revealed < total_clues:

            if st.button(
                f"Reveal Clue {revealed + 1}",
                use_container_width=True
            ):

                clue = case["clues"][revealed]

                csp.apply_clue(clue)

                st.session_state.clues_revealed += 1

                st.rerun()

        else:

            st.success(
                "All clues revealed. "
                "Make your accusation below."
            )

        st.markdown("## CSP Propagation Trace")

        logs = csp.get_current_state()["propagation_log"]

        if not logs:

            st.info(
                "No propagation yet. "
                "Reveal the first clue."
            )

        for entry in logs:

            st.markdown(
                f'''
<div class="prop-step">

<b>[ Clue {entry["clue_id"]} ]</b>

<br><br>

{entry["propagation"]}

</div>
''',
                unsafe_allow_html=True
            )

    st.divider()

    # ───────────────── ACCUSATION ─────────────────
    st.markdown("## Make Your Accusation")

    if csp.get_current_state()["solved"]:

        st.info(
            "CSP has logically solved the case."
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        suspect_choice = st.selectbox(
            "Who is the culprit?",
            options=case["suspects"]
        )

    with col2:

        location_choice = st.selectbox(
            "Crime location?",
            options=case["locations"]
        )

    with col3:

        weapon_choice = st.selectbox(
            "Method used?",
            options=case["weapons"]
        )

    st.warning(
        "Wrong accusation means retrying."
    )

    if st.button(
        "Submit Accusation",
        use_container_width=True
    ):

        correct = csp.verify_accusation(
            suspect_choice,
            location_choice,
            weapon_choice
        )

        if correct:

            stars = stars_from_clues(
                revealed,
                total_clues
            )

            points = stars * 100

            st.session_state.score += points

            if (
                st.session_state.current_case_id
                not in st.session_state.completed_cases
            ):

                st.session_state.completed_cases.append(
                    st.session_state.current_case_id
                )

            st.session_state.case_stars[
                st.session_state.current_case_id
            ] = stars

            st.session_state.screen = "verdict"

            st.rerun()

        else:

            st.session_state.wrong_attempts += 1

            st.error(
                f"Incorrect accusation. "
                f"Wrong attempts: "
                f"{st.session_state.wrong_attempts}"
            )

# ─────────────────────────────────────────────────────────────
# VERDICT SCREEN
# ─────────────────────────────────────────────────────────────
elif st.session_state.screen == "verdict":

    case = CASES[st.session_state.current_case_id]

    csp = st.session_state.csp

    solution = case["solution"]

    stars = st.session_state.case_stars.get(
        st.session_state.current_case_id,
        1
    )

    st.markdown(
        f"# ✅ Case Closed — {case['title']}"
    )

    st.divider()

    st.markdown(f"""
<div class="solved-card">

<h2 style="color:#4ade80;">

Correct Accusation

</h2>

<br>

<p>
<b>Culprit:</b>
{solution['culprit']}
</p>

<p>
<b>Location:</b>
{solution['location']}
</p>

<p>
<b>Method:</b>
{solution['weapon']}
</p>

<p>
<b>Stars Earned:</b>
{'⭐' * stars}
</p>

</div>
""", unsafe_allow_html=True)

    st.divider()

    st.markdown("## Full CSP Reasoning Trace")

    logs = csp.get_current_state()["propagation_log"]

    for entry in logs:

        st.markdown(f"""
<div class="prop-step">

<b>[ Clue {entry['clue_id']} ]</b>

<br><br>

{entry['clue_text']}

<br><br>

<b>Propagation:</b>

<br>

{entry['propagation']}

</div>
""", unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "⬅ Back Home",
            use_container_width=True
        ):

            go_home()
            st.rerun()

    with col2:

        if st.button(
            "🔄 Replay Case",
            use_container_width=True
        ):

            start_case(
                st.session_state.current_case_id
            )

            st.rerun()
