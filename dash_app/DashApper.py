import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import psycopg2
import time
import datetime

# Database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname="postgresDB",
        user="kyle",
        password="123",
        host="postgresDB",
        port="5432"
    )
    return conn

# Function to fetch latest message counts from PostgreSQL
def get_user_message_counts():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT message FROM irc_messages")
    messages = cur.fetchall()
    cur.close()
    conn.close()

    # Placeholder for user message counts
    users_count = {
        'User0': 0,
        'User1': 2,
        'User2': 7,
        'User3': 3
    }

    # Count messages by user (for now, assuming 'User0' to 'User3' are users)
    for message in messages:
        user = "User0"  # This is just an example, you can refine the logic to detect the actual user
        if user in users_count:
            users_count[user] += 1

    return users_count

# Dash app setup
app = dash.Dash(__name__)

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

# Callback to update graph every 10 seconds
@app.callback(
    Output('live-graph', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    """Updates the graph every 10 seconds based on latest user message counts."""
    users_count = get_user_message_counts()  # Fetch latest message counts from DB
    print(f"Updated users_count: {users_count}")  # Debug print
    df = pd.DataFrame({
        "User": list(users_count.keys()),
        "Messages": list(users_count.values())
    })
    return px.bar(df, x="User", y="Messages", title="User Message Activity in #tm_c2_coord")

if __name__ == '__main__':
    print("Starting Dash App...")
    app.run(debug=True, host='0.0.0.0', port=8050)
