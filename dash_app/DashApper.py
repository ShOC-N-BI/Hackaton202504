import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import queue

msg_queue = queue.Queue()

# Dash app setup
app = dash.Dash(__name__)

# Store user message counts
user_message_counts = {}

def get_latest_messages():
    """Pulls new messages from the queue and updates user message counts."""
    while not msg_queue.empty():
        msg = msg_queue.get()
        user = msg["user"]
        user_message_counts[user] = user_message_counts.get(user, 0) + 1  # Count messages per user

# Dash layout
app.layout = html.Div([
    html.H1("Live IRC Chat Activity"),
    dcc.Graph(id='live-graph'),
    dcc.Interval(
        id='interval-component',
        interval=10 * 1000,  # 10 seconds
        n_intervals=0
    )
])

# Callback to update graph
@app.callback(
    Output('live-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    get_latest_messages()  # Get new messages
    df = pd.DataFrame({
        "User": list(user_message_counts.keys()),
        "Messages Sent": list(user_message_counts.values())
    })
    
    fig = px.bar(df, x="User", y="Messages Sent", title="User Message Activity in #shoebody")
    return fig

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
