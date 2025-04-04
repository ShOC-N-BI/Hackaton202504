import irc.bot
import sys
import psycopg2
from DataResponse import extracted_chat



# Track number,e1.category, e1.trackId, e12.callsign

# Database connection
print("Script running...")


def get_db_connection():
    conn = psycopg2.connect(
        dbname="postgresDB",
        user="kyle",
        password="123",
        host="postgresDB",
        port="5432"
    )
    return conn

# Function to insert message into PostgreSQL
def insert_message(message):
    try: 
        print("Begin inserting message")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO irc_messages (message) VALUES (%s)", (message,))
        # future input 
        # cur.execute("INSERT INTO irc_messages (entity, action1, action2, action3) VALUES (%s)", (entity_desc, action1, action2, action3))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Message inserted into DB: {message}")
    except:
        print("Message insert fail")

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
        # Capture the IRC message
        message = event.arguments[0]
        print(f"Received message: {message}")
        
        # Insert message into PostgreSQL
        insert_message(message)

        # Process message from chat
        found_enemy, found_intel, found_cyber = extracted_chat(message)
        print("Found Air enemy:", found_enemy)
        print("Found enemy Intel:", found_intel)
        print("Found enemy Cyber:", found_cyber)

def start_irc_bot():
    bot = IRCBot("#shoebody", "Skibby_Mendoza")
    print("IRC listener starting...")
    bot.start()


start_irc_bot()
