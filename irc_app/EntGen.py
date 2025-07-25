import re
import os
import json


# To ensure that we load the words file from the directory of the script we have to do these extra steps
script_dir = os.path.dirname(__file__)
with open(os.path.join(script_dir, 'words.json'), 'r') as file:
    words = json.load(file)
    ACTIONS = words["ACTIONS"]
    WORDS = words["WORDS"]
    

out =["SWIM","BEER"]

battle_effect_dict = {
    "Attack":["Attack, Intercept", "Ambush", "Assail", "Assault", "Strike", "Hit", "Raid", "Invade", "Advance", "Shoot", "Suppress", "Disable"],
    "Investigate":["Investigate", "Consider", "Examine", "Explore", "Inspect", "Interrogate", "Probe", "Question", "Review", "Search", "Study", "Inquire", "Research", "Faded", "Fade", "Shadow"],
    "Communicate":["Communicate", "Broadcast", "Contact", "Convey", "Correspond", "Disclose", "Reach out", "Pass On", "Tell", "Transfer", "Transmit", "Discover", "Relay", "Report"],
    "Destroy":["Destroy", "Kill", "Nullify", "Terminate", "Vanish"],
    "Counter":["Counter", "Hinder", "Counteract", "Oppose", "Respond", "Retaliate"],
    "Evade":["Evade", "Avoid", "Circumvent", "Conceal", "Elude", "Escape", "Fend Off", "Flee", "Hide"],
    "Brace for Impact": ["Brace for Impact", "Prepare", "Fortify"],
    "Jam":["Jam", "Block", "Bind", "Congest"],
    "Hack":["Hack"],
    "Counter":["Counter", "Hinder", "Counteract", "Oppose", "Respond", "Retaliate"],
    "Psyop":["Psyop", "Propaganda"],
    "Harass":["Harass", "Hassle", "Intimidate", "Torment", "Disturb"]
}

# message = "[10:48:58] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) 2x Torpedo were observed on EO/IR Imagery located on parking apron forward of aircraft hangers IVO 25.045310306035184, -77.464458773165 in Lane Flamingo"
# message = "[11:00:11] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) From 1205Z to 2111Z Radio emmission were detected at location  27.689097938330395, -80.38238737940404 operating on VHF. in Lane Bellagio"
# message = "[10:45:02] WF_Clark: Floater03_OPS (USS Cole DDG): @Maritime_OPS (Maritime Operations Center) Possible helos swarm approaching from south, type unk.  Main generator still inop, drifting WNW at 5 knots, req support in Lane Ceasars"
# message = "[10:48:58] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) 2x J-16s were observed on EO/IR Imagery located on parking apron forward of aircraft hangers IVO 25.045310306035184, -77.464458773165 in Lane Flamingo"
#message = "[11:22:33] WF_FYST: IntelOps: @ Hydro_MSO, TN 44993/94/95/96 are all 1x J-15 each track."
# def get_description(words, index, max_words=5):
#     description = ' '.join(words[index+1:index+max_words]) if index + max_words <= len(words) else ' '.join(words[index+1:])

def action_prompt(entity, description=""):
    """
    Check and see if the entity passed can be found in the "WORDS" lists, if so then retrieve the associated "ACTIONS" and return them
    TO-DO: Review why is there a description parameter that we don't need
    """
    if description:
        print(f"  Description: {description}")

    i = entity.split()[0]
    for k in WORDS.keys():
        if i in WORDS[k]:
            return ACTIONS[k]
    
    return None, None, None


def get_description(words, index, max_words=4):
    description = ""
    # Check if the word before the current entity is present and does not contain a colon or closing parenthesis
    if index > 0 and (':' not in words[index - 1] and ')' not in words[index - 1]):
        description = words[index - 1] + " "

    # Now, add the entity and additional words to the description
    for i in range(1, max_words + 1):
        if index + i < len(words):
            description += words[index + i] + " "

    return description.strip()

def extracted_chat(message):
    message_upper = message.upper()
    
    # Find the positions of the second parenthesis ')'
    first_parenthesis_pos = message_upper.find(')')
    second_parenthesis_pos = message_upper.find(')', first_parenthesis_pos + 1)
    
    # Find the second colon ':'
    second_colon_pos = message_upper.find(':', message_upper.find(':') + 1)
    
    # If a second colon is found, start from that position
    if second_colon_pos != -1:
        start_pos = second_colon_pos + 1
    else:
        start_pos = second_parenthesis_pos + 1 if second_parenthesis_pos != -1 else 0  # Fallback to second parenthesis position if no second colon
    
    # Extract the message text starting from the found position (after second colon or second parenthesis)
    text_to_process = message[start_pos:].strip()
    
    words = text_to_process.split()

    found_air = []
    found_intel = []
    found_cyber = []
    found_surface = []
    found_civilian = []
    found_defend = []
    found_rando = []
    found_enemy =[]

    for i, word in enumerate(words):
        filtered_word = ''.join(e for e in word if e.isalnum() or e == '-').upper()
        filtered_s = filtered_word.rstrip('S')

        if filtered_s in WORDS["AIR"]:
            found_air.append(filtered_s)
            description = get_description(words, i)
            filtered_s = filtered_s + " " + description
            actions = action_prompt(filtered_s)
            action1, action2, action3 = actions[:3]
            return filtered_s, action1, action2, action3

        if filtered_s in WORDS["INCOMING"]:
            found_defend.append(filtered_s)
            description = get_description(words, i)
            filtered_s = filtered_s + " " + description
            actions = action_prompt(filtered_s)
            action1, action2, action3 = actions[:3]
            return filtered_s, action1, action2, action3

        elif filtered_s in WORDS["SURFACE"]:
            found_surface.append(filtered_s)
            description = get_description(words, i)
            filtered_s = filtered_s + " " + description
            actions = action_prompt(filtered_s)
            action1, action2, action3 = actions[:3]
            return filtered_s, action1, action2, action3

        elif filtered_s in WORDS["INTEL"]:
            found_intel.append(filtered_s)
            description = get_description(words, i)
            filtered_s = filtered_s + " " + description
            actions = action_prompt(filtered_s)
            action1, action2, action3 = actions[:3]
            return filtered_s, action1, action2, action3

        elif filtered_s in WORDS["CYBER"]:
            found_cyber.append(filtered_s)
            description = get_description(words, i)
            filtered_s = filtered_s + " " + description
            actions = action_prompt(filtered_s)
            action1, action2, action3 = actions[:3]
            return filtered_s, action1, action2, action3

        elif filtered_s in WORDS["CIVILIAN"]:
            found_civilian.append(filtered_s)
            description = get_description(words, i)
            filtered_s = filtered_s + " " + description
            actions = action_prompt(filtered_s)
            action1, action2, action3 = actions[:3]
            return filtered_s, action1, action2, action3
        
        elif filtered_s in WORDS["RANDOM"]:
            found_rando.append(filtered_s)
            description = get_description(words, i)
            filtered_s = filtered_s + " " + description
            actions = action_prompt(filtered_s)
            action1, action2, action3 = actions[:3]
            return filtered_s, action1, action2, action3
        
        elif filtered_s in WORDS["ENEMIES"]:
            found_enemy.append(filtered_s)
            description = get_description(words, i)
            filtered_s = filtered_s + " " + description
            actions = action_prompt(filtered_s)
            action1, action2, action3 = actions[:3]
            return filtered_s, action1, action2, action3

    
    return None, None, None, None

# filtered_s, action1, action2, action3 = extracted_chat(message)
# print(f"Entity: {filtered_s}")
# print(f"Action 1: {action1}")
# print(f"Action 2: {action2}")
# print(f"Action 3: {action3}")
