# class CSPEngine:
#     """
#     Constraint Satisfaction Problem engine for Mystery Solver.
#     Manages domains for suspects, locations, and weapons.
#     Applies constraint propagation (Arc Consistency) on each clue.
#     """

#     def __init__(self, case: dict):
#         # Initialize domains — all values possible at start
#         self.suspect_domain  = list(case["suspects"])
#         self.location_domain = list(case["locations"])
#         self.weapon_domain   = list(case["weapons"])
#         self.propagation_log = []
#         self.solved          = False
#         self.solution        = case["solution"]

#     def apply_clue(self, clue: dict) -> dict:
#         """
#         Apply one clue to the CSP.
#         Eliminates values from domains based on the clue's constraints.
#         Returns a result dict with what changed.
#         """
#         eliminates = clue.get("eliminates", {})
#         changed    = {"suspects": [], "locations": [], "weapons": []}

#         # Remove eliminated suspects
#         for suspect in eliminates.get("suspects", []):
#             if suspect in self.suspect_domain:
#                 self.suspect_domain.remove(suspect)
#                 changed["suspects"].append(suspect)

#         # Remove eliminated locations
#         for location in eliminates.get("locations", []):
#             if location in self.location_domain:
#                 self.location_domain.remove(location)
#                 changed["locations"].append(location)

#         # Remove eliminated weapons
#         for weapon in eliminates.get("weapons", []):
#             if weapon in self.weapon_domain:
#                 self.weapon_domain.remove(weapon)
#                 changed["weapons"].append(weapon)

#         # Log the propagation step
#         self.propagation_log.append({
#             "clue_id": clue["id"],
#             "clue_text": clue["text"],
#             "propagation": clue["propagation"],
#             "changed": changed
#         })

#         # Check if solved — each domain has exactly one value
#         self.check_solved()

#         return {
#             "changed": changed,
#             "suspect_domain":  list(self.suspect_domain),
#             "location_domain": list(self.location_domain),
#             "weapon_domain":   list(self.weapon_domain),
#             "solved":          self.solved
#         }

#     def check_solved(self):
#         """Mark as solved when all domains are reduced to one value."""
#         if (len(self.suspect_domain)  == 1 and
#             len(self.location_domain) == 1 and
#             len(self.weapon_domain)   == 1):
#             self.solved = True

#     def get_current_state(self) -> dict:
#         """Return current state of all domains."""
#         return {
#             "suspect_domain":  list(self.suspect_domain),
#             "location_domain": list(self.location_domain),
#             "weapon_domain":   list(self.weapon_domain),
#             "solved":          self.solved,
#             "propagation_log": list(self.propagation_log)
#         }

#     def verify_accusation(self, suspect: str, location: str, weapon: str) -> bool:
#         """Check if player's accusation matches the correct solution."""
#         return (
#             suspect  == self.solution["culprit"]   and
#             location == self.solution["location"]  and
#             weapon   == self.solution["weapon"]
#         )


from collections import deque


class CSPEngine:
    """
    Real AC-3 Constraint Satisfaction Problem engine for Mystery Solver.

    HOW THIS WORKS (vs the old engine):
    ─────────────────────────────────────────────────────────────────
    OLD engine: clue directly said "eliminate Kamran" — human pre-solved it.
    NEW engine: clue adds a FACT to knowledge base. Engine itself reasons
                using constraint rules to figure out what gets eliminated.
                This is real AC-3 propagation — exactly like map coloring.

    CSP Structure:
        Variables   → suspect, location, weapon  (what we want to find)
        Domains     → all possible values for each variable
        Constraints → rules defined per case (e.g. alibi times, access rules)
        AC-3        → arc consistency algorithm that propagates eliminations
    ─────────────────────────────────────────────────────────────────
    """

    def __init__(self, case: dict):

        # ── Domains — all values possible at start ───────────────
        self.domains = {
            "suspect":  list(case["suspects"]),
            "location": list(case["locations"]),
            "weapon":   list(case["weapons"])
        }

        # ── Knowledge base — facts collected from clues ──────────
        # Engine reasons FROM these facts automatically
        self.knowledge_base = {}

        # ── Constraints — rules the engine uses to infer ─────────
        # Each constraint: (variable, function)
        # function(value, knowledge_base) → True = value still possible
        # function returns False → value gets eliminated automatically
        self.constraints = case.get("constraints", [])

        # ── Logs and state ────────────────────────────────────────
        self.propagation_log = []
        self.solved          = False
        self.solution        = case["solution"]

    # ─────────────────────────────────────────────────────────────
    #  MAIN FUNCTION — called when player reveals a clue
    # ─────────────────────────────────────────────────────────────

    def apply_clue(self, clue: dict) -> dict:
        """
        Player reveals a clue.
        Step 1 — Add clue facts to knowledge base.
        Step 2 — Run AC-3: engine automatically figures out eliminations.
        Step 3 — Log what changed and why.
        """

        # Step 1 — Add facts from this clue to knowledge base
        new_facts = clue.get("facts", {})
        self.knowledge_base.update(new_facts)

        # Step 2 — Run real AC-3
        eliminated = self._run_ac3()

        # Step 3 — Build explanation and log
        propagation_text = self._build_propagation_text(eliminated, clue)

        self.propagation_log.append({
            "clue_id":     clue["id"],
            "clue_text":   clue["text"],
            "propagation": propagation_text,
            "facts_added": new_facts,
            "changed": {
                "suspects":  eliminated.get("suspect",  []),
                "locations": eliminated.get("location", []),
                "weapons":   eliminated.get("weapon",   [])
            }
        })

        self.check_solved()

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

    # ─────────────────────────────────────────────────────────────
    #  AC-3 ALGORITHM — real constraint propagation
    # ─────────────────────────────────────────────────────────────

    def _run_ac3(self) -> dict:
        """
        Real AC-3 (Arc Consistency Algorithm 3).

        Exactly like map coloring AC-3:
          - Queue holds all (variable, value, constraint_index) to check
          - For each value in each domain, test against its constraint
          - If value violates constraint → remove it from domain
          - If any domain changed → re-queue related arcs
          - Repeat until queue is empty (fully arc consistent)

        The KEY difference from old engine:
          Old: human said "remove Kamran"
          New: constraint says "suspect must not have alibi before crime"
               engine checks each suspect against this rule itself
               engine removes Kamran because his alibi_time < crime_time
        """
        eliminated = {"suspect": [], "location": [], "weapon": []}

        if not self.constraints:
            return eliminated

        # Build initial queue — every (variable, value, constraint) triple
        queue = deque()
        for i, (variable, _) in enumerate(self.constraints):
            for value in list(self.domains[variable]):
                queue.append((variable, value, i))

        visited = set()

        while queue:
            variable, value, constraint_idx = queue.popleft()

            key = (variable, value, constraint_idx)
            if key in visited:
                continue
            visited.add(key)

            # Skip if this value was already eliminated
            if value not in self.domains[variable]:
                continue

            # Get constraint function for this variable
            _, constraint_fn = self.constraints[constraint_idx]

            # Ask the constraint: can this value still exist?
            # constraint_fn(value, knowledge_base) → True = keep, False = remove
            try:
                still_possible = constraint_fn(value, self.knowledge_base)
            except Exception:
                still_possible = True  # if constraint can't evaluate yet, keep

            if not still_possible:

                # Remove value from domain
                self.domains[variable].remove(value)
                eliminated[variable].append(value)

                # Domain changed — re-check all constraints for this variable
                # (same logic as map coloring: when NT loses a color,
                #  re-check all arcs involving NT)
                for i2, (var2, _) in enumerate(self.constraints):
                    if var2 == variable:
                        for remaining in list(self.domains[variable]):
                            new_key = (variable, remaining, i2)
                            if new_key not in visited:
                                queue.append((variable, remaining, i2))

        return eliminated

    # ─────────────────────────────────────────────────────────────
    #  HELPERS
    # ─────────────────────────────────────────────────────────────

    def _build_propagation_text(self, eliminated: dict, clue: dict) -> str:
        """Build readable explanation of what AC-3 inferred this step."""

        parts = []

        # Show facts added to knowledge base
        facts = clue.get("facts", {})
        if facts:
            fact_strs = [f"{k} = {v}" for k, v in facts.items()]
            parts.append(f"KB updated: {', '.join(fact_strs)}")

        # Show what was eliminated and why
        for var_type, values in eliminated.items():
            if values:
                reason = clue.get("reason", {}).get(var_type, "constraint violated")
                parts.append(
                    f"AC-3 removed {var_type}(s) [{', '.join(values)}] — {reason}"
                )

        # Announce when a variable is fully resolved
        for var_type in ["suspect", "location", "weapon"]:
            domain = self.domains[var_type]
            if len(domain) == 1:
                parts.append(
                    f"{var_type.capitalize()} resolved: {domain[0]}"
                )

        return " | ".join(parts) if parts else clue.get("propagation", "Constraint applied.")

    def check_solved(self):
        """Case is solved when every domain has exactly one value."""
        if all(len(self.domains[v]) == 1 for v in ["suspect", "location", "weapon"]):
            self.solved = True

    def get_current_state(self) -> dict:
        return {
            "suspect_domain":  list(self.domains["suspect"]),
            "location_domain": list(self.domains["location"]),
            "weapon_domain":   list(self.domains["weapon"]),
            "solved":          self.solved,
            "propagation_log": list(self.propagation_log),
            "knowledge_base":  dict(self.knowledge_base)
        }

    def verify_accusation(self, suspect: str, location: str, weapon: str) -> bool:
        return (
            suspect  == self.solution["culprit"]  and
            location == self.solution["location"] and
            weapon   == self.solution["weapon"]
        )
