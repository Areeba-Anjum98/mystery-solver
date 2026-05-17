# # import streamlit as st
# # from cases import CASES
# # from csp_engine import CSPEngine

# # # ─────────────────────────────────────────────────────────────
# # #  PAGE CONFIG
# # # ─────────────────────────────────────────────────────────────
# # st.set_page_config(
# #     page_title="Mystery Solver",
# #     page_icon="M",
# #     layout="wide",
# #     initial_sidebar_state="expanded"
# # )

# # # ─────────────────────────────────────────────────────────────
# # #  CUSTOM CSS
# # # ─────────────────────────────────────────────────────────────
# # st.markdown("""
# # <style>
# # /* Main background */
# # .stApp { background-color: #0f0f1a; }

# # /* Sidebar */
# # [data-testid="stSidebar"] {
# #     background-color: #16213e;
# #     border-right: 1px solid #2a2a4a;
# # }

# # /* All text */
# # .stApp, .stMarkdown, p, span, label { color: #e0dff0 !important; }

# # /* Headings */
# # h1, h2, h3 { color: #ffffff !important; }

# # /* Buttons */
# # .stButton > button {
# #     background-color: #e94560;
# #     color: white !important;
# #     border: none;
# #     border-radius: 8px;
# #     padding: 10px 20px;
# #     font-weight: 600;
# #     width: 100%;
# #     letter-spacing: 0.02em;
# #     transition: background 0.2s;
# # }
# # .stButton > button:hover {
# #     background-color: #c73652;
# #     color: white !important;
# # }

# # /* Cards */
# # .case-card {
# #     background: #1a1a2e;
# #     border: 1px solid #2a2a4a;
# #     border-radius: 12px;
# #     padding: 16px;
# #     margin: 8px 0;
# # }
# # .solved-card {
# #     background: #0d2b1e;
# #     border: 1px solid #1d9e75;
# #     border-radius: 12px;
# #     padding: 16px;
# #     margin: 8px 0;
# # }
# # .clue-card-done {
# #     background: #0d2b1e;
# #     border-left: 3px solid #1d9e75;
# #     border-radius: 0 10px 10px 0;
# #     padding: 12px 16px;
# #     margin: 6px 0;
# # }
# # .prop-step {
# #     background: #12122a;
# #     border: 1px solid #2a2a4a;
# #     border-radius: 8px;
# #     padding: 8px 12px;
# #     margin: 4px 0;
# #     font-family: monospace;
# #     font-size: 13px;
# #     color: #a0d4b8 !important;
# #     line-height: 1.6;
# # }

# # /* Difficulty badges */
# # .badge-easy   { background:#0d2b1e; color:#4ade80; padding:3px 10px; border-radius:4px; font-size:12px; font-weight:600; }
# # .badge-medium { background:#2b1e0d; color:#fb923c; padding:3px 10px; border-radius:4px; font-size:12px; font-weight:600; }
# # .badge-hard   { background:#2b0d0d; color:#f87171; padding:3px 10px; border-radius:4px; font-size:12px; font-weight:600; }
# # .badge-expert { background:#1e0d2b; color:#c084fc; padding:3px 10px; border-radius:4px; font-size:12px; font-weight:600; }

# # /* Domain pills */
# # .domain-active {
# #     background: #1d3a2a;
# #     color: #4ade80;
# #     padding: 3px 10px;
# #     border-radius: 4px;
# #     font-size: 12px;
# #     display: inline-block;
# #     margin: 2px;
# #     font-weight: 500;
# # }
# # .domain-elim {
# #     background: #1a1a2e;
# #     color: #555577;
# #     padding: 3px 10px;
# #     border-radius: 4px;
# #     font-size: 12px;
# #     display: inline-block;
# #     margin: 2px;
# #     text-decoration: line-through;
# # }

# # /* Selectbox label */
# # .stSelectbox label { color: #e0dff0 !important; }

# # /* Progress bar */
# # .stProgress > div > div { background-color: #e94560 !important; }

# # /* Alerts */
# # .stSuccess { background: #0d2b1e !important; border: 1px solid #1d9e75 !important; }
# # .stError   { background: #2b0d0d !important; border: 1px solid #e94560 !important; }
# # .stWarning { background: #2b1e0d !important; border: 1px solid #f59e0b !important; }
# # .stInfo    { background: #0d1f2b !important; border: 1px solid #378ADD !important; }
# # </style>
# # """, unsafe_allow_html=True)


# # # ─────────────────────────────────────────────────────────────
# # #  SESSION STATE INITIALISATION
# # # ─────────────────────────────────────────────────────────────
# # def init_state():
# #     defaults = {
# #         "screen":          "home",
# #         "current_case_id": None,
# #         "csp":             None,
# #         "clues_revealed":  0,
# #         "score":           0,
# #         "completed_cases": [],
# #         "case_stars":      {},
# #         "wrong_attempts":  0,
# #         "verdict_correct": None,
# #     }
# #     for key, val in defaults.items():
# #         if key not in st.session_state:
# #             st.session_state[key] = val

# # init_state()


# # # ─────────────────────────────────────────────────────────────
# # #  HELPER FUNCTIONS
# # # ─────────────────────────────────────────────────────────────
# # def stars_from_clues(clues_used: int, total_clues: int) -> int:
# #     ratio = clues_used / total_clues
# #     if ratio <= 0.5:
# #         return 3
# #     elif ratio <= 0.75:
# #         return 2
# #     return 1

# # def badge_html(difficulty: str) -> str:
# #     return f'<span class="badge-{difficulty.lower()}">{difficulty}</span>'

# # def domain_pills(active: list, all_items: list) -> str:
# #     html = ""
# #     for item in all_items:
# #         if item in active:
# #             html += f'<span class="domain-active">[+] {item}</span>'
# #         else:
# #             html += f'<span class="domain-elim">{item}</span>'
# #     return html

# # def star_display(count: int) -> str:
# #     # HTML star entities — no emoji needed
# #     filled = "&#9733;" * count
# #     empty  = "&#9734;" * (3 - count)
# #     return (
# #         f'<span style="color:#f59e0b; font-size:22px;">{filled}</span>'
# #         f'<span style="color:#444; font-size:22px;">{empty}</span>'
# #     )

# # def start_case(case_id: int):
# #     case = CASES[case_id]
# #     st.session_state.current_case_id = case_id
# #     st.session_state.csp             = CSPEngine(case)
# #     st.session_state.clues_revealed  = 0
# #     st.session_state.wrong_attempts  = 0
# #     st.session_state.verdict_correct = None
# #     st.session_state.screen          = "game"

# # def go_home():
# #     st.session_state.screen          = "home"
# #     st.session_state.current_case_id = None
# #     st.session_state.csp             = None


# # # ─────────────────────────────────────────────────────────────
# # #  SIDEBAR
# # # ─────────────────────────────────────────────────────────────
# # with st.sidebar:
# #     st.markdown("## Mystery Solver")
# #     st.markdown("*A CSP-Based Detective Game*")
# #     st.divider()

# #     st.markdown(f"**Total Score:** `{st.session_state.score}`")
# #     st.markdown(f"**Cases Solved:** `{len(st.session_state.completed_cases)}`")
# #     st.divider()

# #     st.markdown("### All Cases")
# #     for cid, case in CASES.items():
# #         stars    = st.session_state.case_stars.get(cid, 0)
# #         star_str = " [" + ("*" * stars) + "]" if stars else ""
# #         status   = "[Solved]" if cid in st.session_state.completed_cases else "[Open]"
# #         label    = f"{status} Case {cid} — {case['title']}{star_str}"
# #         if st.button(label, key=f"sb_{cid}"):
# #             start_case(cid)
# #             st.rerun()

# #     st.divider()

# #     with st.expander("AI Concepts Used"):
# #         st.markdown("""
# # **CSP (Constraint Satisfaction)**
# # - Variables: Suspect, Location, Weapon
# # - Domains: All possible values at start
# # - Constraints: Each clue removes values

# # **Constraint Propagation**
# # - Each clue triggers elimination
# # - Chain reaction across all domains

# # **Arc Consistency (AC-3)**
# # - Ensures consistency between variables
# # - Reduces domains automatically

# # **Backtracking**
# # - Used when red herrings appear
# # - Explores alternatives if stuck

# # **Logical Agents**
# # - Knowledge base updates per clue
# # - IF-THEN deduction rules applied
# #         """)

# #     if st.session_state.screen != "home":
# #         st.divider()
# #         if st.button("Back to Home"):
# #             go_home()
# #             st.rerun()


# # # ─────────────────────────────────────────────────────────────
# # #  SCREEN 1 — HOME
# # # ─────────────────────────────────────────────────────────────
# # if st.session_state.screen == "home":

# #     st.markdown("# Mystery Solver")
# #     st.markdown("### Use clues and logic to find the culprit. Each clue eliminates suspects using CSP.")
# #     st.divider()

# #     # Introductory cases
# #     st.markdown("## Introductory Cases — Warm Up")
# #     fun_cols  = st.columns(2)
# #     fun_cases = {k: v for k, v in CASES.items() if v["level"] == "fun"}

# #     for i, (cid, case) in enumerate(fun_cases.items()):
# #         with fun_cols[i % 2]:
# #             stars    = st.session_state.case_stars.get(cid, 0)
# #             star_str = " [" + ("*" * stars) + "]" if stars else ""
# #             status   = "SOLVED" if cid in st.session_state.completed_cases else "NOT STARTED"
# #             s_color  = "#4ade80" if cid in st.session_state.completed_cases else "#888"
# #             st.markdown(f"""
# # <div class="case-card">
# #     <h3 style="color:#fff;">{case['title']}</h3>
# #     <p style="color:#aaa; font-size:12px; margin:2px 0;">{case['location']}</p>
# #     <p style="margin:8px 0;">{case['description'][:120]}...</p>
# #     <p>
# #         {badge_html(case['difficulty'])}
# #         &nbsp;
# #         <span style="color:{s_color}; font-size:12px; font-weight:600;">{status}{star_str}</span>
# #     </p>
# #     <p style="color:#666; font-size:12px;">
# #         {len(case['suspects'])} suspects &nbsp;|&nbsp;
# #         {len(case['locations'])} locations &nbsp;|&nbsp;
# #         {len(case['clues'])} clues
# #     </p>
# # </div>
# # """, unsafe_allow_html=True)
# #             btn_label = f"Replay — {case['title']}" if cid in st.session_state.completed_cases else f"Start — {case['title']}"
# #             if st.button(btn_label, key=f"start_{cid}"):
# #                 start_case(cid)
# #                 st.rerun()

# #     st.divider()

# #     # Investigation cases
# #     st.markdown("## Investigation Cases — Real Mysteries")
# #     serious_cases = {k: v for k, v in CASES.items() if v["level"] == "serious"}
# #     cols = st.columns(3)

# #     for i, (cid, case) in enumerate(serious_cases.items()):
# #         with cols[i % 3]:
# #             stars    = st.session_state.case_stars.get(cid, 0)
# #             star_str = " [" + ("*" * stars) + "]" if stars else ""
# #             status   = "SOLVED" if cid in st.session_state.completed_cases else "NOT STARTED"
# #             s_color  = "#4ade80" if cid in st.session_state.completed_cases else "#888"
# #             st.markdown(f"""
# # <div class="case-card">
# #     <h3 style="color:#fff;">{case['title']}</h3>
# #     <p style="color:#aaa; font-size:12px; margin:2px 0;">{case['location']}</p>
# #     <p style="margin:8px 0;">{case['description'][:110]}...</p>
# #     <p>
# #         {badge_html(case['difficulty'])}
# #         &nbsp;
# #         <span style="color:{s_color}; font-size:12px; font-weight:600;">{status}{star_str}</span>
# #     </p>
# #     <p style="color:#666; font-size:12px;">
# #         {len(case['suspects'])} suspects &nbsp;|&nbsp;
# #         {len(case['locations'])} locations &nbsp;|&nbsp;
# #         {len(case['clues'])} clues
# #     </p>
# # </div>
# # """, unsafe_allow_html=True)
# #             btn_label = f"Replay — {case['title']}" if cid in st.session_state.completed_cases else f"Start — {case['title']}"
# #             if st.button(btn_label, key=f"start_{cid}"):
# #                 start_case(cid)
# #                 st.rerun()


# # # ─────────────────────────────────────────────────────────────
# # #  SCREEN 2 — GAME
# # # ─────────────────────────────────────────────────────────────
# # elif st.session_state.screen == "game":

# #     case        = CASES[st.session_state.current_case_id]
# #     csp         = st.session_state.csp
# #     total_clues = len(case["clues"])
# #     revealed    = st.session_state.clues_revealed

# #     # Top bar
# #     col_title, col_meta = st.columns([2, 1])
# #     with col_title:
# #         st.markdown(f"# {case['title']}")
# #         st.markdown(f"*Location: {case['location']}*")
# #     with col_meta:
# #         st.markdown(f"**Clues Used:** {revealed} / {total_clues}")
# #         st.progress(revealed / total_clues if total_clues else 0)
# #         st.markdown(f"**Score:** {st.session_state.score}")

# #     st.divider()

# #     # Case description
# #     with st.expander("Case Description", expanded=True):
# #         st.markdown(f"*{case['description']}*")
# #         st.info(f"\"{case['quote']}\"")

# #     st.divider()

# #     # Main layout
# #     left_col, right_col = st.columns([1, 1])

# #     # LEFT — Suspects and Domains
# #     with left_col:

# #         st.markdown("### Suspects")
# #         state = csp.get_current_state()

# #         for suspect in case["suspects"]:
# #             role = case["suspect_roles"][suspect]
# #             if suspect in state["suspect_domain"]:
# #                 label_color  = "#d4af37"
# #                 status_label = "ACTIVE"
# #                 border_color = "#d4af37"
# #             else:
# #                 label_color  = "#555577"
# #                 status_label = "ELIMINATED"
# #                 border_color = "#2a2a4a"
# #             st.markdown(
# #                 f'<div style="background:#1a1a2e; border-radius:8px; '
# #                 f'padding:9px 14px; margin:5px 0; border-left:3px solid {border_color};">'
# #                 f'<span style="color:{label_color}; font-weight:600;">{suspect}</span>'
# #                 f'<span style="color:#666; font-size:11px;"> — {role}</span>'
# #                 f'<span style="float:right; font-size:11px; font-weight:600; color:{label_color};">'
# #                 f'{status_label}</span>'
# #                 f'</div>',
# #                 unsafe_allow_html=True
# #             )

# #         st.markdown("### Locations")
# #         st.markdown(
# #             domain_pills(state["location_domain"], case["locations"]),
# #             unsafe_allow_html=True
# #         )

# #         st.markdown("### Methods / Weapons")
# #         st.markdown(
# #             domain_pills(state["weapon_domain"], case["weapons"]),
# #             unsafe_allow_html=True
# #         )

# #     # RIGHT — Clues and Propagation
# #     with right_col:

# #         st.markdown("### Clues Revealed")

# #         for i in range(revealed):
# #             clue = case["clues"][i]
# #             st.markdown(
# #                 f'<div class="clue-card-done">'
# #                 f'<span style="color:#1d9e75; font-weight:600;">Clue {clue["id"]}:</span> '
# #                 f'{clue["text"]}'
# #                 f'</div>',
# #                 unsafe_allow_html=True
# #             )

# #         if revealed < total_clues:
# #             if st.button(f"Reveal Clue {revealed + 1}", use_container_width=True):
# #                 clue = case["clues"][revealed]
# #                 csp.apply_clue(clue)
# #                 st.session_state.clues_revealed += 1
# #                 st.rerun()
# #         else:
# #             st.success("All clues have been revealed. Make your accusation below.")

# #         st.markdown("### CSP Propagation Trace")
# #         log = csp.get_current_state()["propagation_log"]

# #         if not log:
# #             st.markdown(
# #                 '<div class="prop-step" style="color:#555577 !important;">'
# #                 'No clues applied yet. Reveal the first clue to begin.'
# #                 '</div>',
# #                 unsafe_allow_html=True
# #             )
# #         for entry in log:
# #             st.markdown(
# #                 f'<div class="prop-step">'
# #                 f'<span style="color:#e94560; font-weight:600;">[ Clue {entry["clue_id"]} ]</span> '
# #                 f'{entry["propagation"]}'
# #                 f'</div>',
# #                 unsafe_allow_html=True
# #             )

# #     st.divider()

# #     # Accusation section
# #     st.markdown("### Make Your Accusation")

# #     if csp.get_current_state()["solved"]:
# #         st.info("CSP has logically solved the case. Confirm your accusation below.")

# #     acc_col1, acc_col2, acc_col3 = st.columns(3)

# #     with acc_col1:
# #         suspect_choice = st.selectbox(
# #             "Who is the culprit?",
# #             options=case["suspects"],
# #             index=0
# #         )
# #     with acc_col2:
# #         location_choice = st.selectbox(
# #             "Where did it happen?",
# #             options=case["locations"],
# #             index=0
# #         )
# #     with acc_col3:
# #         weapon_choice = st.selectbox(
# #             "What method was used?",
# #             options=case["weapons"],
# #             index=0
# #         )

# #     st.warning("Warning: A wrong accusation will reset your progress on this case.")

# #     if st.button("Submit Accusation", use_container_width=True):
# #         correct = csp.verify_accusation(suspect_choice, location_choice, weapon_choice)
# #         if correct:
# #             stars  = stars_from_clues(revealed, total_clues)
# #             points = stars * 100 + max(0, (total_clues - revealed) * 20)
# #             st.session_state.score += points
# #             st.session_state.case_stars[st.session_state.current_case_id] = stars
# #             if st.session_state.current_case_id not in st.session_state.completed_cases:
# #                 st.session_state.completed_cases.append(st.session_state.current_case_id)
# #             st.session_state.verdict_correct = True
# #             st.session_state.screen = "verdict"
# #             st.rerun()
# #         else:
# #             st.session_state.wrong_attempts += 1
# #             st.error(
# #                 f"Incorrect accusation. That is not the right answer. "
# #                 f"({st.session_state.wrong_attempts} wrong attempt(s)). "
# #                 f"Reveal more clues and try again."
# #             )


# # # ─────────────────────────────────────────────────────────────
# # #  SCREEN 3 — VERDICT
# # # ─────────────────────────────────────────────────────────────
# # elif st.session_state.screen == "verdict":

# #     case     = CASES[st.session_state.current_case_id]
# #     csp      = st.session_state.csp
# #     stars    = st.session_state.case_stars.get(st.session_state.current_case_id, 1)
# #     solution = case["solution"]
# #     points   = stars * 100 + max(0, (len(case["clues"]) - st.session_state.clues_revealed) * 20)

# #     st.markdown(f"# Case Closed — {case['title']}")
# #     st.markdown("---")

# #     # Verdict card
# #     st.markdown(f"""
# # <div class="solved-card">
# #     <h2 style="color:#4ade80;">Accusation Correct. Case Solved.</h2>
# #     <br>
# #     <table width="100%">
# #         <tr>
# #             <td style="color:#888; padding:6px 0; width:160px;">Culprit</td>
# #             <td style="color:#fff; font-weight:bold;">{solution['culprit']}</td>
# #         </tr>
# #         <tr>
# #             <td style="color:#888; padding:6px 0;">Location</td>
# #             <td style="color:#fff; font-weight:bold;">{solution['location']}</td>
# #         </tr>
# #         <tr>
# #             <td style="color:#888; padding:6px 0;">Method Used</td>
# #             <td style="color:#fff; font-weight:bold;">{solution['weapon']}</td>
# #         </tr>
# #         <tr>
# #             <td style="color:#888; padding:6px 0;">Clues Used</td>
# #             <td style="color:#fff; font-weight:bold;">{st.session_state.clues_revealed} / {len(case['clues'])}</td>
# #         </tr>
# #         <tr>
# #             <td style="color:#888; padding:6px 0;">CSP Steps</td>
# #             <td style="color:#fff; font-weight:bold;">{len(csp.get_current_state()['propagation_log'])} propagations</td>
# #         </tr>
# #         <tr>
# #             <td style="color:#888; padding:6px 0;">Points Earned</td>
# #             <td style="color:#f59e0b; font-weight:bold;">{points} pts</td>
# #         </tr>
# #     </table>
# #     <br>
# #     <p style="font-size:13px; color:#888; margin-bottom:6px;">Rating</p>
# #     {star_display(stars)}
# # </div>
# # """, unsafe_allow_html=True)

# #     # Full CSP reasoning trace
# #     st.markdown("### Full CSP Reasoning Trace")

# #     for entry in csp.get_current_state()["propagation_log"]:
# #         eliminated = []
# #         if entry["changed"]["suspects"]:
# #             eliminated.append(f"Suspects removed: {', '.join(entry['changed']['suspects'])}")
# #         if entry["changed"]["locations"]:
# #             eliminated.append(f"Locations removed: {', '.join(entry['changed']['locations'])}")
# #         if entry["changed"]["weapons"]:
# #             eliminated.append(f"Weapons removed: {', '.join(entry['changed']['weapons'])}")
# #         elim_text = " | ".join(eliminated) if eliminated else "No direct eliminations — contextual reasoning applied"

# #         st.markdown(f"""
# # <div class="prop-step">
# #     <span style="color:#e94560; font-weight:600;">[ Clue {entry['clue_id']} ]</span> {entry['clue_text']}<br>
# #     <span style="color:#f59e0b;">&gt;&gt; {entry['propagation']}</span><br>
# #     <span style="color:#60a5fa;">&gt;&gt; {elim_text}</span>
# # </div>
# # """, unsafe_allow_html=True)

# #     st.divider()

# #     # Navigation
# #     btn_col1, btn_col2, btn_col3 = st.columns(3)

# #     with btn_col1:
# #         if st.button("Back to Home", use_container_width=True):
# #             go_home()
# #             st.rerun()

# #     with btn_col2:
# #         if st.button("Replay This Case", use_container_width=True):
# #             start_case(st.session_state.current_case_id)
# #             st.rerun()

# #     with btn_col3:
# #         next_case = None
# #         for cid in CASES:
# #             if cid not in st.session_state.completed_cases:
# #                 next_case = cid
# #                 break
# #         if next_case:
# #             if st.button(f"Next Case — {CASES[next_case]['title']}", use_container_width=True):
# #                 start_case(next_case)
# #                 st.rerun()
# #         else:
# #             st.success("All cases solved. You are the ultimate detective.")


# import streamlit as st
# from cases import CASES
# from csp_engine import CSPEngine

# # ─────────────────────────────────────────────────────────────
# # PAGE CONFIG
# # ─────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Mystery Solver",
#     page_icon="🕵️",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ─────────────────────────────────────────────────────────────
# # CUSTOM CSS
# # ─────────────────────────────────────────────────────────────
# st.markdown("""
# <style>

# /* Background */
# .stApp {
#     background-color: #0f172a;
# }

# /* Sidebar */
# [data-testid="stSidebar"] {
#     background-color: #111827;
# }

# /* Text */
# html, body, [class*="css"] {
#     color: #f3f4f6;
# }

# /* Buttons */
# .stButton > button {
#     width: 100%;
#     border-radius: 10px;
#     background: #dc2626;
#     color: white;
#     border: none;
#     padding: 0.6rem;
#     font-weight: 600;
# }

# .stButton > button:hover {
#     background: #b91c1c;
#     color: white;
# }

# /* Cards */
# .case-card {
#     background: #1e293b;
#     border: 1px solid #334155;
#     border-radius: 14px;
#     padding: 18px;
#     margin-bottom: 15px;
# }

# /* Solved Card */
# .solved-card {
#     background: #052e16;
#     border: 1px solid #22c55e;
#     border-radius: 14px;
#     padding: 20px;
# }

# /* Clues */
# .clue-card {
#     background: #1e293b;
#     border-left: 4px solid #dc2626;
#     padding: 12px;
#     border-radius: 8px;
#     margin-bottom: 10px;
# }

# /* Propagation */
# .prop-step {
#     background: #111827;
#     border: 1px solid #334155;
#     border-radius: 8px;
#     padding: 10px;
#     margin-bottom: 8px;
#     font-size: 13px;
# }

# /* Domain pills */
# .domain-active {
#     background: #14532d;
#     color: #86efac;
#     padding: 4px 10px;
#     border-radius: 999px;
#     display: inline-block;
#     margin: 4px;
#     font-size: 12px;
# }

# .domain-elim {
#     background: #1e293b;
#     color: #64748b;
#     text-decoration: line-through;
#     padding: 4px 10px;
#     border-radius: 999px;
#     display: inline-block;
#     margin: 4px;
#     font-size: 12px;
# }

# /* Difficulty badges */
# .badge-easy {
#     background: #14532d;
#     color: #86efac;
#     padding: 4px 10px;
#     border-radius: 6px;
#     font-size: 12px;
# }

# .badge-medium {
#     background: #78350f;
#     color: #fdba74;
#     padding: 4px 10px;
#     border-radius: 6px;
#     font-size: 12px;
# }

# .badge-hard {
#     background: #7f1d1d;
#     color: #fca5a5;
#     padding: 4px 10px;
#     border-radius: 6px;
#     font-size: 12px;
# }

# .badge-expert {
#     background: #581c87;
#     color: #d8b4fe;
#     padding: 4px 10px;
#     border-radius: 6px;
#     font-size: 12px;
# }

# </style>
# """, unsafe_allow_html=True)

# # ─────────────────────────────────────────────────────────────
# # SESSION STATE
# # ─────────────────────────────────────────────────────────────
# def init_state():

#     defaults = {
#         "screen": "home",
#         "current_case_id": None,
#         "csp": None,
#         "clues_revealed": 0,
#         "score": 0,
#         "completed_cases": [],
#         "case_stars": {},
#         "wrong_attempts": 0
#     }

#     for key, value in defaults.items():
#         if key not in st.session_state:
#             st.session_state[key] = value

# init_state()

# # ─────────────────────────────────────────────────────────────
# # HELPERS
# # ─────────────────────────────────────────────────────────────
# def badge_html(difficulty):

#     mapping = {
#         "Easy": "badge-easy",
#         "Medium": "badge-medium",
#         "Hard": "badge-hard",
#         "Expert": "badge-expert"
#     }

#     return f'<span class="{mapping[difficulty]}">{difficulty}</span>'

# def domain_pills(active, all_items):

#     html = ""

#     for item in all_items:

#         if item in active:
#             html += f'<span class="domain-active">{item}</span>'
#         else:
#             html += f'<span class="domain-elim">{item}</span>'

#     return html

# def start_case(case_id):

#     st.session_state.current_case_id = case_id
#     st.session_state.csp = CSPEngine(CASES[case_id])
#     st.session_state.clues_revealed = 0
#     st.session_state.wrong_attempts = 0
#     st.session_state.screen = "game"

# def go_home():

#     st.session_state.screen = "home"
#     st.session_state.current_case_id = None
#     st.session_state.csp = None

# def stars_from_clues(clues_used, total):

#     ratio = clues_used / total

#     if ratio <= 0.5:
#         return 3
#     elif ratio <= 0.75:
#         return 2

#     return 1

# # ─────────────────────────────────────────────────────────────
# # SIDEBAR
# # ─────────────────────────────────────────────────────────────
# with st.sidebar:

#     st.title("🕵️ Mystery Solver")

#     st.markdown(f"### Score: `{st.session_state.score}`")
#     st.markdown(f"### Solved Cases: `{len(st.session_state.completed_cases)}`")

#     st.divider()

#     st.subheader("All Cases")

#     for cid, case in CASES.items():

#         solved = "✅" if cid in st.session_state.completed_cases else "🕵️"

#         if st.button(f"{solved} Case {cid}"):
#             start_case(cid)
#             st.rerun()

#     if st.session_state.screen != "home":

#         st.divider()

#         if st.button("⬅ Back Home"):
#             go_home()
#             st.rerun()

# # ─────────────────────────────────────────────────────────────
# # HOME SCREEN
# # ─────────────────────────────────────────────────────────────
# if st.session_state.screen == "home":

#     st.title("🕵️ Mystery Solver")
#     st.markdown("### Solve mysteries using CSP, AC-3 and logical deduction.")

#     st.divider()

#     # FUN CASES
#     st.header("🍰 Introductory Cases")

#     fun_cases = {k: v for k, v in CASES.items() if v["level"] == "fun"}

#     fun_list = list(fun_cases.items())

#     for row_start in range(0, len(fun_list), 2):

#         cols = st.columns(2)

#         row_cases = fun_list[row_start:row_start + 2]

#         for col, (cid, case) in zip(cols, row_cases):

#             with col:

#                 solved = cid in st.session_state.completed_cases
#                 status = "SOLVED" if solved else "NOT STARTED"

#                 st.markdown(f"""
# <div class="case-card">

# <h3>{case['emoji']} {case['title']}</h3>

# <p style="color:#94a3b8;">
# {case['location']}
# </p>

# <p>
# {case['description'][:140]}...
# </p>

# <p>
# {badge_html(case['difficulty'])}
# &nbsp;
# <span style="color:#94a3b8;">{status}</span>
# </p>

# <p style="font-size:12px;color:#64748b;">
# {len(case['suspects'])} suspects |
# {len(case['locations'])} locations |
# {len(case['clues'])} clues
# </p>

# </div>
# """, unsafe_allow_html=True)

#                 btn = "Replay Case" if solved else "Start Case"

#                 if st.button(btn, key=f"fun_{cid}"):
#                     start_case(cid)
#                     st.rerun()

#     st.divider()

#     # SERIOUS CASES
#     st.header("🏦 Investigation Cases")

#     serious_cases = {k: v for k, v in CASES.items() if v["level"] == "serious"}

#     serious_list = list(serious_cases.items())

#     for row_start in range(0, len(serious_list), 3):

#         cols = st.columns(3)

#         row_cases = serious_list[row_start:row_start + 3]

#         for col, (cid, case) in zip(cols, row_cases):

#             with col:

#                 solved = cid in st.session_state.completed_cases
#                 status = "SOLVED" if solved else "NOT STARTED"

#                 st.markdown(f"""
# <div class="case-card">

# <h3>{case['emoji']} {case['title']}</h3>

# <p style="color:#94a3b8;">
# {case['location']}
# </p>

# <p>
# {case['description'][:120]}...
# </p>

# <p>
# {badge_html(case['difficulty'])}
# &nbsp;
# <span style="color:#94a3b8;">{status}</span>
# </p>

# <p style="font-size:12px;color:#64748b;">
# {len(case['suspects'])} suspects |
# {len(case['locations'])} locations |
# {len(case['clues'])} clues
# </p>

# </div>
# """, unsafe_allow_html=True)

#                 btn = "Replay Case" if solved else "Start Case"

#                 if st.button(btn, key=f"serious_{cid}"):
#                     start_case(cid)
#                     st.rerun()

# # ─────────────────────────────────────────────────────────────
# # GAME SCREEN
# # ─────────────────────────────────────────────────────────────
# elif st.session_state.screen == "game":

#     case = CASES[st.session_state.current_case_id]
#     csp = st.session_state.csp

#     total_clues = len(case["clues"])
#     revealed = st.session_state.clues_revealed

#     st.title(f"{case['emoji']} {case['title']}")

#     st.markdown(f"### {case['location']}")

#     st.progress(revealed / total_clues)

#     st.info(case["quote"])

#     st.markdown(case["description"])

#     st.divider()

#     left, right = st.columns([1, 1])

#     # LEFT
#     with left:

#         st.subheader("Suspects")

#         state = csp.get_current_state()

#         for suspect in case["suspects"]:

#             role = case["suspect_roles"][suspect]

#             if suspect in state["suspect_domain"]:
#                 color = "#22c55e"
#                 status = "ACTIVE"
#             else:
#                 color = "#64748b"
#                 status = "ELIMINATED"

#             st.markdown(f"""
# <div class="case-card" style="border-left:4px solid {color};">
# <b>{suspect}</b><br>
# <span style="color:#94a3b8;">{role}</span><br>
# <span style="color:{color};font-size:12px;">{status}</span>
# </div>
# """, unsafe_allow_html=True)

#         st.subheader("Locations")

#         st.markdown(
#             domain_pills(
#                 state["location_domain"],
#                 case["locations"]
#             ),
#             unsafe_allow_html=True
#         )

#         st.subheader("Weapons / Methods")

#         st.markdown(
#             domain_pills(
#                 state["weapon_domain"],
#                 case["weapons"]
#             ),
#             unsafe_allow_html=True
#         )

#     # RIGHT
#     with right:

#         st.subheader("Clues")

#         for i in range(revealed):

#             clue = case["clues"][i]

#             st.markdown(f"""
# <div class="clue-card">
# <b>Clue {clue['id']}:</b><br>
# {clue['text']}
# </div>
# """, unsafe_allow_html=True)

#         if revealed < total_clues:

#             if st.button(f"Reveal Clue {revealed + 1}"):

#                 clue = case["clues"][revealed]

#                 csp.apply_clue(clue)

#                 st.session_state.clues_revealed += 1

#                 st.rerun()

#         else:
#             st.success("All clues revealed.")

#         st.subheader("CSP Propagation")

#         logs = csp.get_current_state()["propagation_log"]

#         if not logs:

#             st.info("No propagation yet.")

#         for entry in logs:

#             st.markdown(f"""
# <div class="prop-step">
# <b>Clue {entry['clue_id']}</b><br>
# {entry['propagation']}
# </div>
# """, unsafe_allow_html=True)

#     st.divider()

#     # ACCUSATION
#     st.subheader("Make Your Accusation")

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         suspect_choice = st.selectbox(
#             "Culprit",
#             case["suspects"]
#         )

#     with col2:
#         location_choice = st.selectbox(
#             "Location",
#             case["locations"]
#         )

#     with col3:
#         weapon_choice = st.selectbox(
#             "Method",
#             case["weapons"]
#         )

#     st.warning("Wrong accusation means retrying the case.")

#     if st.button("Submit Accusation"):

#         correct = csp.verify_accusation(
#             suspect_choice,
#             location_choice,
#             weapon_choice
#         )

#         if correct:

#             stars = stars_from_clues(revealed, total_clues)

#             points = stars * 100

#             st.session_state.score += points

#             if st.session_state.current_case_id not in st.session_state.completed_cases:

#                 st.session_state.completed_cases.append(
#                     st.session_state.current_case_id
#                 )

#             st.session_state.case_stars[
#                 st.session_state.current_case_id
#             ] = stars

#             st.session_state.screen = "verdict"

#             st.rerun()

#         else:

#             st.error("Incorrect accusation.")

# # ─────────────────────────────────────────────────────────────
# # VERDICT SCREEN
# # ─────────────────────────────────────────────────────────────
# elif st.session_state.screen == "verdict":

#     case = CASES[st.session_state.current_case_id]

#     solution = case["solution"]

#     stars = st.session_state.case_stars.get(
#         st.session_state.current_case_id,
#         1
#     )

#     st.title("✅ CASE SOLVED")

#     st.markdown(f"""
# <div class="solved-card">

# <h2>{case['title']}</h2>

# <p><b>Culprit:</b> {solution['culprit']}</p>

# <p><b>Location:</b> {solution['location']}</p>

# <p><b>Method:</b> {solution['weapon']}</p>

# <p><b>Stars:</b> {'⭐' * stars}</p>

# </div>
# """, unsafe_allow_html=True)

#     st.divider()

#     st.subheader("Reasoning Trace")

#     logs = st.session_state.csp.get_current_state()["propagation_log"]

#     for entry in logs:

#         st.markdown(f"""
# <div class="prop-step">
# <b>Clue {entry['clue_id']}</b><br>
# {entry['clue_text']}<br><br>

# <b>Propagation:</b><br>
# {entry['propagation']}
# </div>
# """, unsafe_allow_html=True)

#     st.divider()

#     c1, c2 = st.columns(2)

#     with c1:

#         if st.button("🏠 Home"):
#             go_home()
#             st.rerun()

#     with c2:

#         if st.button("🔄 Replay"):
#             start_case(st.session_state.current_case_id)
#             st.rerun()



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
