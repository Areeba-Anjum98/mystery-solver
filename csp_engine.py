from collections import deque


class CSPEngine:
    """
    Hybrid CSP Engine — supports two modes automatically:

    MODE A — Real AC-3 (Cases 1, 2, 3):
        Clue provides FACTS only.
        Engine has CONSTRAINT RULES (like map coloring).
        AC-3 algorithm checks every domain value against every rule.
        Engine itself decides what to eliminate — human does not pre-decide.

    MODE B — Simple Propagation (Cases 4, 5, 6, 7):
        Clue directly lists what to eliminate.
        Engine executes the elimination and logs it.
        Still CSP structure: variables, domains, constraints applied.

    Both modes use the same CSP structure:
        Variables  → suspect, location, weapon
        Domains    → all possible values at start
        Constraints → rules (Mode A) or direct eliminates (Mode B)
    """

    def __init__(self, case: dict):

        # ── Domains — all values possible at start ───────────────
        self.domains = {
            "suspect":  list(case["suspects"]),
            "location": list(case["locations"]),
            "weapon":   list(case["weapons"])
        }

        # ── Knowledge base — facts collected from clues ──────────
        self.knowledge_base = {}

        # ── Constraints — used in Mode A (AC-3) cases ────────────
        self.constraints = case.get("constraints", [])

        # ── Determine mode automatically ─────────────────────────
        # If case has constraints list → Mode A (real AC-3)
        # If clues use eliminates dict  → Mode B (simple)
        self.mode = "ac3" if self.constraints else "simple"

        # ── Logs and state ────────────────────────────────────────
        self.propagation_log = []
        self.solved          = False
        self.solution        = case["solution"]

    # ─────────────────────────────────────────────────────────────
    #  MAIN — called when player reveals a clue
    # ─────────────────────────────────────────────────────────────

    def apply_clue(self, clue: dict) -> dict:
        """
        Route to correct mode based on case type.
        Both modes return same result structure for app.py compatibility.
        """
        if self.mode == "ac3":
            return self._apply_clue_ac3(clue)
        else:
            return self._apply_clue_simple(clue)

    # ─────────────────────────────────────────────────────────────
    #  MODE A — Real AC-3
    # ─────────────────────────────────────────────────────────────

    def _apply_clue_ac3(self, clue: dict) -> dict:
        """
        AC-3 mode:
        Step 1 — Add clue facts to knowledge base
        Step 2 — Run AC-3: engine checks every value against every constraint
        Step 3 — Log what was eliminated and why
        """

        # Step 1 — update knowledge base with new facts
        new_facts = clue.get("facts", {})
        self.knowledge_base.update(new_facts)

        # Step 2 — run AC-3 algorithm
        eliminated = self._run_ac3()

        # Step 3 — build log entry
        propagation_text = self._build_ac3_log(eliminated, clue)

        self.propagation_log.append({
            "clue_id":     clue["id"],
            "clue_text":   clue["text"],
            "propagation": propagation_text,
            "mode":        "AC-3",
            "facts_added": new_facts,
            "changed": {
                "suspects":  eliminated.get("suspect",  []),
                "locations": eliminated.get("location", []),
                "weapons":   eliminated.get("weapon",   [])
            }
        })

        self.check_solved()

        return self._result_dict(eliminated)

    def _run_ac3(self) -> dict:
        """
        Arc Consistency Algorithm 3.

        Exactly like map coloring:
          Map coloring:  constraint(WA, NT) → colors must differ
                         engine removes Red from NT when WA=Red

          Mystery game:  constraint(suspect) → must not have left before crime
                         engine removes Usman when usman_left_early=True

        Queue holds (variable, value, constraint_index) triples.
        Each value tested against its constraint.
        Failed values removed. Related arcs re-queued.
        Continues until queue empty = arc consistent state.
        """

        eliminated = {"suspect": [], "location": [], "weapon": []}

        if not self.constraints:
            return eliminated

        # Build queue — every (variable, value, constraint) combination
        queue = deque()
        for i, (variable, _) in enumerate(self.constraints):
            for value in list(self.domains[variable]):
                queue.append((variable, value, i))

        visited = set()

        while queue:

            variable, value, c_idx = queue.popleft()

            key = (variable, value, c_idx)
            if key in visited:
                continue
            visited.add(key)

            # Skip already eliminated values
            if value not in self.domains[variable]:
                continue

            _, constraint_fn = self.constraints[c_idx]

            # Test: does this value satisfy this constraint?
            # True  = keep value in domain
            # False = remove value from domain
            try:
                still_valid = constraint_fn(value, self.knowledge_base)
            except Exception:
                still_valid = True  # constraint cannot evaluate yet — keep

            if not still_valid:

                # Remove from domain
                self.domains[variable].remove(value)
                eliminated[variable].append(value)

                # Re-queue related arcs (same as map coloring re-queuing)
                for i2, (var2, _) in enumerate(self.constraints):
                    if var2 == variable:
                        for remaining in list(self.domains[variable]):
                            new_key = (variable, remaining, i2)
                            if new_key not in visited:
                                queue.append((variable, remaining, i2))

        return eliminated

    def _build_ac3_log(self, eliminated: dict, clue: dict) -> str:
        """Build readable explanation of AC-3 reasoning."""
        parts = []

        facts = clue.get("facts", {})
        if facts:
            parts.append(f"KB updated: {', '.join(f'{k}={v}' for k,v in facts.items())}")

        for var_type, values in eliminated.items():
            if values:
                reason = clue.get("reason", {}).get(var_type, "constraint violated")
                parts.append(f"AC-3 eliminated {var_type}(s) [{', '.join(values)}] — {reason}")

        for var_type in ["suspect", "location", "weapon"]:
            if len(self.domains[var_type]) == 1:
                parts.append(f"{var_type.capitalize()} resolved: {self.domains[var_type][0]}")

        return " | ".join(parts) if parts else "Constraint applied."

    # ─────────────────────────────────────────────────────────────
    #  MODE B — Simple Propagation
    # ─────────────────────────────────────────────────────────────

    def _apply_clue_simple(self, clue: dict) -> dict:
        """
        Simple mode:
        Clue directly specifies what to eliminate.
        Engine executes and logs.
        Still CSP: domains shrink, propagation logged, solved checked.
        """

        eliminates = clue.get("eliminates", {})
        changed    = {"suspects": [], "locations": [], "weapons": []}

        for suspect in eliminates.get("suspects", []):
            if suspect in self.domains["suspect"]:
                self.domains["suspect"].remove(suspect)
                changed["suspects"].append(suspect)

        for location in eliminates.get("locations", []):
            if location in self.domains["location"]:
                self.domains["location"].remove(location)
                changed["locations"].append(location)

        for weapon in eliminates.get("weapons", []):
            if weapon in self.domains["weapon"]:
                self.domains["weapon"].remove(weapon)
                changed["weapons"].append(weapon)

        self.propagation_log.append({
            "clue_id":     clue["id"],
            "clue_text":   clue["text"],
            "propagation": clue.get("propagation", "Domain reduced."),
            "mode":        "Simple",
            "facts_added": {},
            "changed":     changed
        })

        self.check_solved()

        elim_dict = {
            "suspect":  changed["suspects"],
            "location": changed["locations"],
            "weapon":   changed["weapons"]
        }
        return self._result_dict(elim_dict)

    # ─────────────────────────────────────────────────────────────
    #  SHARED HELPERS
    # ─────────────────────────────────────────────────────────────

    def _result_dict(self, eliminated: dict) -> dict:
        return {
            "changed": {
                "suspects":  eliminated.get("suspect",  []),
                "locations": eliminated.get("location", []),
                "weapons":   eliminated.get("weapon",   [])
            },
            "suspect_domain":  list(self.domains["suspect"]),
            "location_domain": list(self.domains["location"]),
            "weapon_domain":   list(self.domains["weapon"]),
            "solved":          self.solved
        }

    def check_solved(self):
        if all(len(self.domains[v]) == 1 for v in ["suspect", "location", "weapon"]):
            self.solved = True

    def get_current_state(self) -> dict:
        return {
            "suspect_domain":  list(self.domains["suspect"]),
            "location_domain": list(self.domains["location"]),
            "weapon_domain":   list(self.domains["weapon"]),
            "solved":          self.solved,
            "propagation_log": list(self.propagation_log),
            "knowledge_base":  dict(self.knowledge_base),
            "mode":            self.mode
        }

    def verify_accusation(self, suspect: str, location: str, weapon: str) -> bool:
        return (
            suspect  == self.solution["culprit"]  and
            location == self.solution["location"] and
            weapon   == self.solution["weapon"]
        )
