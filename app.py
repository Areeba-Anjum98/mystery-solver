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
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0f172a;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #111827;
}

/* Text */
html, body, [class*="css"] {
    color: #f3f4f6;
}

/* Buttons */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    background: #dc2626;
    color: white;
    border: none;
    padding: 0.6rem;
    font-weight: 600;
}

.stButton > button:hover {
    background: #b91c1c;
    color: white;
}

/* Cards */
.case-card {
    background: #1e293b;
    border: 1px solid #334155;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 15px;
}

/* Solved Card */
.solved-card {
    background: #052e16;
    border: 1px solid #22c55e;
    border-radius: 14px;
    padding: 20px;
}

/* Clues */
.clue-card {
    background: #1e293b;
    border-left: 4px solid #dc2626;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 10px;
}

/* Propagation */
.prop-step {
    background: #111827;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 10px;
    margin-bottom: 8px;
    font-size: 13px;
}

/* Domain pills */
.domain-active {
    background: #14532d;
    color: #86efac;
    padding: 4px 10px;
    border-radius: 999px;
    display: inline-block;
    margin: 4px;
    font-size: 12px;
}

.domain-elim {
    background: #1e293b;
    color: #64748b;
    text-decoration: line-through;
    padding: 4px 10px;
    border-radius: 999px;
    display: inline-block;
    margin: 4px;
    font-size: 12px;
}

/* Difficulty badges */
.badge-easy {
    background: #14532d;
    color: #86efac;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
}

.badge-medium {
    background: #78350f;
    color: #fdba74;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
}

.badge-hard {
    background: #7f1d1d;
    color: #fca5a5;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
}

.badge-expert {
    background: #581c87;
    color: #d8b4fe;
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 12px;
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

    mapping = {
        "Easy": "badge-easy",
        "Medium": "badge-medium",
        "Hard": "badge-hard",
        "Expert": "badge-expert"
    }

    return f'<span class="{mapping[difficulty]}">{difficulty}</span>'

def domain_pills(active, all_items):

    html = ""

    for item in all_items:

        if item in active:
            html += f'<span class="domain-active">{item}</span>'
        else:
            html += f'<span class="domain-elim">{item}</span>'

    return html

def start_case(case_id):

    st.session_state.current_case_id = case_id
    st.session_state.csp = CSPEngine(CASES[case_id])
    st.session_state.clues_revealed = 0
    st.session_state.wrong_attempts = 0
    st.session_state.screen = "game"

def go_home():

    st.session_state.screen = "home"
    st.session_state.current_case_id = None
    st.session_state.csp = None

def stars_from_clues(clues_used, total):

    ratio = clues_used / total

    if ratio <= 0.5:
        return 3
    elif ratio <= 0.75:
        return 2

    return 1

# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
with st.sidebar:

    st.title("🕵️ Mystery Solver")

    st.markdown(f"### Score: `{st.session_state.score}`")
    st.markdown(f"### Solved Cases: `{len(st.session_state.completed_cases)}`")

    st.divider()

    st.subheader("All Cases")

    for cid, case in CASES.items():

        solved = "✅" if cid in st.session_state.completed_cases else "🕵️"

        if st.button(f"{solved} Case {cid}"):
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

    st.title("🕵️ Mystery Solver")
    st.markdown("### Solve mysteries using CSP, AC-3 and logical deduction.")

    st.divider()

    # FUN CASES
    st.header("🍰 Introductory Cases")

    fun_cases = {k: v for k, v in CASES.items() if v["level"] == "fun"}

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

<p style="color:#94a3b8;">
{case['location']}
</p>

<p>
{case['description'][:140]}...
</p>

<p>
{badge_html(case['difficulty'])}
&nbsp;
<span style="color:#94a3b8;">{status}</span>
</p>

<p style="font-size:12px;color:#64748b;">
{len(case['suspects'])} suspects |
{len(case['locations'])} locations |
{len(case['clues'])} clues
</p>

</div>
""", unsafe_allow_html=True)

                btn = "Replay Case" if solved else "Start Case"

                if st.button(btn, key=f"fun_{cid}"):
                    start_case(cid)
                    st.rerun()

    st.divider()

    # SERIOUS CASES
    st.header("🏦 Investigation Cases")

    serious_cases = {k: v for k, v in CASES.items() if v["level"] == "serious"}

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

<p style="color:#94a3b8;">
{case['location']}
</p>

<p>
{case['description'][:120]}...
</p>

<p>
{badge_html(case['difficulty'])}
&nbsp;
<span style="color:#94a3b8;">{status}</span>
</p>

<p style="font-size:12px;color:#64748b;">
{len(case['suspects'])} suspects |
{len(case['locations'])} locations |
{len(case['clues'])} clues
</p>

</div>
""", unsafe_allow_html=True)

                btn = "Replay Case" if solved else "Start Case"

                if st.button(btn, key=f"serious_{cid}"):
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

    st.title(f"{case['emoji']} {case['title']}")

    st.markdown(f"### {case['location']}")

    st.progress(revealed / total_clues)

    st.info(case["quote"])

    st.markdown(case["description"])

    st.divider()

    left, right = st.columns([1, 1])

    # LEFT
    with left:

        st.subheader("Suspects")

        state = csp.get_current_state()

        for suspect in case["suspects"]:

            role = case["suspect_roles"][suspect]

            if suspect in state["suspect_domain"]:
                color = "#22c55e"
                status = "ACTIVE"
            else:
                color = "#64748b"
                status = "ELIMINATED"

            st.markdown(f"""
<div class="case-card" style="border-left:4px solid {color};">
<b>{suspect}</b><br>
<span style="color:#94a3b8;">{role}</span><br>
<span style="color:{color};font-size:12px;">{status}</span>
</div>
""", unsafe_allow_html=True)

        st.subheader("Locations")

        st.markdown(
            domain_pills(
                state["location_domain"],
                case["locations"]
            ),
            unsafe_allow_html=True
        )

        st.subheader("Weapons / Methods")

        st.markdown(
            domain_pills(
                state["weapon_domain"],
                case["weapons"]
            ),
            unsafe_allow_html=True
        )

    # RIGHT
    with right:

        st.subheader("Clues")

        for i in range(revealed):

            clue = case["clues"][i]

            st.markdown(f"""
<div class="clue-card">
<b>Clue {clue['id']}:</b><br>
{clue['text']}
</div>
""", unsafe_allow_html=True)

        if revealed < total_clues:

            if st.button(f"Reveal Clue {revealed + 1}"):

                clue = case["clues"][revealed]

                csp.apply_clue(clue)

                st.session_state.clues_revealed += 1

                st.rerun()

        else:
            st.success("All clues revealed.")

        st.subheader("CSP Propagation")

        logs = csp.get_current_state()["propagation_log"]

        if not logs:

            st.info("No propagation yet.")

        for entry in logs:

            st.markdown(f"""
<div class="prop-step">
<b>Clue {entry['clue_id']}</b><br>
{entry['propagation']}
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ACCUSATION
    st.subheader("Make Your Accusation")

    col1, col2, col3 = st.columns(3)

    with col1:
        suspect_choice = st.selectbox(
            "Culprit",
            case["suspects"]
        )

    with col2:
        location_choice = st.selectbox(
            "Location",
            case["locations"]
        )

    with col3:
        weapon_choice = st.selectbox(
            "Method",
            case["weapons"]
        )

    st.warning("Wrong accusation means retrying the case.")

    if st.button("Submit Accusation"):

        correct = csp.verify_accusation(
            suspect_choice,
            location_choice,
            weapon_choice
        )

        if correct:

            stars = stars_from_clues(revealed, total_clues)

            points = stars * 100

            st.session_state.score += points

            if st.session_state.current_case_id not in st.session_state.completed_cases:

                st.session_state.completed_cases.append(
                    st.session_state.current_case_id
                )

            st.session_state.case_stars[
                st.session_state.current_case_id
            ] = stars

            st.session_state.screen = "verdict"

            st.rerun()

        else:

            st.error("Incorrect accusation.")

# ─────────────────────────────────────────────────────────────
# VERDICT SCREEN
# ─────────────────────────────────────────────────────────────
elif st.session_state.screen == "verdict":

    case = CASES[st.session_state.current_case_id]

    solution = case["solution"]

    stars = st.session_state.case_stars.get(
        st.session_state.current_case_id,
        1
    )

    st.title("✅ CASE SOLVED")

    st.markdown(f"""
<div class="solved-card">

<h2>{case['title']}</h2>

<p><b>Culprit:</b> {solution['culprit']}</p>

<p><b>Location:</b> {solution['location']}</p>

<p><b>Method:</b> {solution['weapon']}</p>

<p><b>Stars:</b> {'⭐' * stars}</p>

</div>
""", unsafe_allow_html=True)

    st.divider()

    st.subheader("Reasoning Trace")

    logs = st.session_state.csp.get_current_state()["propagation_log"]

    for entry in logs:

        st.markdown(f"""
<div class="prop-step">
<b>Clue {entry['clue_id']}</b><br>
{entry['clue_text']}<br><br>

<b>Propagation:</b><br>
{entry['propagation']}
</div>
""", unsafe_allow_html=True)

    st.divider()

    c1, c2 = st.columns(2)

    with c1:

        if st.button("🏠 Home"):
            go_home()
            st.rerun()

    with c2:

        if st.button("🔄 Replay"):
            start_case(st.session_state.current_case_id)
            st.rerun()
