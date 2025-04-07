import re

# Sample lists (could be extended)
air_enemy = ["UAV", "BOGEY", "BANDIT", "BANZAI", "MIG-21", "MIG-15", "MIG-17", "MIG-19", "MIG-23", "MIG-25", "MIG-29", "MIG-31",
    "SU-7", "SU-9", "SU-11", "SU-15", "SU-17", "SU-20", "SU-22", "SU-24", "SU-25",
    "SU-27", "SU-30", "SU-33", "SU-35", "SU-57", "YAK-9", "YAK-23", "YAK-25", "YAK-28",
    "J-16", "J-50", "J-36", "J-35", "J-20", "J-15", "J-10B", "J-11B", "J-10", "FC-1", 
    "JH-7", "Su-30MK2", "Su-30MKK", "Su-35S", "J-11D", "J-13", "J-12", "J-11", "J-9", 
    "J-8", "J-7", "J-6", "J-5", "J-2", "MiG-9", "Q-5", "Q-6", "J-16D", "J-15D", 
    "H-20", "H-8", "H-7", "H-6", "ZDK03", "Y-8", "KJ-200", "YY-20", "HY-6", "Il-78", "IL-76"]

surface = ["DESTROYER", "DD", "FRIGATE", "FF", "CRUISER", "CC", "SUBMARINE", "SUB", "CARRIER", "CV", "BANZAI", "BRACKET", "BUMP/BUMP-UP", "BURN GLINT", "BUSTER", "BLANK"]

intel = ["RADIO", "EMISSION", "EMISSIONS", "BLUR", "AUTOCAT", "BEAM RIDER", "CTTN"]

cyber = ["FORWARD LOOKUP", "REQUEST", "ALLIGATOR", "NETWORK", "TRAFFIC"]

civilian = [
    "CIVILIAN", "CIV", "NON-COMBATANT", "NON-HOSTILE", "HUMANITARIAN", "REFUGEE", "CIVILIAN AREA", "HUMANITARIAN MISSION", "COMMERCIAL", "COMMERCIAL VESSEL", "COMMERCIAL PLANE", "COMMERCIAL A/C"]

def action_prompt(entity, description=""):
    # Different actions
    if entity in air_enemy:
        actions = ["Attack", "Investigate", "Communicate"]
    elif entity in surface:
        actions = ["Attack", "Investigate", "Communicate"]
    elif entity in intel:
        actions = ["Jam", "Communicate", "Investigate"]
    elif entity in cyber:
        actions = ["Jam", "Hack", "Counter"]
    elif entity in civilian:
        actions = ["Monitor", "Investigate", "Communicate"]
    else:
        return entity, "None", "None", "None"
    
    action1, action2, action3 = actions[0], actions[1], actions[2]
    return entity, action1, action2, action3

def extracted_chat(message):
    # Initialize default values
    entity = action1 = action2 = action3 = None

    # Convert to uppercase for consistency
    message_upper = message.upper()

    # Find second ')' character to get message content after it
    first_parenthesis_pos = message_upper.find(')')
    second_parenthesis_pos = message_upper.find(')', first_parenthesis_pos + 1)
    
    if second_parenthesis_pos != -1:
        text_second_parenthesis = message_upper[second_parenthesis_pos + 1:]

        # Use regex to capture relevant terms, considering possible entity format
        # Updated regex to better capture terms like J-16, J-16s, YAK-28
        words = re.findall(r'\b([A-Z0-9\-]+(?:S)?)\b', text_second_parenthesis)  # Match singular and plural forms

        # Process each word to identify and act on entities
        for word in words:
            filtered_word = word.upper()

            # Handle singular/plural matching more robustly (handle both singular and plural)
            if filtered_word in air_enemy or filtered_word[:-1] in air_enemy:  # Also check without the plural 's'
                entity, action1, action2, action3 = action_prompt(filtered_word)
                print(f"Found Air Enemy: {filtered_word}")
                break  # Stop once we find the first match
            elif filtered_word in surface or filtered_word[:-1] in surface:
                entity, action1, action2, action3 = action_prompt(filtered_word)
                print(f"Found Surface Entity: {filtered_word}")
                break
            elif filtered_word in intel or filtered_word[:-1] in intel:
                entity, action1, action2, action3 = action_prompt(filtered_word)
                print(f"Found Intel Entity: {filtered_word}")
                break
            elif filtered_word in cyber or filtered_word[:-1] in cyber:
                entity, action1, action2, action3 = action_prompt(filtered_word)
                print(f"Found Cyber Entity: {filtered_word}")
                break
            elif filtered_word in civilian or filtered_word[:-1] in civilian:
                entity, action1, action2, action3 = action_prompt(filtered_word)
                print(f"Found Civilian: {filtered_word}")
                break
    
    # Return entity and actions if no entity is found
    print(f"Entity: {entity}")
    print(f"Actions: {action1}, {action2}, {action3}")
    return entity, action1, action2, action3

# Test case
message = "[10:48:58] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) 2x j-16s were Yak-28s on UAV Imagery jassm carrier on aav apron forward J-8 aircraft CV commercial vessel 25.045310306035184, -77.464458773165 in Lane Flamingo"
extracted_chat(message)
