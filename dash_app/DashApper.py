import irc.bot
import sys

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
        print(f"{event.source} {event.target} > {event.arguments[0]}")

bot = IRCBot("#test", "my_bot") # channel, nickname
bot.start()

while True:
    print('.')
    time.sleep(10)


















# import dash
# from dash import dcc, html
# import plotly.express as px
# import pandas as pd



# # Dash app setup
# app = dash.Dash(__name__)

# # Hardcoded data
# data = {
#     'category': ['A', 'B', 'C', 'D', 'E'],
#     'values': [10, 20, 30, 40, 50]
# }

# df = pd.DataFrame(data)

# # Create a bar plot using the hardcoded data
# fig = px.bar(df, x='category', y='values', title='Hardcoded Data Bar Chart')

# # Dash layout
# app.layout = html.Div([
#     html.H1("Dash App with Hardcoded DEta"),
#     dcc.Graph(figure=fig)
# ])

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8050)
