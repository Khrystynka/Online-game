import socket
from _thread import *
import sys

server = "192.168.0.106"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print('Not binded correctly',e)

s.listen(2)
print("Waiting for connection.Server started")

def read_pos(str):
    str = str.split(",")
    return (int(str[0]), int(str[1]))

def make_pos(tup):
    return str(tup[0])+','+str(tup[1])

pos = [(0,0), (100,100)]
def threaded_client(conn, player):
    #  when the connection is estavblished for the first time - server sends initial position of the player
    conn.send(str.encode(make_pos(pos[player])))
    while True:
        try:
            # from client the server receives its position, for ex. player1 sends its position 
            # server uses this information to update pos 
            # and sends the position of other player (player0 ) to player1
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data
            # reply = data.decode('utf-8')
            if not data:
                print('Disconnected')
                break
            else:
                # after the initialconnection the server always send the 
                # position of player1 to player 0 and visa versa
                
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                # print('Received from player ', player, data)
                # print('Sending to player:',player, reply)
            conn.sendall(str.encode(make_pos(reply)))
        except:
            break
    print('Lost connection')
    conn.close()
            

current_player = 0
while True:
    conn, addr = s.accept()
    print(f"connected to {addr} with conn {conn}, You are player {current_player}")
    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1