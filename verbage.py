# afatk:[Jam, attack, sink]
# afgood:[friendly, civilian]

# for atk in afatk:
#     answer=input(afatk.prompt)
#     if answer == afatk:

# print(f"enemy{answer}ed")

# for friend in afgood:
#     answer=input(afgood.propmpt)
#     if answer == afgood:

# print(f"identified as{afgood}")

# Lists
enemy = ["uav", "bogie", "j-16", "j-16s", "bandit", "destroyer", "aav","jassm"]
intel = ["radio", "emission", "emissions"]
cyber = ["forward lookup", "requests", "request"]

chat_message = "[10:45:02] WF_Clark: Floater03_OPS (USS Cole DDG): @Maritime_OPS (Maritime Operations Center) Possible UAV swarm approaching from south, type unk.  Main generator still inop, drifting WNW at 5 knots, req support in Lane Ceasars"

def extracted_jargon(message):
    message = message.lower()
    # Find the position of the second '(' character
    first_parenthesis_pos = message.find('(')
    second_parenthesis_pos = message.find('(', first_parenthesis_pos + 1)
    
    # Extract the part of the message after the second '('
    if second_parenthesis_pos != -1:
        text_after_second_parenthesis = message[second_parenthesis_pos + 1:]  # Everything after the second '('
        
        # Split the extracted text into words
        words = text_after_second_parenthesis.split()  # Split into words
        first_8_words = words[:8]  # Only the first 8 words
        
        # separate lists 
        found_enemy = []
        found_intel = []
        found_cyber = []

        # Check each word and categorize it
        for word in first_8_words:
            if word in enemy:
                found_enemy.append(word)
            elif word in intel:
                found_intel.append(word)
            elif word in cyber:
                found_cyber.append(word)
        
        # Return the categorized lists
        return found_enemy, found_intel, found_cyber
    return [], [], []  # If none return empty list

#result
found_enemy, found_intel, found_cyber = extracted_jargon(chat_message)

# Print the results separately for each category
print("Found Enemy:", found_enemy)
print("Found enemy Intel:", found_intel)
print("Found enemy Cyber:", found_cyber)

# def enemy_prompt(enemy):

# def intel_prompt(intel):

# def cyber_prompt(cyber):