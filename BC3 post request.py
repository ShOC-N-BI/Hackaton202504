import requests

# Define the IP address and port
ip = '10.10.26.105'
port = 5001
url = f'http://{ip}:{port}/endpoint'
json_example = {{"timestamp":1743460227.137,"trackNumber":63167,"e1.x":1364250.532317,"e1.y":-5385345.283277,"e1.z":3137517.270935,"e1.latitude":29.62103596,"e1.longitude":-75.78451583,"e1.altitude":7268.678,"e1.xdot":153.944293,"e1.ydot":-80.162111,"e1.zdot":-203.163249,"e1.velocityEast":129.54500888,"e1.velocityNorth":-233.70538249,"e1.velocityUp":0.00000021,"e1.groundSpeed":267.2080,"e1.heading":151.0000,"e1.trackQuality":11,"e1.category":"Air","e1.is3d":true,"e1.isDeadReckon":false,"e1.trackId":"Friend","e1.specificType":0,"e1.platform":1,"e1.activity":0,"e1.timestampMicro":136934,"e8.mode4":0,"e11.isSimulated":false,"e11.isEmergency":false,"e11.isSpecialProcessing":false,"e11.isFlightPlan":false,"e11.isExercise":false,"e11.isManeuver":false,"e11.isTest":false,"e11.isNonRealTime":false,"e15.sourceId":4294967295,"e18.a1":897.524576,"e18.a2":125.393096,"e18.a3":-73.546156,"e18.a4":0.000000,"e18.a5":0.000000,"e18.a6":0.000000,"e18.b2":434.303817,"e18.b3":290.321633,"e18.b4":0.000000,"e18.b5":0.000000,"e18.b6":0.000000,"e18.c3":759.009141,"e18.c4":0.000000,"e18.c5":0.000000,"e18.c6":0.000000,"e18.d4":232.257600,"e18.d5":0.000000,"e18.d6":-0.000000,"e18.e5":232.257600,"e18.e6":0.000000,"e18.f6":232.257600}]}
# Send a GET request
response = requests.get(url)

# Print the status code and response body
print(f"Status Code: {response.status_code}")

# BC3 will return a JJSON object with the following structure: refere to Json example. 

# Track number,e1.category, e1.trackId, e12.callsign

#push data from BC3 to dash app. 


