# air_friendly = [
#     "Bird", "Bird(s) affirm", "Bird(s) away", "Bird(s) negat", "Bittersweet", 
#     "Blue on blue", "Bruiser", "Buddy lock", "Buddy spike", "Bulldog", 
#     "Cherubs", "Chicks", "Clean", "Chattermark"
# ]


# sea_friendly = [
#     "Bassett", "Bruiser", "Bulldog", "Cobra", "Cowboys", "Cyclops", "Deadeye"
# ]

# land_friendly = [
#     "Base (number)", "Banzai", "Bracket", "Burn glint", "Buster", 
#     "Blank", "Bulldog", "Bump/Bump-up", "Brevity", "Burn glint", "Buster"
# ]


# air_enemy = [
#     "Bandit", "Bogey", "Bogey dope", "Blow through", "Bloodhound", "Bracket", 
#     "Break (direction)", "Breakaway", "Bingo", "Brevity", "Bruiser", 
#     "Buddy lock", "Buddy spike", "Bugout", "Buster"
# ]

# land_enemy = [
#     "Banzai", "Bracket", "Bump/Bump-up", "Burn glint", "Buster", "Blank", 
#     "Bulldog", "Brevity"
# ]


# sea_enemy = [
#     "Bandit", "Bogey", "Bassett", "Bruiser", "Bulldog", "Cobra", "Cowboys", 
#     "Cyclops", "Deadeye"
# ]


# rsam = [
#     "SA-1 Guild", "SA-2 Guideline", "SA-3 Goa", "SA-4 Ganef", "SA-5 Gammon", 
#     "SA-6 Gainful", "SA-7 Grail", "SA-8 Gecko", "SA-9 Gaskin", "SA-10 Grumble", 
#     "SA-11 Gadfly", "SA-12 Gladiator/Giant", "SA-13 Gopher", "SA-14 Gremlin", 
#     "SA-15 Gauntlet", "SA-16 Gimlet", "SA-17 Grizzly", "SA-18 Grouse", 
#     "SA-19 Grison", "SA-20 Gargoyle", "SA-21 Growler", "SA-22 Greyhound", 
#     "SA-23 Gladiator/Giant", "SA-24 Grinch", "SA-X-25 Sosna-R", "SA-26 Pechora-2M", 
#     "SA-27 Gollum", "SA-X-28 S-350E Vityaz", "SA-29 Gizmo"
# ]

# rnsam = [
#     "SA-N-1 Goa", "SA-N-2 Guideline", "SA-N-3 Goblet", "SA-N-4 Gecko", "SA-N-5 Grail",
#     "SA-N-6 Grumble", "SA-N-7 Gadfly", "SA-N-8 Gremlin", "SA-N-9 Gauntlet", "SA-N-10 Grouse",
#     "SA-N-11 Grison", "SA-N-12 Grizzly", "SA-N-14 Grouse", "SA-N-20 Gargoyle"
# ]

# chsam = [
#     "CH-SA-3",  # HN-5
#     "CH-SA-4",  # HQ-7
#     "CH-SA-6",  # HQ-6
#     "CH-SA-7",  # QW-1
#     "CH-SA-8",  # QW-2
#     "CH-SA-10", # FN-6
#     "CH-SA-15", # HQ-17
#     "CH-SA-16", # HQ-16
#     "CH-SA-N-4",# HHQ-7
#     "CH-SA-N-9",# HHQ-9
#     "CH-SA-N-16",# HHQ-16
#     "CH-SA-N-17",# HHQ-10
#     "CH-SA-N-21" # HHQ-9B
# ]

import irc.bot
import sys
import re

# # Define the list of aircraft, air types, etc.
# air_fighter = [
#     "MiG-21", "MiG-15", "MiG-17", "MiG-19", "MiG-23", "MiG-25", "MiG-29", "MiG-31",
#     "Su-7", "Su-9", "Su-11", "Su-15", "Su-17", "Su-20", "Su-22", "Su-24", "Su-25",
#     "Su-27", "Su-30", "Su-33", "Su-35", "Su-57", "Yak-9", "Yak-23", "Yak-25", "Yak-28",
#     "Yak-38", "Yak-41", "J-16"
# ]
# air_bomber = [
#     "A-20 Havoc", "Il-2", "Il-4", "Il-10", "Il-28", "Il-40", "Il-54", 
#     "M-4", "M-50", "B-25 Mitchell", "Pe-2", "Tu-2", "Tu-4", "Tu-14", "Tu-16", 
#     "Tu-22", "Tu-22M", "Tu-82", "Tu-85", "Tu-91", "Tu-95", "Tu-98", "Tu-160", 
#     "Yak-28", "Yak-28B"
# ]
# navy =["DESTROYER", "DD", "FRIGATE", "FF","CRUISER","CC","SUBMARINE","SUB","CARRIER","CV"]
# air = ["UAV", "BOGEY", "BANDIT", "BANZAI", "AAV"]
# land = ["JASSM", "ATTACK"]
# intel = ["RADIO", "EMISSION", "EMISSIONS", "BLUR", "AUTOCAT", "BEAM RIDER"]
# cyber = ["FORWARD LOOKUP", "REQUEST", "ALLIGATOR", "NETWORK", "TRAFFIC"]
# #message = "[10:51:58] WF_Clark: Floater05_OPS (USS Guam DDG): @Maritime_OPS (Maritime Operations Center) Starting to recover first wave of MiG-15. Will start loading SA-8 min and it will take 1.5 hours to launch the second wave"

# # Updated function to process the message and extract relevant categories
# def extracted_chat(message):
#     # Convert the message to uppercase for easier comparison later
#     message_upper = message.upper()  

#     # Find second ')' character
#     first_parenthesis_pos = message_upper.find(')') 
#     second_parenthesis_pos = message_upper.find(')', first_parenthesis_pos + 1)
    
#     # Extract the text after second '('
#     if second_parenthesis_pos != -1:
#         text_second_parenthesis = message_upper[second_parenthesis_pos + 1:]  # Everything after the second ')'
        
#         # Split the message into words
#         words = text_second_parenthesis.split()

#         # Lists to hold found words in each category
#         found_air = []
#         found_intel = []
#         found_cyber = []
#         found_land = []
#         found_navy =[]

#         for word in words:
#             # Strip any trailing non-alphabetic characters 
#             filtered_word = ''.join(e for e in word if e.isalnum() or e == '-').upper()  # Allow hyphen

#             # Remove the 's' at the end for matching
#             filtered_word_singular = filtered_word.rstrip('S')

#             # Check if word matches any entry in the categories
#             if filtered_word_singular in [x.upper() for x in air_fighter]:
#                 found_air.append(filtered_word_singular)
#             elif filtered_word_singular in [x.upper() for x in air]:  
#                 found_air.append(filtered_word_singular)

#             elif filtered_word_singular in [x.upper() for x in land]:  
#                 found_land.append(filtered_word_singular)

#             elif filtered_word_singular in [x.upper() for x in navy]:  
#                 found_navy.append(filtered_word_singular)
                
#             elif filtered_word_singular in [x.upper() for x in intel]:  
#                 found_intel.append(filtered_word_singular)

#             elif filtered_word_singular in [x.upper() for x in cyber]:  
#                 found_cyber.append(filtered_word_singular)

        # Prompt actions for found entities
        # for entity in found_air:
        #     action = action_prompt("Air Enemy", entity)
        #     print(f"Action for {entity}: {action}")
        
        # for entity in found_land:
        #     action = action_prompt("Land Enemy", entity)
        #     print(f"Action for {entity}: {action}")

        # for entity in found_navy:
        #     action = action_prompt("Naval Enemy", entity)
        #     print(f"Action for {entity}: {action}")

        # for entity in found_intel:
        #     action = action_prompt("Intel", entity)
        #     print(f"Action for {entity}: {action}")
        
        # for entity in found_cyber:
        #     action = action_prompt("Cyber", entity)
        #     print(f"Action for {entity}: {action}")
        
        # Return the categorized lists
    #     return found_air, found_intel, found_cyber, found_land, found_navy

    # return [], [], [], [], []  # Return empty lists if no valid second parenthesis
    class BC3_out:
        def __init__(self, server="10.10.26.105", port=5001):
            self.ip = ip
            self.port = port
            self.url = f'http://{ip}:{port}/endpoint'

        def send_request_to_bc3(ip, port, json_example):
            response = requests.get(url)
            print(f"Status Code: {response.status_code}")
            return response    

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



        # # Process message from chat
        # found_air, found_intel, found_cyber, found_land, found_navy = extracted_chat(message)

        # Output the results
        # if found_air:
        #     print("Found Air enemies:", found_air)
        # if found_land:
        #     print("Found Land enemies:", found_land)
        # if found_navy:
        #     print("Found Land enemies:", found_navy)    
        # if found_intel:
        #     print("Found enemy Intel:", found_intel)
        # if found_cyber:
        #     print("Found enemy Cyber:", found_cyber)



    class Dash_app:
        def __init__(self)
        ...
    
# Start the bot
bot = IRCBot("#shoebody", "bop3")  # channel, nickname
bot.start()
# please select a channel and nickname unique to you and your org