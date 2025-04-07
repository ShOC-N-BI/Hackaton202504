import re

# Sample lists (could be extended)
air_enemy = ["J-16s", "j-16s", "MIG-29", "SU-27"]
surface = ["DESTROYER", "CRUISER", "SUBMARINE"]
intel = ["RADIO", "EMISSION"]
cyber = ["NETWORK", "TRAFFIC"]
civilian = ["CIVILIAN", "COMMERCIAL"]

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
        text_second_parenthesis = message_upper[second_parenthesis_pos + 1:]

        # Use regex to capture relevant terms, considering possible entity format
        words = re.findall(r'\b([A-Z0-9\-]+)\b', text_second_parenthesis)

        # Lists to hold found words 
        found_air = []
        found_intel = []
        found_cyber = []
        found_surface = []
        found_civilian = []

        for i, word in enumerate(words):
            # Clean up the word by keeping only alphanumeric characters or hyphens and make it uppercase
            filtered_word = ''.join(e for e in word if e.isalnum() or e == '-').upper()

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
