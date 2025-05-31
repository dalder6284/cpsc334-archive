import socket
import struct
import select
import time
from pythonosc.udp_client import SimpleUDPClient

sc_ip = "127.0.0.1"
sc_port = 57120
sc_client = SimpleUDPClient(sc_ip, sc_port)

mostRecentChange = time.time()
mostRecentChill = time.time()
curr = "N1"

def moveUp():
    global curr
    global mostRecentChange
    if curr == "B1":
        curr = "M1"
    elif curr == "N1":
        curr = "M1"
    elif curr == "M1":
        curr = "M2"
    elif curr == "M2":
        curr = "M3"
    
def moveDown():
    global curr
    global mostRecentChange
    if curr == "M1":
        curr = "N1"
    elif curr == "M2":
        curr = "M1"
    elif curr == "M3":
        curr = "M2"

def parse_data(data):
    global curr
    global mostRecentChange
    limit = 800
    ax, ay, az, gx, gy, gz, sponge = data
    onside = (ay < 9.0) and (ay > -5)
    usd = (ay < -8)
    shaken = (abs(gx) > 2.5) or (abs(gy) > 2.5) or (abs(gz) > 2.5)
    cool = not (onside or usd or shaken or sponge > limit)
    
    if curr == "B1" and 0 < sponge < limit:
        return
    
    now = time.time()
    if (now - mostRecentChange > 10):
        mostRecentChange = time.time()
        if sponge > 0 and sponge < limit and curr == "N1":
            curr = "B1"
            
            sc_client.send_message("/data", curr)
            return
        
        if sponge == 0 and curr == "B1":
            curr = "N1"
            
        if usd:
            curr = "M3"
        elif onside or shaken:
            moveUp()
        elif sponge > limit:
            moveUp()
        elif cool:
            moveDown()
            
        sc_client.send_message("/data", curr)

def start_server(host='0.0.0.0', port=8090, timeout=20):
    global curr
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {host}:{port}")

    clients = {}
    
    try:
        while True:
            read_sockets, _, _ = select.select([server_socket] + list(clients.keys()), [], [])

            current_time = time.time()
            for sock in list(clients.keys()):
                if current_time - clients[sock] > timeout:
                    print(f"[TIMEOUT] {sock.getpeername()} has timed out.")
                    sock.close()
                    del clients[sock]

            for sock in read_sockets:
                if sock is server_socket:
                    client_socket, addr = server_socket.accept()
                    clients[client_socket] = current_time
                    print(f"[NEW CONNECTION] {addr} connected.")
                else:
                    try:
                        data = sock.recv(1024)
                        if data:
                            if len(data) == 26:
                                unpacked_data = struct.unpack('ffffffh', data)
                                print(f"[RECEIVED] {unpacked_data} from {sock.getpeername()}")
                                parse_data(unpacked_data)
                                clients[sock] = current_time
                            else:
                                raise ConnectionResetError
                        else:
                            raise ConnectionResetError
                    except (ConnectionResetError, BrokenPipeError):
                        print(f"[DISCONNECTED] {sock.getpeername()} disconnected.")
                        sock.close()
                        del clients[sock]

    except KeyboardInterrupt:
        print("[SHUTTING DOWN] Server is shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
