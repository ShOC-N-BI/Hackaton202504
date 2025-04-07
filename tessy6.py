import re

air_enemy = ["UAV", "BOGEY", "BANDIT", "BANZAI",
    "BANDIT", "BOGEY", "BOGEY DOPE", "BLOW THROUGH", "BLOODHOUND", "BRACKET", 
    "BREAK (DIRECTION)", "BREAKAWAY", "BINGO", "BREVITY", "BRUISER", "BUGOUT", "BUSTER", "MIG-21", "MIG-15", "MIG-17", "MIG-19", "MIG-23", "MIG-25", "MIG-29", "MIG-31",
    "SU-7", "SU-9", "SU-11", "SU-15", "SU-17", "SU-20", "SU-22", "SU-24", "SU-25",
    "SU-27", "SU-30", "SU-33", "SU-35", "SU-57", "YAK-9", "YAK-23", "YAK-25", "YAK-28",
    "YAK-38", "YAK-41", "J-16", "J-8"
]

surface = ["DESTROYER", "DD", "FRIGATE", "FF", "CRUISER", "CC", "SUBMARINE", "SUB", "CARRIER", "CV", "BANZAI", "BRACKET", "BUMP/BUMP-UP", "BURN GLINT", "BUSTER", "BLANK", 
    "BULLDOG", "BREVITY", "BANDIT", "BOGEY", "BASSETT", "BRUISER", "BULLDOG", "COBRA", "COWBOYS", 
    "CYCLOPS", "DEADEYE", "JASSM", "ATTACK", "AAV", "DDG"
]

intel = ["RADIO", "EMISSION", "EMISSIONS", "BLUR", "AUTOCAT", "BEAM RIDER"]

cyber = ["FORWARD LOOKUP", "REQUEST", "ALLIGATOR", "NETWORK", "TRAFFIC"]

civilian = [
    "CIVILIAN", "CIV", "NON-COMBATANT", "NON-HOSTILE", "HUMANITARIAN", "REFUGEE", "CIVILIAN AREA", "HUMANITARIAN MISSION", "COMMERCIAL", "COMMERCIAL VESSEL", "COMMERCIAL PLANE", "COMMERCIAL A/C"
]

# Sample message to process
message = "[10:48:58] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) 2x J-16s were observed on EO/IR Imagery located on parking apron forward of aircraft hangers IVO 25.045310306035184, -77.464458773165 in Lane Flamingo"
#message = "[10:48:58] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) 2x j-16s were Yak-28s on UAV Imagery jassm  carrier on aav apron forward J-8 aircraft CV commercial vessel 25.045310306035184, -77.464458773165 in Lane Flamingo"
def action_prompt(entity_type, entity, description=""):
    if description:
        print(f"  Description: {description}")

    # print(f"  Actions you can take for {entity_type} '{entity}':")
    # Different actions 
    if entity in air_enemy:
        actions = ["Jam", "Attack", "Investigate", "Communicate"]
    elif entity in surface:
        actions = ["Jam", "Attack", "Investigate", "Communicate"]
    elif entity in intel:
        actions = ["Jam", "Communicate", "Investigate"]
    elif entity in cyber:
        actions = ["Jam", "Hack", "Counter"]
    elif entity in civilian:
        actions = ["Monitor", "Investigate", "Communicate", "Protect"]
    else:
        actions = ["Investigate", "Communicate", "", ""]

    print(f"  Actions for {entity}: {', '.join(actions)}")
    
    # default action
    chosen_action = actions[0]
    
    print(f"  Action for {entity}: {chosen_action}")
    return chosen_action


def extracted_chat(message):
    # Convert the message to uppercase 
    message_upper = message.upper()  

    # Find second ')' character
    first_parenthesis_pos = message_upper.find(')') 
    second_parenthesis_pos = message_upper.find(')', first_parenthesis_pos + 1)
    
    # Extract the text after second '('
    if second_parenthesis_pos != -1:
        text_second_parenthesis = message_upper[second_parenthesis_pos + 1:]  # Everything after the second ')'
        
        # Split the message into words
        words = text_second_parenthesis.split()

        # Lists to hold found words 
        found_air = []
        found_intel = []
        found_cyber = []
        found_surface = []
        found_civilian = []

        for i, word in enumerate(words):
            # Clean up the word by keeping only alphanumeric characters or hyphens and make it uppercase
            filtered_word = ''.join(e for e in word if e.isalnum() or e == '-').upper()

            # Remove the 's' at the end for singular match (if any)
            filtered_s = filtered_word.rstrip('S')

            # Check the word against all categories 
            if filtered_s in air_enemy:  
                found_air.append(filtered_s)
                description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
                print(f"Found Aircraft: {filtered_s}")
                action_prompt("Air Enemy", filtered_s, description)

            elif filtered_s in surface:  
                found_surface.append(filtered_s)
                description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
                print(f"Found Surface enemy: {filtered_s}")
                action_prompt("Surface Enemy", filtered_s, description)

            elif filtered_s in intel:  
                found_intel.append(filtered_s)
                description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
                print(f"Found enemy Intel: {filtered_s}")
                action_prompt("Intel", filtered_s, description)
                
            elif filtered_s in cyber:  
                found_cyber.append(filtered_s)
                description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
                print(f"Found enemy Cyber: {filtered_s}")
                action_prompt("Cyber", filtered_s, description)

            elif filtered_s in civilian:
                found_civilian.append(filtered_s)
                description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
                print(f"Found Civilian: {filtered_s}")
                action_prompt("Civilian", filtered_s, description)
        
        # Output the results               
        return found_air, found_surface, found_intel, found_cyber, found_civilian

    return [], [], [], [], []  # Return empty lists if no valid second parenthesis

# Sample Test
found_air, found_surface, found_intel, found_cyber, found_civilian = extracted_chat(message)
