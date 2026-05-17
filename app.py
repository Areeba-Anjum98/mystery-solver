import streamlit as st
from cases import CASES
from csp_engine import CSPEngine

# ─────────────────────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mystery Solver",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Main background */
.stApp { background-color: #0f0f1a; }

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #16213e;
    border-right: 1px solid #2a2a4a;
}

/* All text color */
.stApp, .stMarkdown, p, span, label { color: #e0dff0 !important; }

/* Headings */
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
    transition: background 0.2s;
}
.stButton > button:hover {
    background-color: #c73652;
    color: white !important;
}

/* Cards / info boxes */
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
.clue-card {
    background: #1e1e35;
    border-left: 3px solid #e94560;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    margin: 6px 0;
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
.prop-step-active {
    background: #1e1e08;
    border: 1px solid #8a7a20;
    border-radius: 8px;
    padding: 8px 12px;
    margin: 4px 0;
    font-family: monospace;
    font-size: 13px;
    color: #d4c45a !important;
}
.badge-easy   { background:#0d2b1e; color:#4ade80; padding:3px 10px; border-radius:99px; font-size:12px; font-weight:600; }
.badge-medium { background:#2b1e0d; color:#fb923c; padding:3px 10px; border-radius:99px; font-size:12px; font-weight:600; }
.badge-hard   { background:#2b0d0d; color:#f87171; padding:3px 10px; border-radius:99px; font-size:12px; font-weight:600; }
.badge-expert { background:#1e0d2b; color:#c084fc; padding:3px 10px; border-radius:99px; font-size:12px; font-weight:600; }

/* Domain pills */
.domain-active { background:#1d3a2a; color:#4ade80; padding:3px 10px; border-radius:99px; font-size:12px; display:inline-block; margin:2px; }
.domain-elim   { background:#1a1a2e; color:#555577; padding:3px 10px; border-radius:99px; font-size:12px; display:inline-block; margin:2px; text-decoration:line-through; }

/* Selectbox */
.stSelectbox label { color: #e0dff0 !important; }

/* Progress bar */
.stProgress > div > div { background-color: #e94560 !important; }

/* Success / error messages */
.stSuccess { background: #0d2b1e !important; border: 1px solid #1d9e75 !important; }
.stError   { background: #2b0d0d !important; border: 1px solid #e94560 !important; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
#  SESSION STATE INITIALISATION
# ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "screen":          "home",       # home | game | verdict
        "current_case_id": None,
        "csp":             None,         # CSPEngine instance
        "clues_revealed":  0,
        "score":           0,
        "completed_cases": [],           # list of completed case ids
        "case_stars":      {},           # {case_id: stars}
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
def stars_from_clues(clues_used: int, total_clues: int) -> int:
    ratio = clues_used / total_clues
    if ratio <= 0.5:
        return 3
    elif ratio <= 0.75:
        return 2
    return 1

def badge_html(difficulty: str) -> str:
    d = difficulty.lower()
    return f'<span class="badge-{d}">{difficulty}</span>'

def domain_pills(items: list, all_items: list) -> str:
    html = ""
    for item in all_items:
        if item in items:
            html += f'<span class="domain-active">✓ {item}</span>'
        else:
            html += f'<span class="domain-elim">{item}</span>'
    return html

def start_case(case_id: int):
    case = CASES[case_id]
    st.session_state.current_case_id = case_id
    st.session_state.csp              = CSPEngine(case)
    st.session_state.clues_revealed   = 0
    st.session_state.wrong_attempts   = 0
    st.session_state.verdict_correct  = None
    st.session_state.screen           = "game"

def go_home():
    st.session_state.screen          = "home"
    st.session_state.current_case_id = None
    st.session_state.csp             = None


# ─────────────────────────────────────────────────────────────
#  SIDEBAR — always visible
# ─────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Mystery Solver")
    st.markdown("*A CSP Detective Game*")
    st.divider()

    # Score
    st.markdown(f"### 🏆 Total Score: `{st.session_state.score}`")
    st.markdown(f"### ✅ Cases Solved: `{len(st.session_state.completed_cases)}`")
    st.divider()

    # Case list in sidebar
    st.markdown("### 📋 All Cases")
    for cid, case in CASES.items():
        stars = st.session_state.case_stars.get(cid, "")
        star_str = "⭐" * stars if stars else ""
        done = "✅" if cid in st.session_state.completed_cases else "🔵"
        label = f"{done} {case['emoji']} {case['title']} {star_str}"
        if st.button(label, key=f"sb_{cid}"):
            start_case(cid)
            st.rerun()

    st.divider()

    # AI Concepts info
    with st.expander("🧠 AI Concepts Used"):
        st.markdown("""
**CSP (Constraint Satisfaction)**
- Variables: Suspect, Location, Weapon
- Domains: All possible values
- Constraints: Each clue removes values

**Constraint Propagation**
- Each clue triggers elimination
- Chain reaction across domains

**Arc Consistency (AC-3)**
- Ensures consistency between variables
- Reduces domains automatically

**Backtracking**
- Used when red herrings appear
- Explores alternatives if stuck

**Logical Agents**
- Knowledge base updates per clue
- IF-THEN deduction rules
        """)

    if st.session_state.screen != "home":
        st.divider()
        if st.button("🏠 Back to Home"):
            go_home()
            st.rerun()


# ─────────────────────────────────────────────────────────────
#  SCREEN 1 — HOME
# ─────────────────────────────────────────────────────────────
if st.session_state.screen == "home":

    st.markdown("# 🔍 Mystery Solver")
    st.markdown("### Use clues and logic to find the culprit. Each clue eliminates suspects using CSP.")
    st.divider()

    # Fun cases
    st.markdown("## 🎉 Fun Cases — Warm Up")
    fun_cols = st.columns(2)
    fun_cases = {k: v for k, v in CASES.items() if v["level"] == "fun"}
    for i, (cid, case) in enumerate(fun_cases.items()):
        with fun_cols[i % 2]:
            stars = st.session_state.case_stars.get(cid, 0)
            star_str = "⭐" * stars if stars else ""
            done_badge = "✅ Solved" if cid in st.session_state.completed_cases else "🔵 Not started"
            st.markdown(f"""
<div class="case-card">
    <h3>{case['emoji']} {case['title']}</h3>
    <p style="color:#aaa;">{case['location']}</p>
    <p>{case['description'][:120]}...</p>
    <p>{badge_html(case['difficulty'])} &nbsp; {done_badge} {star_str}</p>
    <p style="color:#888; font-size:12px;">
        👤 {len(case['suspects'])} suspects &nbsp;|&nbsp;
        📍 {len(case['locations'])} locations &nbsp;|&nbsp;
        🔎 {len(case['clues'])} clues
    </p>
</div>
""", unsafe_allow_html=True)
            if st.button(f"{'🔄 Replay' if cid in st.session_state.completed_cases else '▶ Start'} — {case['title']}", key=f"start_{cid}"):
                start_case(cid)
                st.rerun()

    st.divider()

    # Serious cases
    st.markdown("## 🕵️ Serious Cases — Real Mysteries")
    serious_cases = {k: v for k, v in CASES.items() if v["level"] == "serious"}
    cols = st.columns(3)
    for i, (cid, case) in enumerate(serious_cases.items()):
        with cols[i % 3]:
            stars = st.session_state.case_stars.get(cid, 0)
            star_str = "⭐" * stars if stars else ""
            done_badge = "✅ Solved" if cid in st.session_state.completed_cases else "🔵 Not started"
            st.markdown(f"""
<div class="case-card">
    <h3>{case['emoji']} {case['title']}</h3>
    <p style="color:#aaa;">{case['location']}</p>
    <p>{case['description'][:110]}...</p>
    <p>{badge_html(case['difficulty'])} &nbsp; {done_badge} {star_str}</p>
    <p style="color:#888; font-size:12px;">
        👤 {len(case['suspects'])} suspects &nbsp;|&nbsp;
        📍 {len(case['locations'])} locations &nbsp;|&nbsp;
        🔎 {len(case['clues'])} clues
    </p>
</div>
""", unsafe_allow_html=True)
            if st.button(f"{'🔄 Replay' if cid in st.session_state.completed_cases else '▶ Start'} — {case['title']}", key=f"start_{cid}"):
                start_case(cid)
                st.rerun()


# ─────────────────────────────────────────────────────────────
#  SCREEN 2 — GAME
# ─────────────────────────────────────────────────────────────
elif st.session_state.screen == "game":

    case       = CASES[st.session_state.current_case_id]
    csp        = st.session_state.csp
    total_clues = len(case["clues"])
    revealed   = st.session_state.clues_revealed

    # ── Top bar ──────────────────────────────────────────────
    col_title, col_meta = st.columns([2, 1])
    with col_title:
        st.markdown(f"# {case['emoji']} {case['title']}")
        st.markdown(f"📍 *{case['location']}*")
    with col_meta:
        st.markdown(f"**Clues used:** {revealed} / {total_clues}")
        st.progress(revealed / total_clues if total_clues else 0)
        st.markdown(f"**Score:** 🏆 {st.session_state.score}")

    st.divider()

    # ── Story ─────────────────────────────────────────────────
    with st.expander("📖 Case Description", expanded=True):
        st.markdown(f"*{case['description']}*")
        st.info(f"💬 \"{case['quote']}\"")

    st.divider()

    # ── Main game layout ─────────────────────────────────────
    left_col, right_col = st.columns([1, 1])

    # LEFT — Suspects + Domains
    with left_col:
        st.markdown("### 👤 Suspects")
        state = csp.get_current_state()
        for suspect in case["suspects"]:
            role = case["suspect_roles"][suspect]
            if suspect in state["suspect_domain"]:
                icon = "🟡"
                color = "#d4af37"
            else:
                icon = "❌"
                color = "#555"
            st.markdown(
                f'<div style="background:#1a1a2e; border-radius:8px; '
                f'padding:8px 12px; margin:4px 0; border-left: 3px solid {color};">'
                f'{icon} <b style="color:{color};">{suspect}</b> '
                f'<span style="color:#888; font-size:12px;">— {role}</span></div>',
                unsafe_allow_html=True
            )

        st.markdown("### 📍 Locations")
        st.markdown(
            domain_pills(state["location_domain"], case["locations"]),
            unsafe_allow_html=True
        )

        st.markdown("### 🔧 Weapons / Methods")
        st.markdown(
            domain_pills(state["weapon_domain"], case["weapons"]),
            unsafe_allow_html=True
        )

    # RIGHT — Clues + Propagation
    with right_col:
        st.markdown("### 🔍 Clues Revealed")

        # Show already revealed clues
        for i in range(revealed):
            clue = case["clues"][i]
            st.markdown(
                f'<div class="clue-card-done">✅ <b>Clue {clue["id"]}:</b> {clue["text"]}</div>',
                unsafe_allow_html=True
            )

        # Reveal next clue button
        if revealed < total_clues:
            if st.button(f"👁 Reveal Clue {revealed + 1}", use_container_width=True):
                clue = case["clues"][revealed]
                csp.apply_clue(clue)
                st.session_state.clues_revealed += 1
                st.rerun()
        else:
            st.success("All clues revealed! Make your accusation below.")

        # CSP Propagation Trace
        st.markdown("### 🧠 CSP Propagation Trace")
        log = csp.get_current_state()["propagation_log"]
        if not log:
            st.markdown(
                '<div class="prop-step" style="color:#555 !important;">No clues applied yet...</div>',
                unsafe_allow_html=True
            )
        for entry in log:
            st.markdown(
                f'<div class="prop-step">⚙ Clue {entry["clue_id"]}: {entry["propagation"]}</div>',
                unsafe_allow_html=True
            )

    st.divider()

    # ── Accusation Section ────────────────────────────────────
    st.markdown("### ⚖️ Make Your Accusation")

    if csp.get_current_state()["solved"]:
        st.info("🔎 CSP has solved the case logically. Confirm your accusation below.")

    acc_col1, acc_col2, acc_col3 = st.columns(3)

    with acc_col1:
        suspect_choice = st.selectbox(
            "Who is the culprit?",
            options=case["suspects"],
            index=0
        )
    with acc_col2:
        location_choice = st.selectbox(
            "Where did it happen?",
            options=case["locations"],
            index=0
        )
    with acc_col3:
        weapon_choice = st.selectbox(
            "What method was used?",
            options=case["weapons"],
            index=0
        )

    st.warning("⚠️ A wrong accusation will reset your clue progress for this case!")

    if st.button("🔨 Submit Accusation", use_container_width=True):
        correct = csp.verify_accusation(suspect_choice, location_choice, weapon_choice)
        if correct:
            # Calculate stars and score
            stars  = stars_from_clues(revealed, total_clues)
            points = stars * 100 + max(0, (total_clues - revealed) * 20)
            st.session_state.score += points
            st.session_state.case_stars[st.session_state.current_case_id] = stars
            if st.session_state.current_case_id not in st.session_state.completed_cases:
                st.session_state.completed_cases.append(st.session_state.current_case_id)
            st.session_state.verdict_correct = True
            st.session_state.screen = "verdict"
            st.rerun()
        else:
            st.session_state.wrong_attempts += 1
            st.error(
                f"❌ Wrong accusation! That is not correct. "
                f"({st.session_state.wrong_attempts} wrong attempt(s)). "
                f"Reveal more clues and try again."
            )


# ─────────────────────────────────────────────────────────────
#  SCREEN 3 — VERDICT
# ─────────────────────────────────────────────────────────────
elif st.session_state.screen == "verdict":

    case    = CASES[st.session_state.current_case_id]
    csp     = st.session_state.csp
    stars   = st.session_state.case_stars.get(st.session_state.current_case_id, 1)
    solution = case["solution"]

    st.markdown(f"# 🎉 Case Solved — {case['emoji']} {case['title']}")
    st.markdown("---")

    # Verdict card
    st.markdown(f"""
<div class="solved-card">
    <h2 style="color:#4ade80;">✅ You solved the case correctly!</h2>
    <br>
    <table width="100%">
        <tr>
            <td style="color:#888; padding:6px 0;">🕵️ Culprit</td>
            <td style="color:#fff; font-weight:bold;">{solution['culprit']}</td>
        </tr>
        <tr>
            <td style="color:#888; padding:6px 0;">📍 Location</td>
            <td style="color:#fff; font-weight:bold;">{solution['location']}</td>
        </tr>
        <tr>
            <td style="color:#888; padding:6px 0;">🔧 Method</td>
            <td style="color:#fff; font-weight:bold;">{solution['weapon']}</td>
        </tr>
        <tr>
            <td style="color:#888; padding:6px 0;">🔎 Clues Used</td>
            <td style="color:#fff; font-weight:bold;">{st.session_state.clues_revealed} / {len(case['clues'])}</td>
        </tr>
        <tr>
            <td style="color:#888; padding:6px 0;">⚙️ CSP Steps</td>
            <td style="color:#fff; font-weight:bold;">{len(csp.get_current_state()['propagation_log'])} propagations</td>
        </tr>
        <tr>
            <td style="color:#888; padding:6px 0;">🏆 Points Earned</td>
            <td style="color:#fbbf24; font-weight:bold;">{stars * 100 + max(0, (len(case['clues']) - st.session_state.clues_revealed) * 20)} pts</td>
        </tr>
    </table>
    <br>
    <h2>{"⭐" * stars} {"★" * (3 - stars)}</h2>
</div>
""", unsafe_allow_html=True)

    # Full propagation trace on verdict screen
    st.markdown("### 🧠 Full CSP Reasoning Trace")
    for entry in csp.get_current_state()["propagation_log"]:
        eliminated = []
        if entry["changed"]["suspects"]:
            eliminated.append(f"Suspects removed: {', '.join(entry['changed']['suspects'])}")
        if entry["changed"]["locations"]:
            eliminated.append(f"Locations removed: {', '.join(entry['changed']['locations'])}")
        if entry["changed"]["weapons"]:
            eliminated.append(f"Weapons removed: {', '.join(entry['changed']['weapons'])}")
        elim_text = " | ".join(eliminated) if eliminated else "No direct eliminations — contextual reasoning"
        st.markdown(f"""
<div class="prop-step">
    <b>Clue {entry['clue_id']}:</b> {entry['clue_text']}<br>
    <span style="color:#fbbf24;">↳ {entry['propagation']}</span><br>
    <span style="color:#60a5fa;">↳ {elim_text}</span>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # Navigation buttons
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        if st.button("🏠 Home", use_container_width=True):
            go_home()
            st.rerun()
    with btn_col2:
        if st.button("🔄 Replay This Case", use_container_width=True):
            start_case(st.session_state.current_case_id)
            st.rerun()
    with btn_col3:
        # Find next unsolved case
        next_case = None
        for cid in CASES:
            if cid not in st.session_state.completed_cases:
                next_case = cid
                break
        if next_case:
            if st.button(f"▶ Next: {CASES[next_case]['title']}", use_container_width=True):
                start_case(next_case)
                st.rerun()
        else:
            st.success("🎊 All cases solved! You are the ultimate detective!")
