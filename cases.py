CASES = {

    # ═══════════════════════════════════════════════════════════════
    #  CASES 1 & 2 — FUN / INTRODUCTORY
    #  MODE: Real AC-3
    #  Clues provide FACTS only. Constraints are rules like map coloring.
    #  Engine infers eliminations automatically — human does not pre-decide.
    # ═══════════════════════════════════════════════════════════════

    1: {
        "id": 1,
        "level": "fun",
        "difficulty": "Easy",
        "emoji": "🍰",
        "title": "The Missing Cake Mystery",
        "location": "Home Kitchen",
        "description": (
            "Mom baked a beautiful chocolate cake and left it on the kitchen counter. "
            "One hour later — the cake was completely gone! Only three suspects were "
            "home at the time. Someone has a sweet tooth and a guilty conscience."
        ),
        "quote": "There were chocolate crumbs on the floor and small footprints near the counter...",
        "suspects": ["Brother Ali", "Sister Sara", "Dog Bruno"],
        "suspect_roles": {
            "Brother Ali": "12-year-old, loves chocolate",
            "Sister Sara": "8-year-old, just had lunch",
            "Dog Bruno":   "Golden Retriever, always hungry"
        },
        "locations": ["Kitchen Counter", "Living Room", "Backyard", "Bedroom"],
        "weapons":   ["Ate it directly", "Shared with friend", "Knocked it to floor"],
        "solution": {
            "culprit":  "Dog Bruno",
            "location": "Kitchen Counter",
            "weapon":   "Knocked it to floor"
        },

        # ── REAL AC-3 CONSTRAINTS ────────────────────────────────
        # Rule 1: if paw_prints found → only Dog Bruno possible
        # Rule 2: if sara_alibi confirmed → Sara impossible
        # Rule 3: if crime_scene known → only that location possible
        # Rule 4: if cake_knocked → only Knocked it to floor possible
        "constraints": [
            ("suspect",
             lambda v, kb: not kb.get("paw_prints") or v == "Dog Bruno"),
            ("suspect",
             lambda v, kb: not (kb.get("sara_alibi") and v == "Sister Sara")),
            ("location",
             lambda v, kb: kb.get("crime_scene") is None or v == kb["crime_scene"]),
            ("weapon",
             lambda v, kb: not kb.get("cake_knocked") or v == "Knocked it to floor"),
        ],

        # ── CLUES — facts only, no eliminates ────────────────────
        "clues": [
            {
                "id": 1,
                "text": "Small paw-shaped chocolate prints were found on the kitchen floor leading to the backyard.",
                "facts": {"paw_prints": True, "crime_scene": "Kitchen Counter"},
                "reason": {"suspect": "Only Dog Bruno has paws — Ali and Sara have human feet"}
            },
            {
                "id": 2,
                "text": "The cake plate was found on the floor — not on the counter. It was knocked down, not carried.",
                "facts": {"cake_knocked": True},
                "reason": {"weapon": "Plate knocked off = dog behavior, not human"}
            },
            {
                "id": 3,
                "text": "Sister Sara was watching TV in the living room the entire time — Mom confirmed she never entered the kitchen.",
                "facts": {"sara_alibi": True},
                "reason": {"suspect": "Sara has confirmed alibi — she was not in the kitchen"}
            }
        ]
    },

    2: {
        "id": 2,
        "level": "fun",
        "difficulty": "Easy",
        "emoji": "📚",
        "title": "The Lost Homework Case",
        "location": "School Classroom 5B",
        "description": (
            "Hamza submitted his homework to the class monitor before recess. "
            "After recess, the homework was missing from the monitor's desk. "
            "The teacher is upset and Hamza could fail. Three classmates had "
            "access to the desk during recess."
        ),
        "quote": "A torn notebook page was found near the window, and there were ink marks on the desk...",
        "suspects": ["Classmate Omer", "Class Monitor Hira", "Classmate Sadia"],
        "suspect_roles": {
            "Classmate Omer":     "Sits next to monitor's desk, failed last assignment",
            "Class Monitor Hira": "Responsible for collecting homework",
            "Classmate Sadia":    "Best friend of Hamza, was nearby"
        },
        "locations": ["Monitor Desk", "Window Side", "Classroom Door", "Teacher Table"],
        "weapons":   ["Hid it in bag", "Threw it in bin", "Accidentally destroyed it"],
        "solution": {
            "culprit":  "Classmate Omer",
            "location": "Monitor Desk",
            "weapon":   "Hid it in bag"
        },

        # ── REAL AC-3 CONSTRAINTS ────────────────────────────────
        # Rule 1: if hira_verified → Hira impossible (she documented correctly)
        # Rule 2: if sadia_library → Sadia impossible (she left early)
        # Rule 3: if crime_scene known → only that location possible
        # Rule 4: if copy_motive → only hiding makes sense, not destroying
        "constraints": [
            ("suspect",
             lambda v, kb: not (kb.get("hira_verified") and v == "Class Monitor Hira")),
            ("suspect",
             lambda v, kb: not (kb.get("sadia_library") and v == "Classmate Sadia")),
            ("location",
             lambda v, kb: kb.get("crime_scene") is None or v == kb["crime_scene"]),
            ("weapon",
             lambda v, kb: not kb.get("copy_motive") or v == "Hid it in bag"),
        ],

        "clues": [
            {
                "id": 1,
                "text": "Hira the monitor kept a log — she recorded receiving Hamza's homework before recess. It was on the desk when recess started.",
                "facts": {"hira_verified": True},
                "reason": {"suspect": "Hira documented everything — she had no reason to take it"}
            },
            {
                "id": 2,
                "text": "Sadia left the classroom immediately after recess started — three students saw her go to the library.",
                "facts": {"sadia_library": True, "crime_scene": "Monitor Desk"},
                "reason": {"suspect": "Sadia was absent — no opportunity", "location": "Homework was at Monitor Desk"}
            },
            {
                "id": 3,
                "text": "Omer was seen near the monitor's desk during recess. He also failed the same assignment last week and needed to copy it.",
                "facts": {"copy_motive": True},
                "reason": {"weapon": "Copy motive means hiding — not destroying or discarding"}
            }
        ]
    },

    # ═══════════════════════════════════════════════════════════════
    #  CASE 3 — SERIOUS / MEDIUM
    #  MODE: Real AC-3
    #  Engine uses constraint rules to infer eliminations from facts.
    # ═══════════════════════════════════════════════════════════════

    3: {
        "id": 3,
        "level": "serious",
        "difficulty": "Medium",
        "emoji": "🏦",
        "title": "The Bank Transfer",
        "location": "HBL Branch, Lahore",
        "description": (
            "Rs. 50 million was secretly transferred from the main account at 11:47 PM. "
            "Only three employees had after-hours keycard access and system credentials that night. "
            "The transfer was traced back to an internal terminal."
        ),
        "quote": "The transfer was authorized using valid credentials — only an insider could have done this.",
        "suspects": ["Kamran Malik", "Sana Mirza", "Usman Qureshi"],
        "suspect_roles": {
            "Kamran Malik":  "Branch Manager",
            "Sana Mirza":    "IT Officer",
            "Usman Qureshi": "Senior Teller"
        },
        "locations": ["Server Room", "Manager Office", "Teller Counter", "CCTV Room"],
        "weapons":   ["Admin Password", "Keycard Override", "Insider Credentials"],
        "solution": {
            "culprit":  "Sana Mirza",
            "location": "Server Room",
            "weapon":   "Admin Password"
        },

        # ── REAL AC-3 CONSTRAINTS ────────────────────────────────
        # Rule 1: if usman_left_early → Usman impossible
        # Rule 2: if kamran_alibi → Kamran impossible
        # Rule 3: if crime_scene known → only that location possible
        # Rule 4: if admin_password_used → only Admin Password possible
        "constraints": [
            ("suspect",
             lambda v, kb: not (kb.get("usman_left_early") and v == "Usman Qureshi")),
            ("suspect",
             lambda v, kb: not (kb.get("kamran_alibi") and v == "Kamran Malik")),
            ("location",
             lambda v, kb: kb.get("crime_scene") is None or v == kb["crime_scene"]),
            ("weapon",
             lambda v, kb: not kb.get("admin_password_used") or v == "Admin Password"),
        ],

        "clues": [
            {
                "id": 1,
                "text": "CCTV footage shows Usman Qureshi left the building at 10:30 PM — one hour before the transfer.",
                "facts": {"usman_left_early": True},
                "reason": {"suspect": "Usman left before crime — physically impossible for him to do it"}
            },
            {
                "id": 2,
                "text": "The transfer originated from a terminal in the Server Room, not the Teller Counter or Manager Office.",
                "facts": {"crime_scene": "Server Room"},
                "reason": {"location": "Only Server Room terminal can authorize transactions"}
            },
            {
                "id": 3,
                "text": "Kamran Malik was on a video call with the regional director from 11:00 PM to midnight — call logs confirmed.",
                "facts": {"kamran_alibi": True},
                "reason": {"suspect": "Kamran has verified alibi for the entire crime window"}
            },
            {
                "id": 4,
                "text": "The CCTV Room terminal does not have transaction access — only the Server Room terminal does.",
                "facts": {},
                "reason": {}
            },
            {
                "id": 5,
                "text": "The transaction required Admin Password authentication — only the IT Officer holds this credential.",
                "facts": {"admin_password_used": True},
                "reason": {"weapon": "Admin Password required — only Sana Mirza (IT Officer) has it"}
            }
        ]
    },

    # ═══════════════════════════════════════════════════════════════
    #  CASES 4–7 — SERIOUS
    #  MODE: Simple Eliminates
    #  Clues directly list what to eliminate.
    #  Still CSP structure: variables, domains, propagation logged.
    # ═══════════════════════════════════════════════════════════════

    4: {
        "id": 4,
        "level": "serious",
        "difficulty": "Medium",
        "emoji": "🔬",
        "title": "The Stolen Research",
        "location": "NUST AI Lab, Islamabad",
        "description": (
            "Classified defense project data was copied and sent to a competitor company. "
            "The encryption key was used at 2:14 AM to access the files. "
            "Five researchers had access that night — one of their alibis is false."
        ),
        "quote": "Only three people had the decryption key — but all five were in the building that night.",
        "suspects": ["Dr. Ahmed Raza", "Aisha Nawaz", "Tariq Mehmood", "Zara Khan", "Hassan Iqbal"],
        "suspect_roles": {
            "Dr. Ahmed Raza":  "Lead Researcher",
            "Aisha Nawaz":     "Data Analyst",
            "Tariq Mehmood":   "Security Officer",
            "Zara Khan":       "Junior Researcher",
            "Hassan Iqbal":    "System Administrator"
        },
        "locations": ["Server Lab", "Conference Room", "Rooftop", "Parking", "Director Office"],
        "weapons":   ["Decryption Key", "Remote Access", "USB Drive"],
        "solution": {
            "culprit":  "Hassan Iqbal",
            "location": "Server Lab",
            "weapon":   "Remote Access"
        },
        "constraints": [],   # simple mode — no constraints needed
        "clues": [
            {
                "id": 1,
                "text": "Dr. Ahmed Raza was presenting at an online conference from midnight to 3 AM — 200 attendees confirm this.",
                "eliminates": {"suspects": ["Dr. Ahmed Raza"]},
                "propagation": "Dr. Ahmed Raza has a verified public alibi. Eliminated."
            },
            {
                "id": 2,
                "text": "Physical USB ports were disabled that night — data was accessed remotely from inside the building.",
                "eliminates": {"weapons": ["USB Drive"]},
                "propagation": "USB Drive eliminated. Weapon domain: Decryption Key, Remote Access."
            },
            {
                "id": 3,
                "text": "Tariq Mehmood's security badge shows he was in the Conference Room monitoring feeds all night.",
                "eliminates": {"suspects": ["Tariq Mehmood"], "locations": ["Conference Room", "Rooftop", "Parking"]},
                "propagation": "Tariq Mehmood eliminated. Remote non-lab locations ruled out."
            },
            {
                "id": 4,
                "text": "Aisha Nawaz does not have Remote Access credentials — only the System Administrator and Lead Researcher hold them.",
                "eliminates": {"suspects": ["Aisha Nawaz"]},
                "propagation": "Aisha Nawaz cannot use Remote Access. Eliminated. Remaining: Zara Khan, Hassan Iqbal."
            },
            {
                "id": 5,
                "text": "Zara Khan's decryption key was reported stolen two days ago — she filed a complaint with IT. She had no working key.",
                "eliminates": {"suspects": ["Zara Khan"]},
                "propagation": "Zara Khan had no valid credentials. Eliminated. Only Hassan Iqbal remains."
            },
            {
                "id": 6,
                "text": "Server Lab access logs show Hassan Iqbal's credentials used at 2:14 AM via remote session — he claimed he was asleep in the parking lot. The Decryption Key was never touched — only Remote Access was used.",
                "eliminates": {"locations": ["Director Office"], "weapons": ["Decryption Key"]},
                "propagation": "Location confirmed: Server Lab. Weapon confirmed: Remote Access. Hassan Iqbal's alibi is false."
            }
        ]
    },

    5: {
        "id": 5,
        "level": "serious",
        "difficulty": "Hard",
        "emoji": "🏢",
        "title": "The Corporate Sabotage",
        "location": "TechCorp Headquarters, Karachi",
        "description": (
            "Someone deliberately corrupted the product launch presentation and leaked "
            "investor contracts to a competitor the night before the Rs. 2 crore launch event. "
            "Only six people knew the CEO would be absent that night."
        ),
        "quote": "The sabotage required deep internal knowledge — someone who knew the schedules, the systems, and the secrets.",
        "suspects": ["Farhan Siddiqui", "Nadia Hussain", "Omar Sheikh", "Rabia Tariq", "Bilal Ahmed", "Sara Zafar"],
        "suspect_roles": {
            "Farhan Siddiqui": "Chief Technology Officer",
            "Nadia Hussain":   "Chief Financial Officer",
            "Omar Sheikh":     "Head of Marketing",
            "Rabia Tariq":     "Head of HR",
            "Bilal Ahmed":     "Senior Developer",
            "Sara Zafar":      "Executive Intern"
        },
        "locations": ["CEO Office", "Server Room", "Marketing Floor", "Conference Hall", "Rooftop"],
        "weapons":   ["Presentation Access", "Investor Database", "Admin Override"],
        "solution": {
            "culprit":  "Bilal Ahmed",
            "location": "Server Room",
            "weapon":   "Admin Override"
        },
        "constraints": [],
        "clues": [
            {
                "id": 1,
                "text": "The investor contracts were accessed through a developer-level admin override — not an executive account.",
                "eliminates": {"suspects": ["Farhan Siddiqui", "Nadia Hussain", "Omar Sheikh", "Rabia Tariq"]},
                "propagation": "Executive accounts not used. Only developer-level access fits. Four executives eliminated."
            },
            {
                "id": 2,
                "text": "Sara Zafar's intern account does not include server room entry permissions or admin override access.",
                "eliminates": {"suspects": ["Sara Zafar"]},
                "propagation": "Sara Zafar lacks required permissions. Eliminated. Only Bilal Ahmed remains."
            },
            {
                "id": 3,
                "text": "The corrupted files were modified from a terminal inside the Server Room only — other terminals lack this access.",
                "eliminates": {"locations": ["CEO Office", "Marketing Floor", "Conference Hall", "Rooftop"]},
                "propagation": "Location confirmed: Server Room."
            },
            {
                "id": 4,
                "text": "Both files were accessed using Admin Override — not standard login credentials.",
                "eliminates": {"weapons": ["Presentation Access", "Investor Database"]},
                "propagation": "Weapon confirmed: Admin Override. This matches Bilal Ahmed's developer access exactly."
            }
        ]
    },

    6: {
        "id": 6,
        "level": "serious",
        "difficulty": "Hard",
        "emoji": "🏥",
        "title": "The Hospital Poisoning",
        "location": "CMH Hospital, Rawalpindi",
        "description": (
            "A VIP patient was given a deliberate medication overdose during the night shift. "
            "The medication was switched between 2:15 AM and 3:00 AM. "
            "Seven people were in the ward — one had both motive and access."
        ),
        "quote": "The medication label was peeled off and replaced — someone planned this carefully.",
        "suspects": ["Dr. Imran Khalid", "Nurse Hina Baig", "Nurse Kamil Shah",
                     "Nurse Zoya Ahmed", "Pharmacist Rashid", "Ward Boy Saleem", "Visitor Unknown"],
        "suspect_roles": {
            "Dr. Imran Khalid":  "Night Shift Doctor",
            "Nurse Hina Baig":   "Head Nurse",
            "Nurse Kamil Shah":  "Ward Nurse",
            "Nurse Zoya Ahmed":  "Ward Nurse",
            "Pharmacist Rashid": "On-Call Pharmacist",
            "Ward Boy Saleem":   "Ward Boy",
            "Visitor Unknown":   "Unregistered Visitor"
        },
        "locations": ["Patient Room", "Medicine Storage", "Nurses Station", "Doctor Office", "Pharmacy"],
        "weapons":   ["Label Replacement", "Prescription Forgery", "Key Duplication"],
        "solution": {
            "culprit":  "Nurse Hina Baig",
            "location": "Medicine Storage",
            "weapon":   "Label Replacement"
        },
        "constraints": [],
        "clues": [
            {
                "id": 1,
                "text": "The visitor signed out at 2:00 AM — fifteen minutes before the medication switch window began.",
                "eliminates": {"suspects": ["Visitor Unknown"]},
                "propagation": "Visitor left before the crime window (2:15–3:00 AM). Eliminated."
            },
            {
                "id": 2,
                "text": "Ward Boy Saleem does not have a keycard for Medicine Storage — it requires a nurse or doctor credential.",
                "eliminates": {"suspects": ["Ward Boy Saleem"]},
                "propagation": "Ward Boy cannot access Medicine Storage. Eliminated."
            },
            {
                "id": 3,
                "text": "The medication label was physically replaced — not a prescription error. This rules out forgery and duplication.",
                "eliminates": {"weapons": ["Prescription Forgery", "Key Duplication"]},
                "propagation": "Weapon confirmed: Label Replacement. Requires direct physical access to Medicine Storage."
            },
            {
                "id": 4,
                "text": "Dr. Imran Khalid was performing emergency surgery from 2:00 AM to 4:00 AM — three doctors confirm this.",
                "eliminates": {"suspects": ["Dr. Imran Khalid"]},
                "propagation": "Dr. Imran Khalid has a confirmed alibi during the entire crime window. Eliminated."
            },
            {
                "id": 5,
                "text": "Pharmacist Rashid was locked inside the Pharmacy dispensing emergency medication — pharmacy logs confirm this.",
                "eliminates": {"suspects": ["Pharmacist Rashid"],
                               "locations": ["Doctor Office", "Pharmacy", "Nurses Station", "Patient Room"]},
                "propagation": "Pharmacist eliminated. Location narrowed to Medicine Storage only."
            },
            {
                "id": 6,
                "text": "Nurse Kamil Shah and Nurse Zoya Ahmed were stationed together at the Nurses Station all shift — confirmed by each other and security camera.",
                "eliminates": {"suspects": ["Nurse Kamil Shah", "Nurse Zoya Ahmed"]},
                "propagation": "Both nurses have mutual alibis and camera confirmation. Eliminated. Only Nurse Hina Baig remains."
            }
        ]
    },

    7: {
        "id": 7,
        "level": "serious",
        "difficulty": "Expert",
        "emoji": "⚖️",
        "title": "The Witness Disappearance",
        "location": "Pearl Continental Hotel, Lahore",
        "description": (
            "A key witness in a major corruption trial disappeared from his hotel room "
            "the night before testimony. No body was found — only a torn document and his phone. "
            "Eight people connected to the case were in or near the hotel that night."
        ),
        "quote": "The witness called his lawyer at 11:00 PM saying he was scared. After that — complete silence.",
        "suspects": ["Advocate Zubair", "Inspector Farooq", "Accused Relative Tariq",
                     "Accused Relative Mehwish", "Judge Assistant Bilal",
                     "Hotel Manager Asad", "Advocate Samina", "Driver Naseer"],
        "suspect_roles": {
            "Advocate Zubair":          "Defense Lawyer",
            "Inspector Farooq":         "Investigating Officer",
            "Accused Relative Tariq":   "Brother of Accused",
            "Accused Relative Mehwish": "Wife of Accused",
            "Judge Assistant Bilal":    "Court Assistant",
            "Hotel Manager Asad":       "Hotel Manager",
            "Advocate Samina":          "Prosecution Lawyer",
            "Driver Naseer":            "Witness Personal Driver"
        },
        "locations": ["Hotel Room 204", "Hotel Lobby", "Parking Basement", "Service Exit", "Rooftop"],
        "weapons":   ["Intimidation", "Bribery", "Forced Removal"],
        "solution": {
            "culprit":  "Inspector Farooq",
            "location": "Service Exit",
            "weapon":   "Forced Removal"
        },
        "constraints": [],
        "clues": [
            {
                "id": 1,
                "text": "Hotel CCTV shows Advocate Zubair and Advocate Samina left together at 10:30 PM and did not return.",
                "eliminates": {"suspects": ["Advocate Zubair", "Advocate Samina"]},
                "propagation": "Both advocates left before the disappearance window. Eliminated."
            },
            {
                "id": 2,
                "text": "Driver Naseer was found asleep in the parking basement — hotel staff confirm he never left his car all night.",
                "eliminates": {"suspects": ["Driver Naseer"], "locations": ["Rooftop", "Hotel Lobby"]},
                "propagation": "Driver Naseer eliminated. Rooftop and Lobby ruled out — full camera coverage there."
            },
            {
                "id": 3,
                "text": "Accused Relative Tariq and Mehwish were under police surveillance outside the hotel all night — logs confirmed.",
                "eliminates": {"suspects": ["Accused Relative Tariq", "Accused Relative Mehwish"]},
                "propagation": "Both accused relatives were under watch the entire night. Eliminated."
            },
            {
                "id": 4,
                "text": "Judge Assistant Bilal does not have the authority or resources to physically remove someone under witness protection.",
                "eliminates": {"suspects": ["Judge Assistant Bilal"], "weapons": ["Bribery", "Intimidation"]},
                "propagation": "Bilal eliminated. Intimidation and Bribery cannot explain a physical disappearance. Weapon: Forced Removal."
            },
            {
                "id": 5,
                "text": "Hotel Manager Asad's master keycard was not used that night — room 204 was not accessed through his credentials.",
                "eliminates": {"suspects": ["Hotel Manager Asad"], "locations": ["Hotel Room 204", "Parking Basement"]},
                "propagation": "Hotel Manager Asad eliminated. Room 204 and Parking ruled out. Location: Service Exit."
            },
            {
                "id": 6,
                "text": "Inspector Farooq was the only one with police authority, knowledge of the witness protection detail, and access to the Service Exit blind spot.",
                "eliminates": {},
                "propagation": "All other suspects eliminated. Inspector Farooq is the only one with means, motive, and access. Case solved."
            }
        ]
    }
}
