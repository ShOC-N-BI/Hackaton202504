import asyncio
import aiohttp
import json
import psycopg2
import re
import requests
import time




class MessageManger:
    def __init__(
        self, api_url='http://10.5.101.181:31011',
        db_connect_config = {
            "host": "10.5.185.53",
            "dbname": "shooca_db",
            "user": "shooca",
            "password": "shooca222",
            "port": "5432"
        },
        queue_size = 5,
        context = "Commander’s Intent: Degrade adversary Anti-Access Area Denial (A2AD) capability in preparation for follow-on coastal strikes.  Allied Force Commander’s Guidance: Use reversible and non-reversible (up to and including deadly force) to neutralize adversary maritime and air assets while protecting civilians and preserving options for follow-on strikes: Objective (Pri 1a): Neutralize adversary surface combatants, Objective (Pri 1b): Destroy adversary air forces, Objective (Pri 2a): Assess adversary intent/strategy, and Objective (Pri 2b): Protect Civilians",
        entity_regex = r"(?P<track_number>\d+)\s*\(CallSign: (?P<callsign>[^,]+), Track Cat: (?P<track_cat>[^,]+), Track ID: (?P<track_id>[^,]+), Aircraft Type: (?P<aircraft_type>[^)]+)\)",
        key_columns = ("timestamp", "entity", "action1", "action2", "action3", "message")
    ):
        """
        """
        self.current_messages = {}
        self.api_queue = []

        self.api_url = api_url
        self.db_connect_config = db_connect_config

        self.queue_size = queue_size
        self.context = context
        self.entity_regex = entity_regex
        self.key_columns = key_columns

        # Boolean for killing our background function
        self.kill_background = False
        self.background_task = None
        pass

    async def _testTooltipService(self):
        # Example code of how to create a task out of the tooltip service.  Shouldn't really be using this
        self.background_task = asyncio.create_task(self.updateTooltips())
        await asyncio.sleep(60)

    async def sendAsyncPostRequest(self, url, data, headers=None):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=data, headers=headers) as response:
                    response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
                    json_obj = json.loads(await response.text())
                    return json_obj
            except aiohttp.ClientError as e:
                print(f"Error sending request: {e}")
                return None

    async def updateTooltips(self):
        """
        """
        while True:
            print(f"updateTooltips {len(self.api_queue)}")
            if len(self.api_queue) == 0:
                await asyncio.sleep(2)
            else:
                print(f"updateTooltips step : 1")
                # Check if the 
                r = None
                while r is None:
                    if len(self.api_queue) == 0:
                        print(f"updateTooltips step : 2")
                        break
                    else:
                        print(f"updateTooltips step : 3")
                        tmp = self.api_queue[0]
                        if self.check_tooltip(tmp):
                            r = tmp
                            break
                        else:
                            self.api_queue.remove(tmp)

                #print(f"next request to find : {r}")
                print(f"updateTooltips step : 10")
                ## Parse the weird input data from our database, and pass them to our AI
                tmp = r[r['action']]
                tmp = tmp.split(' | ')
                friendly = {
                    'callsign' : tmp[0], 
                    'aircraft_type' : tmp[1],
                    'armarments' : tmp[2],
                    'mission' : tmp[3]
                }
                action = tmp[3]
                message = r['message']
                tmp = r['entity']
                entity = {}
                match = re.findall(self.entity_regex, tmp)
                if match:
                    for m in match:
                        if m[0]: entity['track_number'] = m[0].strip()
                        if m[1]: entity['callsign'] = m[1].strip()
                        if m[2]: entity['track_cat'] = m[2].strip()
                        if m[3]: entity['track_id'] = m[3].strip()
                        if m[4]: entity['aircraft_type'] = m[4].strip()

                print(f"updateTooltips step : 20")

                post_data = {
                    "prompt": f"Command: Send {friendly} to {action} {entity}, based upon an irc message '{message}'.   Context: {self.context}.  Concisely determine which of the commanders objective this command accomplishes?"
                }
                print(post_data)
                custom_headers = {"Content-Type": "application/json", "Accept": "application/json"}
                url = self.api_url
                response_data = await self.sendAsyncPostRequest(self.api_url, post_data, custom_headers)
                if response_data:
                    # Retrieve our currnet message and update the correct tooltip
                    self.current_messages[r['key']][r['action'] + '_tooltip'] = response_data['response']
                    self.api_queue.remove(r)
                    print(f"Response: {response_data}")
                else:
                    print("POST request failed.")
                

    def get_db_connection(self):
        """
        """
        return psycopg2.connect(**self.db_connect_config)
    
    def get_latest_messages_as_array(self):
        """
        """
        results = [None for i in range(self.queue_size)]
        for m in self.current_messages.keys():
            results[self.current_messages[m]["row_number"]-1] = self.current_messages[m]
        return results
    def generate_key(self, msg_obj):
        """
        """
        return "".join([msg_obj[p] for p in self.key_columns])
    def get_latest_messages(self):
        """
        """
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute(f"""
            SELECT timestamp, entity, action1, action2, action3, message, row_number() over (order by timestamp DESC) as row_number
            FROM mef_data
            ORDER BY timestamp DESC
            LIMIT {self.queue_size}
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        new_keys = []
        # Append new messages to our dictionary
        for r in rows:
            m = {
                'timestamp': str(r[0]),
                'entity': r[1],
                'action1': r[2],
                'action1_tooltip': None,
                'action2': r[3],
                'action2_tooltip': None,
                'action3': r[4],
                'action3_tooltip': None,
                'message': r[5],
                'row_number': r[6]
            }
            key_val = self.generate_key(m)
            new_keys.append(key_val)

            if key_val not in self.current_messages:
                self.current_messages[key_val] = m
                for a in ('action1', 'action2', 'action3'):
                    self.api_queue.append({
                        'timestamp': m['timestamp'],
                        'entity': m['entity'],
                        'action': a,
                        a: m[a],
                        'message': m['message'],
                        'key': key_val
                    })

        # Delete any old messages from the current messages
        for m in self.current_messages.keys():
            if m not in new_keys:
                del self.current_messages[m]
        return self.get_latest_messages_as_array()

    def check_tooltip(self, request):
        """
        Check if the tooltip already exists, before calling the api
        """
        # If the message has been deleted, then return false
        print(f"check_tooltip step : 1")
        if request['key'] not in self.current_messages:
            print(f"check_tooltip step : 2")
            return False
        
        print(f"check_tooltip step : 3")
        message = self.current_messages[request['key']]
        # If the 
        if message[request['action'] + '_tooltip'] is not None:
            print(f"check_tooltip step : 4")
            return False
        print(f"check_tooltip step : 5")
        return True


async def main():
    messages = MessageManger(api_url='http://10.5.101.181:31012')
    messages.get_latest_messages()

    task = asyncio.create_task(messages.updateTooltips())
    await asyncio.sleep(60)
    task.cancel()
    try:
        await task # Await cancellation to ensure cleanup
    except asyncio.CancelledError:
        print("Background task cancelled.")
    
    print(f"messages.current_messages : {messages.current_messages} \n")
    print(f"messages.api_queue : {messages.api_queue}")


asyncio.run(main())