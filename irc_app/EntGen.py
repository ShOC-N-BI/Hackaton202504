# import re

# air_enemy = ["UAV", "BOGEY", "BANDIT", "BANZAI",
#     "BANDIT", "BOGEY", "BOGEY DOPE", "BLOW THROUGH", "BLOODHOUND", "BRACKET", 
#     "BREAK (DIRECTION)", "BREAKAWAY", "BINGO", "BREVITY", "BRUISER", "BUGOUT", "BUSTER", "MIG-21", "MIG-15", "MIG-17", "MIG-19", "MIG-23", "MIG-25", "MIG-29", "MIG-31",
#     "SU-7", "SU-9", "SU-11", "SU-15", "SU-17", "SU-20", "SU-22", "SU-24", "SU-25",
#     "SU-27", "SU-30", "SU-33", "SU-35", "SU-57", "YAK-9", "YAK-23", "YAK-25", "YAK-28",
#     "YAK-38", "YAK-41", "J-16", "J-50", "J-36", "J-35", "J-20", "J-15", "J-16", "J-10B", "J-11B", "J-10", "FC-1", 
#     "JH-7", "Su-30MK2", "Su-30MKK", "Su-35S", "J-11D", "J-13", "J-12", "J-11", "J-9", 
#     "J-8", "J-7", "J-6", "J-5", "J-2", "MiG-9", "Su-27", "Q-5", "Q-6", "J-16D", "J-15D", 
#     "H-20", "H-8", "H-7", "H-6", "H-5", "Tu-14", "Tu-2", "KJ-600", "KJ-500", "KJ-2000", 
#     "Y-9JZ ELINT", "Y-8CB", "Y-8DZ", "Y-8G", "Y-8GX3", "Y-8JB", "Y-8T", "Y-8W", "Y-8EW", 
#     "ZDK03", "Y-8J", "KJ-200", "Y-7", "KJ-1 AEWC", "An-30", "CIOMP", 
#     "YY-20", "HY-6", "Il-78", "JZ-8", "JZ-7", "MIG-29", "MIG-31", "MIG-35", "SU-27", "SU-30", "SU-34", "SU-35", "SU-57", 
#     "SU-24", "SU-25", "MI-8", "MI-24", "MI-28", "KA-52", "KA-60", "ANSAT", 
#     "PANTHER", "IL-76", "IL-78", "IL-112", "IL-214", "AN-26", "AN-72", 
#     "BE-200", "TU-22M", "TU-160", "TU-95", "B-2", "S-400", "T-50", "T-14", "AWACS"
# ]

# surface = ["DESTROYER", "DD", "FRIGATE", "FF", "CRUISER", "CC", "SUBMARINE", "SUB", "CARRIER", "CV", "BANZAI", "BRACKET", "BUMP/BUMP-UP", "BURN GLINT", "BUSTER", "BLANK", 
#     "BULLDOG", "BREVITY", "BANDIT", "BOGEY", "BASSETT", "BRUISER", "BULLDOG", "COBRA", "COWBOYS", 
#     "CYCLOPS", "DEADEYE", "JASSM", "ATTACK", "AAV", "DDG", "CVN", "DDG", "CG", "LHD", "LPD", "LCS", "SSN", "SSBN", 
#     "LHA", "T-AKE", "AOR", "LST", "T-AO"
# ]

# intel = ["RADIO", "EMISSION", "EMISSIONS", "BLUR", "AUTOCAT", "BEAM RIDER","CTTN"]

# cyber = ["FORWARD LOOKUP", "REQUEST", "ALLIGATOR", "NETWORK", "TRAFFIC"]

# civilian = [
#     "CIVILIAN", "CIV", "NON-COMBATANT", "NON-HOSTILE", "HUMANITARIAN", "REFUGEE", "CIVILIAN AREA", "HUMANITARIAN MISSION", "COMMERCIAL", "COMMERCIAL VESSEL", "COMMERCIAL PLANE", "COMMERCIAL A/C"
# ]

# # Sample message to process
# #message = "[10:48:58] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) 2x J-16s were observed on EO/IR Imagery located on parking apron forward of aircraft hangers IVO 25.045310306035184, -77.464458773165 in Lane Flamingo"
# #message = "[10:48:58] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) 2x j-16s were Yak-28s on UAV Imagery jassm  carrier on aav apron forward J-8 aircraft CV commercial vessel 25.045310306035184, -77.464458773165 in Lane Flamingo"
# # message = "[10:59:16] Hydro_MSO: Intel,, Radio color tN 44840/41"
# # extracted_chat(message)

# def action_prompt(entity, description=""):
#     if description:
#         print(f"  Description: {description}")

#     # Different actions
#     if entity in air_enemy:
#         actions = ["Attack", "Investigate", "Communicate"]
#     elif entity in surface:
#         actions = ["Attack", "Investigate", "Communicate"]
#     elif entity in intel:
#         actions = ["Jam", "Communicate", "Investigate"]
#     elif entity in cyber:
#         actions = ["Jam", "Hack", "Counter"]
#     elif entity in civilian:
#         actions = ["Monitor", "Investigate", "Communicate"]
#     else:
#         actions = ["Investigate", "Communicate", "Ignore"]

#     # Printing actions separately
#     # print(f"  Actions for {entity}:")
#     for idx, action in enumerate(actions, 1):
#         print(f"{idx}. {action}")
    
#     return actions


# def extracted_chat(message):
#     # Convert the message to uppercase 
#     message_upper = message.upper()  

#     # Find second ')' character
#     first_parenthesis_pos = message_upper.find(')') 
#     second_parenthesis_pos = message_upper.find(')', first_parenthesis_pos + 1)
    
#     # Extract the text after second ')'
#     if second_parenthesis_pos != -1:
#         text_second_parenthesis = message_upper[second_parenthesis_pos + 1:]  # Everything after the second ')'
        
#         # Split the message into words
#         words = text_second_parenthesis.split()

#         # Lists to hold found words 
#         found_air = []
#         found_intel = []
#         found_cyber = []
#         found_surface = []
#         found_civilian = []

#         for i, word in enumerate(words):
#             # Clean up the word by keeping only alphanumeric characters or hyphens and make it uppercase
#             filtered_word = ''.join(e for e in word if e.isalnum() or e == '-').upper()

#             # Remove the 's' at the end for singular match
#             filtered_s = filtered_word.rstrip('S')
#             # Check the word against all categories 
#             if filtered_s in air_enemy:  
#                 found_air.append(filtered_s)
#                 # description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
#                 print(f"Found enemy Aircraft: {filtered_s}")
#                 # action_prompt("Air Enemy", filtered_s, description)
#                 action_prompt(filtered_s)

#             elif filtered_s in surface:  
#                 found_surface.append(filtered_s)
#                 # description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
#                 print(f"Found Surface enemy: {filtered_s}")
#                 # action_prompt("Surface Enemy", filtered_s, description)
#                 action_prompt(filtered_s)

#             elif filtered_s in intel:  
#                 found_intel.append(filtered_s)
#                 # description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
#                 print(f"Found enemy Intel: {filtered_s}")
#                 # action_prompt("Intel", filtered_s, description)
#                 action_prompt(filtered_s)

#             elif filtered_s in cyber:  
#                 found_cyber.append(filtered_s)
#                 # description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
#                 print(f"Found enemy Cyber: {filtered_s}")
#                 # action_prompt("Cyber", filtered_s, description)
#                 action_prompt(filtered_s)

#             elif filtered_s in civilian:
#                 found_civilian.append(filtered_s)
#                 # description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
#                 print(f"Found Civilian: {filtered_s}")
#                 # action_prompt("Civilian", filtered_s, description)
#                 action_prompt(filtered_s)
    
    
#     # insert code here may?                   
#     print(entity)
#     print(action1)
#     print(action2)
#     print(action3)
#     return entity, action1, action2, action3

import re


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
    "BE-200", "TU-22M", "TU-160", "TU-95", "B-2", "S-400", "T-50", "T-14", "AWACS"
]

surface = ["DESTROYER", "DD", "FRIGATE", "FF", "CRUISER", "CC", "SUBMARINE", "SUB", "CARRIER", "CV", "BANZAI", "BRACKET", "BUMP/BUMP-UP", "BURN GLINT", "BUSTER", "BLANK", 
    "BULLDOG", "BREVITY", "BANDIT", "BOGEY", "BASSETT", "BRUISER", "BULLDOG", "COBRA", "COWBOYS", 
    "CYCLOPS", "DEADEYE", "JASSM", "ATTACK", "AAV", "DDG", "CVN", "DDG", "CG", "LHD", "LPD", "LCS", "SSN", "SSBN", 
    "LHA", "T-AKE", "AOR", "LST", "T-AO"
]

intel = ["RADIO", "EMISSION", "EMISSIONS", "BLUR", "AUTOCAT", "BEAM RIDER","CTTN"]

cyber = ["FORWARD LOOKUP", "REQUEST", "ALLIGATOR", "NETWORK", "TRAFFIC"]

civilian = [
    "CIVILIAN", "CIV", "NON-COMBATANT", "NON-HOSTILE", "HUMANITARIAN", "REFUGEE", "CIVILIAN AREA", "HUMANITARIAN MISSION", "COMMERCIAL", "COMMERCIAL VESSEL", "COMMERCIAL PLANE", "COMMERCIAL A/C"
]

# Sample message to process
#message = "[10:48:58] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) 2x J-16s were observed on EO/IR Imagery located on parking apron forward of aircraft hangers IVO 25.045310306035184, -77.464458773165 in Lane Flamingo"
message = "[10:48:58] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) 2x j-16s were Yak-28s on UAV Imagery jassm  carrier on aav apron forward J-8 aircraft CV commercial vessel 25.045310306035184, -77.464458773165 in Lane Flamingo"
# message = "[10:59:16] Hydro_MSO: Intel,, Radio color tN 44840/41"
# extracted_chat(message)
#message = "[10:48:58] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) 2x J-16s were observed on EO/IR Imagery located on parking apron forward of aircraft hangers IVO 25.045310306035184, -77.464458773165 in Lane Flamingo"
def action_prompt(entity, description=""):
    if description:
        print(f"  Description: {description}")

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
        actions = ["Investigate", "Communicate", "Ignore"]

    # Printing actions separately
    # print(f"  Actions for {entity}:")
    # for idx, action in enumerate(actions, 1):
    #     print(f"{idx}. {action}")
    
    return actions


def extracted_chat(message):
    # Convert the message to uppercase 
    message_upper = message.upper()  

    # Find second ')' character
    first_parenthesis_pos = message_upper.find(')') 
    second_parenthesis_pos = message_upper.find(')', first_parenthesis_pos + 1)
    
    # Extract the text after second ')'
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

            # Remove the 's' at the end for singular match
            filtered_s = filtered_word.rstrip('S')
            # Check the word against all categories 
            if filtered_s in air_enemy:  
                found_air.append(filtered_s)
                # description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
                # print(f"Found enemy Aircraft: {filtered_s}")
                # action_prompt("Air Enemy", filtered_s, description)
                actions = action_prompt(filtered_s)  # Get actions for entity
                action1, action2, action3 = actions[:3]  # top3 actions
                # print(f"Found enemy Aircraft: {filtered_s}")
                return filtered_s, action1, action2, action3

            elif filtered_s in surface:  
                found_surface.append(filtered_s)
                # description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
                # print(f"Found Surface enemy: {filtered_s}")
                # action_prompt("Surface Enemy", filtered_s, description)
                actions = action_prompt(filtered_s)  # Get actions for entity
                action1, action2, action3 = actions[:3]  # top 3 actions
                # print(f"Found Surface enemy: {filtered_s}")
                return filtered_s, action1, action2, action3

            elif filtered_s in intel:  
                found_intel.append(filtered_s)
                # description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
                # print(f"Found enemy Intel: {filtered_s}")
                # action_prompt("Intel", filtered_s, description)
                actions = action_prompt(filtered_s)  # Get actions for entity
                action1, action2, action3 = actions[:3]  # top 3 actions
                # print(f"Found enemy Intel: {filtered_s}")
                return filtered_s, action1, action2, action3

            elif filtered_s in cyber:  
                found_cyber.append(filtered_s)
                # description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
                # print(f"Found enemy Cyber: {filtered_s}")
                # action_prompt("Cyber", filtered_s, description)
                actions = action_prompt(filtered_s)  # Get actions for entity
                action1, action2, action3 = actions[:3]  # top 3 actions
                # print(f"Found enemy Cyber: {filtered_s}")
                return filtered_s, action1, action2, action3

            elif filtered_s in civilian:
                found_civilian.append(filtered_s)
                # description = ' '.join(words[i+1:i+3]) if i + 2 < len(words) else ""
                # print(f"Found Civilian: {filtered_s}")
                # action_prompt("Civilian", filtered_s, description)
                actions = action_prompt(filtered_s)  # Get actions for entity
                action1, action2, action3 = actions[:3]  # top 3 actions
                # print(f"Found Civilian: {filtered_s}")
                return filtered_s, action1, action2, action3
    
        return None, None, None, None
    # insert code here may?

filtered_s, action1, action2, action3 = extracted_chat(message)

# Print test
print(f"Entity: {filtered_s}")
print(f"Action 1: {action1}")
print(f"Action 2: {action2}")
print(f"Action 3: {action3}")
