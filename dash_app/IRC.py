import irc.bot
import sys
import queue
import threading

# Message queue for shared data
msg_queue = queue.Queue()

class IRCBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channel, nickname, server="10.10.21.52", port=6667):
        super().__init__([(server, port)], nickname, nickname)
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
        message_data = {
            "user": event.source,  # Username
            "message": event.arguments[0]  # Message content
        }
        msg_queue.put(message_data)  # Add message to the queue
        print(message_data)  # Debugging output

# Function to start the bot in a separate thread
def start_irc_bot():
    bot = IRCBot("#shoebody", "notMendoza")
    bot.start()

# Start IRC bot in a separate thread
threading.Thread(target=start_irc_bot, daemon=True).start()
