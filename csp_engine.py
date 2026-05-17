class CSPEngine:
    """
    Constraint Satisfaction Problem engine for Mystery Solver.
    Manages domains for suspects, locations, and weapons.
    Applies constraint propagation (Arc Consistency) on each clue.
    """

    def __init__(self, case: dict):
        # Initialize domains — all values possible at start
        self.suspect_domain  = list(case["suspects"])
        self.location_domain = list(case["locations"])
        self.weapon_domain   = list(case["weapons"])
        self.propagation_log = []
        self.solved          = False
        self.solution        = case["solution"]

    def apply_clue(self, clue: dict) -> dict:
        """
        Apply one clue to the CSP.
        Eliminates values from domains based on the clue's constraints.
        Returns a result dict with what changed.
        """
        eliminates = clue.get("eliminates", {})
        changed    = {"suspects": [], "locations": [], "weapons": []}

        # Remove eliminated suspects
        for suspect in eliminates.get("suspects", []):
            if suspect in self.suspect_domain:
                self.suspect_domain.remove(suspect)
                changed["suspects"].append(suspect)

        # Remove eliminated locations
        for location in eliminates.get("locations", []):
            if location in self.location_domain:
                self.location_domain.remove(location)
                changed["locations"].append(location)

        # Remove eliminated weapons
        for weapon in eliminates.get("weapons", []):
            if weapon in self.weapon_domain:
                self.weapon_domain.remove(weapon)
                changed["weapons"].append(weapon)

        # Log the propagation step
        self.propagation_log.append({
            "clue_id": clue["id"],
            "clue_text": clue["text"],
            "propagation": clue["propagation"],
            "changed": changed
        })

        # Check if solved — each domain has exactly one value
        self.check_solved()

        return {
            "changed": changed,
            "suspect_domain":  list(self.suspect_domain),
            "location_domain": list(self.location_domain),
            "weapon_domain":   list(self.weapon_domain),
            "solved":          self.solved
        }

    def check_solved(self):
        """Mark as solved when all domains are reduced to one value."""
        if (len(self.suspect_domain)  == 1 and
            len(self.location_domain) == 1 and
            len(self.weapon_domain)   == 1):
            self.solved = True

    def get_current_state(self) -> dict:
        """Return current state of all domains."""
        return {
            "suspect_domain":  list(self.suspect_domain),
            "location_domain": list(self.location_domain),
            "weapon_domain":   list(self.weapon_domain),
            "solved":          self.solved,
            "propagation_log": list(self.propagation_log)
        }

    def verify_accusation(self, suspect: str, location: str, weapon: str) -> bool:
        """Check if player's accusation matches the correct solution."""
        return (
            suspect  == self.solution["culprit"]   and
            location == self.solution["location"]  and
            weapon   == self.solution["weapon"]
        )
