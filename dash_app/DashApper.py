import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import psycopg2
import time
import datetime

# Placeholder for user message counts
users_count = {
    'User0': 0,
    'User1': 2,
    'User2': 7,
    'User3': 3
}

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
    global user_count
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT message FROM irc_messages order by timestamp desc limit 1")
        messages = cur.fetchall()
        cur.close()
        conn.close()

        print("Message below:")
        print(messages[0][0])
        
    except:
        print("Message pull fail")

    user = "User0"  # This is just an example, you can refine the logic to detect the actual user
    if user in users_count:
        users_count[user] += 1

    return users_count

# Dash app setup
app = dash.Dash(__name__)

# Dash layout
app.layout = html.Div([
    html.H1("Live IRC Chat Activity", style={'textAlign': 'center', 'marginBottom': '30px'}),
    html.H2("Perceived Actionable Entity", style={'marginLeft': '.5vw'}),
    html.H3("Description here", style={'marginLeft': '3vw'}),
    html.H2("Battle Effect 1", style={'marginLeft': '2vw'}),
    html.H3("Description here", style={'marginLeft': '4vw'}),
    html.H2("Battle Effect 2", style={'marginLeft': '2vw'}),
    html.H3("Description here", style={'marginLeft': '4vw'}),
    html.H2("Battle Effect 3", style={'marginLeft': '2vw'}),
    html.H3("Description here", style={'marginLeft': '4vw'}),
    #html.Div(id='latest-message', style={'marginTop': '20px', 'fontSize': '18px', 'fontWeight': 'bold'}),
    #html.Div(id='latest-message', style={'marginTop': '20px', 'fontSize': '18px', 'fontWeight': 'bold'}),
    #html.Div(id='latest-message', style={'marginTop': '20px', 'fontSize': '18px', 'fontWeight': 'bold'}),
    dcc.Graph(id='live-graph'),
    html.Div(id='latest-message', style={'marginTop': '20px', 'fontSize': '18px', 'fontWeight': 'bold'}),
    dcc.Interval(
        id='interval-component',
        interval=10 * 1000,  # 10 seconds
        n_intervals=0
    )
])

# Callback to update graph every 10 seconds
@app.callback(
    Output('live-graph', 'figure'),
    Output('latest-message', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    users_count = get_user_message_counts()  # Update counts

    # Fetch latest message from DB
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT message FROM irc_messages ORDER BY timestamp DESC LIMIT 1")
        messages = cur.fetchall()
        cur.close()
        conn.close()
        latest_msg = messages[0][0] if messages else "No message found."
    except:
        latest_msg = "Message pull failed."

    # Create bar chart
    df = pd.DataFrame({
        "User": list(users_count.keys()),
        "Messages": list(users_count.values())
    })
    fig = px.bar(df, x="User", y="Messages", title="User Message Activity in #tm_c2_coord")

    return fig, f"Latest Message: {latest_msg}"

if __name__ == '__main__':
    print("Starting Dash App...")
    app.run(debug=True, host='0.0.0.0', port=8050)
