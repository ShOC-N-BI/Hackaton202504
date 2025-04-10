import pandas as pd
import socket
import json

HOST = "10.10.26.105"
PORT = 5001

def process_data(data):
    print(data)
    # Example: Parse JSON data
    try:
        jsondata = json.loads(data.decode('utf-8'))
        # Add your data processing logic here
        # For example, you can convert lat/lon to radians for haversine calculation
        # bc3_coords = np.radians([jsondata['e1.latitude'], jsondata['e1.longitude']])
        # Build KDTree for BC3 coords
        # tree = cKDTree(bc3_coords)
        # print("KDTree built")
        # Query nearest BC3 point for each chat message
        # distances, indices = tree.query([25.045310306035184, -77.464458773165], k=1)
        # print("Query complete")
        print(f"bc3 data: {jsondata}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")

def read_file_in_chunks(sock, chunk_size=1024):
    buffer = b''
    while True:
        chunk = sock.recv(chunk_size)
        if not chunk:
            # Process remaining data in buffer
            if buffer:
                for line in buffer.splitlines(True):
                    print(line.decode('utf-8'), end='')
            break
        buffer += chunk
        while b'\n' in buffer:
            line, buffer = buffer.split(b'\n', 1)
            process_data(line.decode('utf-8') + '\n')


udpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
udpSocket.setsockopt(socket.INADDR_ANY, socket.SO_REUSEADDR, 1)
udpSocket.bind((HOST, PORT))
#udpSocket.connect((HOST, PORT))

read_file_in_chunks(udpSocket)

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
#     try:
#         sock.bind((HOST, PORT))
#         sock.listen()
#         print(f"Listening on {HOST}:{PORT}")
#         client_socket, client_address = sock.accept()
#         with client_socket:
#             print(f"Connection from {client_address}")
#             read_file_in_chunks(client_socket)
#     except socket.error as e:
#         print(f"Socket error: {e}")