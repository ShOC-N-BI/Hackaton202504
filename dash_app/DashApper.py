import dash
from dash import dcc, html, Input, Output, State, ctx
import psycopg2
import hashlib
from datetime import datetime, timezone

app = dash.Dash(__name__)

def get_db_connection():
    return psycopg2.connect(
        host="10.5.185.53",
        dbname="shooca_db",
        user="shooca",
        password="shooca222",
        port="5432"
    )

def format_elapsed_time(timestamp_str):
    ts = datetime.fromisoformat(timestamp_str)
    if ts.tzinfo is None:
        ts = ts.replace(tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    diff = now - ts
    total_seconds = int(diff.total_seconds())
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes:02d}:{seconds:02d} ago"


ACTION_STYLE = {
    'backgroundColor': '#ffffff',
    'borderRadius': '15px',
    'boxShadow': '0 6px 12px rgba(0,0,0,0.1)',
    'padding': '25px 40px',
    'flex': '1 1 250px',
    'minWidth': '250px',
    'fontSize': '28px',
    'fontWeight': '600',
    'color': '#2a4365',
    'textAlign': 'center',
    'transition': 'background-color 0.3s ease, box-shadow 0.3s ease',
    'userSelect': 'none',
    'cursor': 'default',
}

# Layout
app.layout = html.Div([
    # html.H1("Live IRC Chat Activity", style={
    #     'textAlign': 'center',
    #     'marginBottom': '40px',
    #     'fontSize': '48px',
    #     'fontWeight': '900',
    #     'fontFamily': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    #     'color': '#222',
    #     'textShadow': '0 1px 3px rgba(0,0,0,0.1)'
    # }),

    html.Div([
        html.H2("Match Effectors:", style={
            'fontWeight': '700',
            'fontSize': '24px',
            'marginBottom': '20px',
            'color': '#444'
        }),
        html.Div(id='entity-message', style={
            'fontSize': '28px',
            'fontWeight': '700',
            'color': '#0B5394',
            'marginBottom': '25px',
            'minHeight': '40px',
            'letterSpacing': '0.05em'
        }),
    ], style={
        'padding': '0 30px',
        'borderBottom': '2px solid #ccc',
        'marginBottom': '30px'
    }),

    html.Div([
        html.Div(id='action1-message', style=ACTION_STYLE),
        html.Div(id='action2-message', style=ACTION_STYLE),
        html.Div(id='action3-message', style=ACTION_STYLE),
    ], style={
        'display': 'flex',
        'justifyContent': 'space-around',
        'marginBottom': '50px',
        'gap': '20px',
        'flexWrap': 'wrap',
        'padding': '0 30px'
    }),

    html.Div(id='latest-message', style={
        'fontSize': '18px',
        'fontStyle': 'italic',
        'color': '#666',
        'textAlign': 'center',
        'marginBottom': '40px',
        'minHeight': '30px',
        'fontFamily': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
    }),

    html.Div(id='history-buttons', style={
        'textAlign': 'center',
        'padding': '10px 20px',
        'maxWidth': '800px',
        'margin': '0 auto',
        'display': 'flex',
        'flexWrap': 'wrap',
        'justifyContent': 'center',
        'gap': '15px'
    }),

    dcc.Store(id='stored-messages'),
    dcc.Store(id='selected-index', data=0),
    dcc.Store(id='messages-hash', data=''),

    dcc.Interval(id='interval-component', interval=1000, n_intervals=0)
], style={
    'backgroundColor': '#f5f8fa',
    'border': '1px solid #ddd',
    'borderRadius': '20px',
    'padding': '40px 20px 60px 20px',
    'margin': '40px auto',
    'maxWidth': '960px',
    'boxShadow': '0 8px 30px rgba(0,0,0,0.12)',
    'fontFamily': "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    'color': '#333',
})

# Style for action boxes
ACTION_STYLE = {
    'backgroundColor': '#ffffff',
    'borderRadius': '15px',
    'boxShadow': '0 6px 12px rgba(0,0,0,0.1)',
    'padding': '25px 40px',
    'flex': '1 1 250px',
    'minWidth': '250px',
    'fontSize': '28px',
    'fontWeight': '600',
    'color': '#2a4365',
    'textAlign': 'center',
    'transition': 'background-color 0.3s ease, box-shadow 0.3s ease',
    'userSelect': 'none',
    'cursor': 'default',
}

def get_latest_messages():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT distinct on (timestamp) timestamp, entity, action1, action2, action3, message
        FROM mef_data
        ORDER BY timestamp DESC
        LIMIT 5
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    messages = [{
        'timestamp': str(r[0]),
        'entity': r[1],
        'action1': r[2],
        'action2': r[3],
        'action3': r[4],
        'message': r[5]
    } for r in rows]
    return messages

# Callback A: Only update messages and buttons if messages changed
@app.callback(
    Output('stored-messages', 'data'),
    Output('messages-hash', 'data'),
    Output('history-buttons', 'children', allow_duplicate=True),
    Input('interval-component', 'n_intervals'),
    State('messages-hash', 'data'),
    prevent_initial_call='initial_duplicate'
)
def maybe_update_messages(n, current_hash):
    messages = get_latest_messages()
    hash_str = hashlib.md5(''.join(m['timestamp'] for m in messages).encode()).hexdigest()

    if hash_str == current_hash:
        raise dash.exceptions.PreventUpdate

    buttons = []
    for i, m in enumerate(messages):
        elapsed = format_elapsed_time(m['timestamp'])
        label = f"{m['entity']} ({elapsed})"
        if i == 0:
            label += " (most recent)"
        buttons.append(
            html.Button(label, id={'type': 'history-button', 'index': i}, n_clicks=0, style=BUTTON_STYLE)
        )
    return messages, hash_str, buttons

# Callback B: Handle selection from button click
@app.callback(
    Output('selected-index', 'data'),
    Input({'type': 'history-button', 'index': dash.ALL}, 'n_clicks'),
    State('selected-index', 'data'),
    prevent_initial_call=True
)
def update_selected(n_clicks, current_index):
    triggered = ctx.triggered_id
    if isinstance(triggered, dict) and 'index' in triggered:
        return triggered['index']
    return current_index

# Callback C: Display selected message + highlight active button
@app.callback(
    Output('entity-message', 'children'),
    Output('action1-message', 'children'),
    Output('action2-message', 'children'),
    Output('action3-message', 'children'),
    Output('latest-message', 'children'),
    Output('history-buttons', 'children'),
    Input('stored-messages', 'data'),
    Input('selected-index', 'data'),
    prevent_initial_call=True
)
def show_selected_message(messages, selected_index):
    if not messages or selected_index >= len(messages):
        return "", "", "", "", "No message available", dash.no_update

    msg = messages[selected_index]
    buttons = []
    for i, m in enumerate(messages):
        elapsed = format_elapsed_time(m['timestamp'])
        label = f"{m['entity']} ({elapsed})"
        if i == 0:
            label += " (most recent)"
        # Active button green, others gray with hover effect
        color = '#4CAF50' if i == selected_index else '#e1e1e1'
        hover_bg = '#45a049' if i == selected_index else '#d5d5d5'
        buttons.append(
            html.Button(label, id={'type': 'history-button', 'index': i}, n_clicks=0, style={
                **BUTTON_STYLE,
                'backgroundColor': color,
                'transition': 'background-color 0.3s ease',
                'border': i == selected_index and '2px solid #388e3c' or '2px solid #ccc',
            })
        )

    return (
        msg['entity'],
        msg['action1'],
        msg['action2'],
        msg['action3'],
        f"Latest Message: {msg['message']}",
        buttons
    )

# Base style for buttons with hover via CSS trick (since Dash inline styles can't do :hover, we add a stylesheet below)
BUTTON_STYLE = {
    'margin': '5px',
    'padding': '12px 28px',
    'backgroundColor': '#e1e1e1',
    'borderRadius': '8px',
    'border': '2px solid #ccc',
    'cursor': 'pointer',
    'fontWeight': '600',
    'fontSize': '16px',
    'color': '#333',
    'boxShadow': '0 2px 5px rgba(0,0,0,0.1)',
    'userSelect': 'none',
    'transition': 'background-color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease'
}

# Add CSS for hover effects globally via external stylesheet
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Live IRC Chat Activity</title>
        {%favicon%}
        {%css%}
        <style>
            button:hover {
                background-color: #d5d5d5 !important;
                border-color: #999 !important;
                box-shadow: 0 4px 10px rgba(0,0,0,0.15) !important;
            }
            button:focus {
                outline: none;
                border-color: #4CAF50 !important;
                box-shadow: 0 0 10px #4CAF50 !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
