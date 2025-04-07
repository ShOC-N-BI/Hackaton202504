import re

# Sample lists (could be extended)
air_enemy = ["J-16s", "j-16s", "MIG-29", "SU-27"]
surface = ["DESTROYER", "CRUISER", "SUBMARINE"]
intel = ["RADIO", "EMISSION"]
cyber = ["NETWORK", "TRAFFIC"]
civilian = ["CIVILIAN", "COMMERCIAL"]

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
        words = re.findall(r'\b([A-Z0-9\-]+)\b', text_second_parenthesis)

        # Process each word to identify and act on entities
        for word in words:
            filtered_word = word.upper()

            # Handle singular/plural matching more robustly
            if filtered_word in air_enemy:
                entity, action1, action2, action3 = action_prompt(filtered_word)
                print(f"Found Air Enemy: {filtered_word}")
                break
            elif filtered_word in surface:
                entity, action1, action2, action3 = action_prompt(filtered_word)
                print(f"Found Surface Entity: {filtered_word}")
                break
            elif filtered_word in intel:
                entity, action1, action2, action3 = action_prompt(filtered_word)
                print(f"Found Intel Entity: {filtered_word}")
                break
            elif filtered_word in cyber:
                entity, action1, action2, action3 = action_prompt(filtered_word)
                print(f"Found Cyber Entity: {filtered_word}")
                break
            elif filtered_word in civilian:
                entity, action1, action2, action3 = action_prompt(filtered_word)
                print(f"Found Civilian: {filtered_word}")
                break
    
    # Return entity and actions found
    print(f"Entity: {entity}")
    print(f"Actions: {action1}, {action2}, {action3}")
    return entity, action1, action2, action3

# Test case
message = "[10:48:58] WF_Clark: Analysis_Center01 (Analysis Center): @Intel_Ops (Intelligence Operations Center) 2x j-16s were Yak-28s on UAV Imagery jassm carrier on aav apron forward J-8 aircraft CV commercial vessel 25.045310306035184, -77.464458773165 in Lane Flamingo"
extracted_chat(message)
