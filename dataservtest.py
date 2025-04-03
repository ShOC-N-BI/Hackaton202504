import irc.bot
import sys

# lists

# air_fighter = [
#     "MiG-21", "MiG-15", "MiG-17", "MiG-19", "MiG-23", "MiG-25", "MiG-29", "MiG-31", 
#     "Su-7", "Su-9", "Su-11", "Su-15", "Su-17", "Su-20", "Su-22", "Su-24", "Su-25", 
#     "Su-27", "Su-30", "Su-33", "Su-35", "Su-57", "Yak-9", "Yak-23", "Yak-25", "Yak-28", 
#     "Yak-38", "Yak-41"
# ]
# air_bomber = [
#     "A-20 Havoc", "Il-2", "Il-4", "Il-10", "Il-28", "Il-40", "Il-54", 
#     "M-4", "M-50", "B-25 Mitchell", "Pe-2", "Tu-2", "Tu-4", "Tu-14", "Tu-16", 
#     "Tu-22", "Tu-22M", "Tu-82", "Tu-85", "Tu-91", "Tu-95", "Tu-98", "Tu-160", 
#     "Yak-28", "Yak-28B"
# ]
air = ["UAV", "BOGEY", "BANDIT", "AAV", "BANZAI" ]
# maritime =["DESTROYER", "FRIGATE","CRUISER","SUBMARINE","SUB",]
# land= ["JASSM","ATTACK"]
intel = ["RADIO", "EMISSION", "EMISSIONS","BLUR","AUTOCAT","BEAM RIDER"]
cyber = ["FORWARD LOOKUP", "REQUEST","ALLIGATOR","NETWORK","TRAFFIC"]
# friendly =["ANGELS","ANYFACE","BIRD","BITTERSWEET","BLIND","BRUISER","BULLDOG","CHICK"]

# process message
def extracted_chat(message):
    message = message.lower()

    # Finds position of the second '(' character
    first_parenthesis_pos = message.find('(')
    second_parenthesis_pos = message.find('(', first_parenthesis_pos + 1)
    
    # Extracts the message after the second '('
    if second_parenthesis_pos != -1:
        text_second_parenthesis = message[second_parenthesis_pos + 1:]  # Everything after the second '('
        
        # Split the extracted text into words
        words = text_second_parenthesis.split()  # Split into words
        first_8_words = words[:9]  # Only the first 8 words
        
        # lists 
        found_air = []
        found_intel = []
        found_cyber = []
        # found_maritime = []
        # found_land =[]

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

        for word in first_8_words:
            if word.lower() in [x.lower() for x in air]:  # Convert both to lowercase 
                found_air.append(word)
            # elif word.lower() in [x.lower() for x in maritime]:  
            #     found_maritime.append(word)
            elif word.lower() in [x.lower() for x in intel]:
                found_intel.append(word)
            elif word.lower() in [x.lower() for x in cyber]:
                found_cyber.append(word)

        # Return the categorized lists
        return found_air, found_intel, found_cyber, #found_maritime
    return [], [], []#, []  # If none return empty list

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
    
    def on_pubmsg(self, connection, event,):
        # Capture the IRC message
        message = event.arguments[0]
        
        # Output to console
        print(f"Received message: {message}")

        # Process message from chat
        found_enemy, found_intel, found_cyber = extracted_chat(message)

        # Print the results separately for each category
        print("Found Air enemy:", found_enemy)
        # print("Found maritime enemy:", found_maritime)
        print("Found enemy Intel:", found_intel)
        print("Found enemy Cyber:", found_cyber)

bot = IRCBot("#shoebody", "bop")  # channel, nickname
# please select a channel and nickname unique to you and your org
bot.start()

