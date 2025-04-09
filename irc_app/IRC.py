import irc.bot
import sys
import psycopg2
# from DataResponse import extracted_chat
from EntGen import extracted_chat


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
def insert_message(message, entity, action1, action2, action3):
    try: 
        print("Begin inserting message")
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO irc_messages (message) VALUES (%s)", (message,))
        print("Main message inserted")
        # future input 
        print(entity)
        print(action1)
        print(action2)
        print(action3)
        cur.execute("INSERT INTO pae (entity, action1, action2, action3) VALUES (%s, %s, %s, %s)", (entity, action1, action2, action3,))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Message inserted into DB: {message}")
    except:
        print("Message insert fail 1")

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
        try:
            found_entity, action1, action2, action3 = extracted_chat(message)
            if found_entity is not None:
                insert_message(message, found_entity, action1, action2, action3)
        except:
            print("bad input")
        
        # Insert message into PostgreSQL
        

        # Process message from chat
        

def start_irc_bot():
    bot = IRCBot("#tm_c2_coord", "Skibby_Mendoza")
    print("IRC listener starting...")
    bot.start()


start_irc_bot()
