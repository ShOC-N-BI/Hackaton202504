# lists
# air_bomber = [
#     "A-20 Havoc", "Il-2", "Il-4", "Il-10", "Il-28", "Il-40", "Il-54", 
#     "M-4", "M-50", "B-25 Mitchell", "Pe-2", "Tu-2", "Tu-4", "Tu-14", "Tu-16", 
#     "Tu-22", "Tu-22M", "Tu-82", "Tu-85", "Tu-91", "Tu-95", "Tu-98", "Tu-160", 
#     "Yak-28", "Yak-28B"
# ]

        # Check each word and categorize it
        # for word in first_8_words:
        #     if word in air:
        #         found_air.append(word)
        #     # elif word in maritime:
        #     #     found_maritime.append(word)
        #     elif word in intel:
        #         found_intel.append(word)
        #     elif word in cyber:
        #         found_cyber.append(word)

# maritime =["DESTROYER", "FRIGATE","CRUISER","SUBMARINE","SUB",]
# friendly =["ANGELS","ANYFACE","BIRD","BITTERSWEET","BLIND","BRUISER","BULLDOG","CHICK"]

import irc.bot
import sys
import re

# Define the list of aircraft, air types, etc.
air_fighter = [
    "MiG-21", "MiG-15", "MiG-17", "MiG-19", "MiG-23", "MiG-25", "MiG-29", "MiG-31",
    "Su-7", "Su-9", "Su-11", "Su-15", "Su-17", "Su-20", "Su-22", "Su-24", "Su-25",
    "Su-27", "Su-30", "Su-33", "Su-35", "Su-57", "Yak-9", "Yak-23", "Yak-25", "Yak-28",
    "Yak-38", "Yak-41", "J-16"
]
air = ["UAV", "BOGEY", "BANDIT", "BANZAI", "AAV"]
land = ["JASSM", "ATTACK"]
intel = ["RADIO", "EMISSION", "EMISSIONS", "BLUR", "AUTOCAT", "BEAM RIDER"]
cyber = ["FORWARD LOOKUP", "REQUEST", "ALLIGATOR", "NETWORK", "TRAFFIC"]

# Process the message
def extracted_chat(message):
    message = message.lower()

    # Find the position of the second '(' character
    first_parenthesis_pos = message.find('(')
    second_parenthesis_pos = message.find('(', first_parenthesis_pos + 1)
    
    # Extract message after the second '('
    if second_parenthesis_pos != -1:
        text_second_parenthesis = message[second_parenthesis_pos + 1:]  # Everything after the second '('

        words = re.findall(r'\b\w+\b', text_second_parenthesis)  # Extract words only (ignores punctuation)
        first_words = words[:15]  # Only the first 15 words
        
        # Lists for categorized findings
        found_air = []
        found_intel = []
        found_cyber = []
        found_land = []

        for word in first_words:
            filtered_word = re.sub(r'[^a-zA-Z]', '', word)  # Remove non-alphabetical characters
            
            # Check the word against each list
            if filtered_word.lower() in [x.lower() for x in air_fighter]:
                found_air.append(word)
            elif filtered_word.lower() in [x.lower() for x in air]:
                found_air.append(word)
            elif filtered_word.lower() in [x.lower() for x in land]:
                found_land.append(word)
            elif filtered_word.lower() in [x.lower() for x in intel]:
                found_intel.append(word)
            elif filtered_word.lower() in [x.lower() for x in cyber]:
                found_cyber.append(word)

        # Return the categorized lists
        return found_air, found_intel, found_cyber, found_land
    return [], [], [], []  # If no parentheses found, return empty lists

# IRCBot
class IRCBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server="10.10.21.52", port=6667):
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port)], nickname, nickname)
        self.channel = channel
    
    def on_welcome(self, connection, event):
        print("WELCOME")
        connection.join(self.channel)
    
    def on_join(self, connection, event):
        print(f"JOIN {self.channel}")

    def on_disconnect(self, connection, event):
        print("DISCONNECT")
        sys.exit(0)
    
    def on_pubmsg(self, connection, event):
        # Capture IRC message
        message = event.arguments[0]
        
        # Output to console
        print(f"Received message: {message}")

        # Process message from chat
        found_air, found_intel, found_cyber, found_land = extracted_chat(message)

        # Print the results separately
        if found_air:
            print("Found Air enemy:", found_air)
        if found_land:
            print("Found land enemy:", found_land)
        if found_intel:
            print("Found enemy Intel:", found_intel)
        if found_cyber:
            print("Found enemy Cyber:", found_cyber)

# Start the bot
bot = IRCBot("#shoebody", "bop")  # channel, nickname
bot.start()
# please select a channel and nickname unique to you and your org