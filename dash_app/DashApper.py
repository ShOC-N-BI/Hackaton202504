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
        host="10.5.185.53",
        dbname="shooca_db",
        user="shooca",
        password="shooca222",
        port="5432"
    )
    return conn

# Function to fetch latest message counts from PostgreSQL
def get_user_message_counts():
    global user_count
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT message FROM pae_data order by timestamp desc limit 1")
        messages = cur.fetchall()
        cur.close()
        conn.close()

        print("Message below:")
        print(messages[0][0])
        
    except:
        print("Message pull fail from base text")

    user = "User0"  # This is just an example, you can refine the logic to detect the actual user
    if user in users_count:
        users_count[user] += 1

    return users_count

# Dash app setup
app = dash.Dash(__name__)

# Dash layout
app.layout = html.Div([
    html.Div([
        html.H1("Live IRC Chat Activity", style={
            'textAlign': 'center',
            'marginBottom': '30px',
            'fontSize': '40px'
        }),

        html.Div([
            html.H2("Perceived Actionable Entity:"),
            html.Div(id='entity-message')
        ], style={
            # 'backgroundColor': '#f9f9f9',
            # 'border': '2px solid #ccc',
            # 'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px 4vw',
            # 'boxShadow': '2px 2px 10px rgba(0,0,0,0.05)',
            'fontSize': '18px',
            'fontWeight': 'bold'
        }),

        html.Div([
            #html.H6("Battle Effect 1"),
            html.Div(id='action1-message')
        ], style={
            'backgroundColor': '#f9f9f9',
            'border': '2px solid #ccc',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px 4vw',
            'boxShadow': '2px 2px 10px rgba(0,0,0,0.05)',
            'fontSize': '30px',
            'fontWeight': 'bold'
        }),

        html.Div([
            #html.H2("Battle Effect 2"),
            html.Div(id='action2-message')
        ], style={
            'backgroundColor': '#f9f9f9',
            'border': '2px solid #ccc',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px 4vw',
            'boxShadow': '2px 2px 10px rgba(0,0,0,0.05)',
            'fontSize': '30px',
            'fontWeight': 'bold'
        }),

        html.Div([
            #html.H2("Battle Effect 3"),
            html.Div(id='action3-message')
        ], style={
            'backgroundColor': '#f9f9f9',
            'border': '2px solid #ccc',
            'borderRadius': '10px',
            'padding': '20px',
            'margin': '10px 4vw',
            'boxShadow': '2px 2px 10px rgba(0,0,0,0.05)',
            'fontSize': '30px',
            'fontWeight': 'bold'
        }),

        html.Div(id='latest-message', style={
            'marginTop': '50px',
            'fontSize': '16px',
            'padding': '20px',
            'textAlign': 'center',
            'color': '#888'
        }),

        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,
            n_intervals=0
        )
    ], style={
        'backgroundColor': '#dddddd',
        'border': '4px solid #ccc',
        'borderRadius': '20px',
        'padding': '30px',
        'margin': '40px auto',
        'maxWidth': '90vw',
        'boxShadow': '0 4px 16px rgba(0, 0, 0, 0.1)'
    })
])


# Callback to update graph every 10 seconds
@app.callback(
    Output('entity-message', 'children'),
    Output('action1-message', 'children'),
    Output('action2-message', 'children'),
    Output('action3-message', 'children'),
    #Output('live-graph', 'figure'),
    Output('latest-message', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_graph(n):
    users_count = get_user_message_counts()  # Update counts
    entity_msg = ""

    # Fetch latest message from DB
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT message FROM pae_data ORDER BY timestamp DESC LIMIT 1")
        messages = cur.fetchall()

        cur.execute("SELECT entity FROM pae_data ORDER BY timestamp DESC LIMIT 1")
        pae_e = cur.fetchall()

        cur.execute("SELECT action1 FROM pae_data ORDER BY timestamp DESC LIMIT 1")
        pae_1 = cur.fetchall()
        
        cur.execute("SELECT action2 FROM pae_data ORDER BY timestamp DESC LIMIT 1")
        pae_2 = cur.fetchall()

        cur.execute("SELECT action3 FROM pae_data ORDER BY timestamp DESC LIMIT 1")
        pae_3 = cur.fetchall()

        cur.close()
        conn.close()

        
    except:
        latest_msg = "Message pull failed."
        print("Message pull failed.")

    latest_msg = messages[0][0] if messages else "No latest message found."
    entity_msg = pae_e[0][0] if pae_e else "No message found for description"
    action1_msg = pae_1[0][0] if pae_1 else "No message found for action 1"
    action2_msg = pae_2[0][0] if pae_2 else "No message found for action 2"
    action3_msg = pae_3[0][0] if pae_3 else "No message found for action 3"
    # Create bar chart
    df = pd.DataFrame({
        "User": list(users_count.keys()),
        "Messages": list(users_count.values())
    })
    fig = px.bar(df, x="User", y="Messages", title="User Message Activity in #tm_c2_coord")

    return f"{entity_msg}", f"{action1_msg}", f"{action2_msg}", f"{action3_msg}", f"Latest Message: {latest_msg}"

if __name__ == '__main__':
    print("Starting Dash App...")
    app.run(debug=True, host='0.0.0.0', port=8050)
