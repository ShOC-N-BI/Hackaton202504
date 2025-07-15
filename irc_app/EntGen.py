import re
import json
import sys

air_enemy = ["UAV", "BOGEY", "BANDIT", "BANZAI",
    "BANDIT", "BOGEY", "BOGEY DOPE", "BLOW THROUGH", "BLOODHOUND", "BRACKET", 
    "BREAK (DIRECTION)", "BREAKAWAY", "BINGO", "BREVITY", "BRUISER", "BUGOUT", "BUSTER", "MIG-21", "MIG-15", "MIG-17", "MIG-19", "MIG-23", "MIG-25", "MIG-29", "MIG-31",
    "SU-7", "SU-9", "SU-11", "SU-15", "SU-17", "SU-20", "SU-22", "SU-24", "SU-25",
    "SU-27", "SU-30", "SU-33", "SU-35", "SU-57", "YAK-9", "YAK-23", "YAK-25", "YAK-28",
    "YAK-38", "YAK-41", "J-16", "J-50", "J-36", "J-35", "J-20", "J-15", "J-16", "J-10B", "J-11B", "J-10", "FC-1", 
    "JH-7", "Su-30MK2", "Su-30MKK", "Su-35S", "J-11D", "J-13", "J-12", "J-11", "J-9", 
    "J-8", "J-7", "J-6", "J-5", "J-2", "MiG-9", "Su-27", "Q-5", "Q-6", "J-16D", "J-15D", 
    "H-20", "H-8", "H-7", "H-6", "H-5", "Tu-14", "Tu-2", "KJ-600", "KJ-500", "KJ-2000", 
    "Y-9JZ ELINT", "Y-8CB", "Y-8DZ", "Y-8G", "Y-8GX3", "Y-8JB", "Y-8T", "Y-8W", "Y-8EW", 
    "ZDK03", "Y-8J", "KJ-200", "Y-7", "KJ-1 AEWC", "An-30", "CIOMP", 
    "YY-20", "HY-6", "Il-78", "JZ-8", "JZ-7", "MIG-29", "MIG-31", "MIG-35", "SU-27", "SU-30", "SU-34", "SU-35", "SU-57", 
    "SU-24", "SU-25", "MI-8", "MI-24", "MI-28", "KA-52", "KA-60", "ANSAT", 
    "PANTHER", "IL-76", "IL-78", "IL-112", "IL-214", "AN-26", "AN-72", 
    "BE-200", "TU-22M", "TU-160", "TU-95", "B-2", "S-400", "T-50", "T-14", 
    "AWACS", "AIRCRAFT", "HELICOPTER", "HELO", "BOMBER", "BOMBERS", "FIGHTER", "FIGHTERS", "A/C", "AIRCRAFTS",
    "MIG21", "MIG15", "MIG17", "MIG19", "MIG23", "MIG25", "MIG29", "MIG31",
    "SU7", "SU9", "SU11", "SU15", "SU17", "SU20", "SU22", "SU24", "SU25",
    "SU27", "SU30", "SU33", "SU35", "SU57", "YAK9", "YAK23", "YAK25", "YAK28",
    "YAK38", "YAK41", "J16", "J50", "J36", "J35", "J20", "J15", "J16", "J10B", "J11B", "J10", "FC1", 
    "JH7", "Su30MK2", "Su30MKK", "Su35S", "J11D", "J13", "J12", "J11", "J9", 
    "J8", "J7", "J6", "J5", "J2", "MiG9", "Su27", "Q5", "Q6", "J16D", "J15D", 
    "H20", "H8", "H7", "H6", "H5", "Tu14", "Tu2", "KJ600", "KJ500", "KJ2000", 
    "Y9JZ ELINT", "Y8CB", "Y8DZ", "Y8G", "Y8GX3", "Y8JB", "Y8T", "Y8W", "Y8EW", 
    "ZDK03", "Y8J", "KJ200", "Y7", "KJ1 AEWC", "An30",
    "YY20", "HY6", "Il78", "JZ8", "JZ7", "MIG29", "MIG31", "MIG35", "SU27", "SU30", "SU34", "SU35", "SU57", 
    "SU24", "SU25", "MI8", "MI24", "MI28", "KA52", "KA60", "IL76", "IL78", "IL112", "IL214", "AN26", "AN72", 
    "BE200", "TU22M", "TU160", "TU95", "B2", "S400", "T50", "T14"
]

surface = ["DESTROYER", "DD", "FRIGATE", "FF", "CRUISER", "CC", "SUBMARINE", "SUB", 
    "CARRIER", "CV", "BANZAI", "BRACKET", "BUMP/BUMP-UP", "BURN-GLINT", "BUSTER", 
    "BLANK", "BULLDOG", "BREVITY", "BANDIT", "BOGEY", "BASSETT", "BRUISER", "COBRA", 
    "COWBOYS", "CYCLOPS", "DEADEYE", "JASSM", "ATTACK", "AAV", "DDG", "CVN", "CG", 
    "LHD", "LPD", "LCS", "SSN", "SSBN", "LHA", "T-AKE", "AOR", "LST", "T-AO", "FFG", 
    "RADAR", "VESSEL", "SHIP", "BB", "CA", "SSGN", "LSD", "AO", "AE", "AK", "AR", "PC", 
    "PY", "MCM", "MSC", "AIRCRAFT-CARRIER", "NUCLEAR-POWERED-AIRCRAFT-CARRIER", "BATTLESHIP", 
    "HEAVY-CRUISER", "GUIDED-MISSILE-CRUISER", "DESTROYER", "GUIDED-MISSILE-DESTROYER", 
    "FRIGATE", "GUIDED-MISSILE-FRIGATE", "SUBMARINE-(DIESEL-ELECTRIC)", 
    "NUCLEAR-POWERED-SUBMARINE-(ATTACK)", "NUCLEAR-POWERED-BALLISTIC-MISSILE-SUBMARINE", 
    "NUCLEAR-POWERED-GUIDED-MISSILE-SUBMARINE", "AMPHIBIOUS-ASSAULT-SHIP", 
    "AMPHIBIOUS-ASSAULT-SHIP-(DIFFERENT-CONFIGURATION)", "AMPHIBIOUS-TRANSPORT-DOCK", 
    "LANDING-SHIP-TANK", "DOCK-LANDING-SHIP", "FLEET-OILER", "AMMUNITION-SHIP", 
    "CARGO-SHIP", "REPAIR-SHIP", "PATROL-CRAFT", "PATROL-YACHT", 
    "MINE-COUNTERMEASURES-SHIP", "MINESWEEPER-COMMAND-SHIP"

]
Incoming = ["MISSILE", "ROCKET", "TORPEDO", "BOMB", "TORP", "CRUISE", "BALLISTIC","LAUNCHED", "LAUNCH", "FIRE", "ENGAGED",
             "ANTI-SHIP MISSILE", "ASW", "AAM", "AGM", "A/S", "A/G", "A/A", "A/T", "A/D", "A/P", "A/L",
               "SURFACE-TO-AIR", "CRUISE-MISSILE","CRUISE",
    "BALLISTIC-MISSILE",
    "ANTI-SHIP-MISSILE",
    "ANTI-AIR-MISSILE",
    "AIR-TO-GROUND-MISSILE",
    "SURFACE-TO-AIR-MISSILE",
    "SURFACE-TO-SURFACE-MISSILE",
    "LAND-ATTACK-CRUISE-MISSILE",
    "SUBMARINE-LAUNCHED-CRUISE-MISSILE",
    "SUBMARINE-LAUNCHED-BALLISTIC-MISSILE",
    "SUBMARINE-LAUNCHED-ANTI-SHIP-MISSILE",
    "SUBMARINE-LAUNCHED-LAND-ATTACK-CRUISE-MISSILE"
    "SUBMARINE-LAUNCHED-ANTI-AIR-MISSILE"
    ]

intel = ["RADIO", "EMISSION", "EMISSIONS", "BLUR", "AUTOCAT", "BEAM RIDER","CTTN","RADAR","NOISE","SIGNAL","JAMMING"]

cyber = ["FORWARD LOOKUP", "REQUEST", "ALLIGATOR", "NETWORK", "TRAFFIC"]

civilian = [
    "CIVILIAN", "CIV", "NON-COMBATANT", "NON-HOSTILE", "HUMANITARIAN", "REFUGEE", "CIVILIAN-AREA", "HUMANITARIAN-MISSION", "COMMERCIAL", "COMMERCIAL-VESSEL", "COMMERCIAL-PLANE", "COMMERCIAL A/C"
]
enem = ["ENEMY", "HOSTILE", "THREAT", "TARGET","ADVERSARY", "OPFOR", "OPPOSITION", "FOE", "RIVAL", "AGGRESSOR", "ANTAGONIST", "BANDIT", "BOGEY"]

rando = ["RANDOM", "UNKNOWN", "UNK", "UNIDENTIFIED", "UNCONFIRMED", "UNCERTAIN", "POTENTIAL"]
out =["SWIM","BEER"]
#message = "[10:48:58] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) 2x Torpedo were observed on EO/IR Imagery located on parking apron forward of aircraft hangers IVO 25.045310306035184, -77.464458773165 in Lane Flamingo"
#message = "[11:00:11] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) From 1205Z to 2111Z Radio emmission were detected at location  27.689097938330395, -80.38238737940404 operating on VHF. in Lane Bellagio"
#message = "[10:45:02] WF_Clark: Floater03_OPS (USS Cole DDG): @Maritime_OPS (Maritime Operations Center) Possible helos swarm approaching from south, type unk.  Main generator still inop, drifting WNW at 5 knots, req support in Lane Ceasars"
# extracted_chat(message)
# message = "[10:48:58] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) 2x J-16s were observed on EO/IR Imagery located on parking apron forward of aircraft hangers IVO 25.045310306035184, -77.464458773165 in Lane Flamingo"
#message = "[11:22:33] WF_FYST: IntelOps: @ Hydro_MSO, TN 44993/94/95/96 are all 1x J-15 each track."
# def get_description(words, index, max_words=5):
#     description = ' '.join(words[index+1:index+max_words]) if index + max_words <= len(words) else ' '.join(words[index+1:])

# === CLASSIFICATION FUNCTION ===
def classify_entity(word):
    if word in air_enemy:
        return "air"
    elif word in Incoming:
        return "incoming"
    elif word in surface:
        return "surface"
    elif word in intel:
        return "intel"
    elif word in cyber:
        return "cyber"
    elif word in civilian:
        return "civilian"
    elif word in enem:
        return "enem"
    elif word in rando:
        return "rando"
    elif word in out:
        return "out"
    return None

# === ENTITY EXTRACTION ===
def extract_and_classify_entities(message):
    message_upper = message.upper()
    words = message_upper.split()

    observed_entities = []

    for i, word in enumerate(words):
        word_clean = re.sub(r'[^\w\-]', '', word).rstrip('S')

        entity_type = classify_entity(word_clean)
        if entity_type:
            entity = {}
            entity["desc"] = word_clean
            entity["type"] = entity_type
            entity["affiliation"] = "unknown"

            # Count detection
            if i > 0 and re.match(r'\d+X', words[i - 1]):
                entity["count"] = int(words[i - 1][:-1])
            else:
                entity["count"] = 1

            # Location extraction
            latlon_matches = re.findall(r"(-?\d{1,3}\.\d+),\s*(-?\d{1,3}\.\d+)", message)
            if latlon_matches:
                lat, lon = latlon_matches[0]
                entity["location"] = [float(lat), float(lon)]
            else:
                entity["location"] = None

            # Direction parsing
            directions = []
            dir_keywords = ["NORTH", "SOUTH", "EAST", "WEST", "N", "S", "E", "W", "NE", "NW", "SE", "SW"]
            context = ' '.join(words[max(0, i - 500):i + 500])
            for d in dir_keywords:
                if re.search(r'\b{}\b'.format(re.escape(d)), context):
                    directions.append(d)
            directions = list(set(directions))
            entity["direction"] = ' '.join(directions) if directions else "unknown"

            observed_entities.append(entity)
            break  # Stop at first match for now

    return {"observed_entities": observed_entities}

# === MAIN (TERMINAL EXECUTION) ===
if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python app.py \"<message text>\"")
        sys.exit(1)

    message_input = sys.argv[1]
    result = extract_and_classify_entities(message_input)
    print(json.dumps(result, indent=2))


# Testing Json
# python irc_app/EntGen.py "[10:48:58] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) 500x BEERs were observed on EO/IR Imagery located on parking apron forward of aircraft hangers IVO 25.045310306035184, -77.464458773165 in Lane Flamingo Heading SW"
