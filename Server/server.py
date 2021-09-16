import socket
from _thread import *
from game import Game
import pickle
from Client.player import *

server = "192.168.0.106"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print('Not binded correctly',e)

s.listen(2)
print("Waiting for connection. Server started")

connected = set()
games = {}
id_count = 0

def threaded_client(conn, p, game_id):
    global id_count
    conn.send(str.encode(str(p)))
    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()
            if game_id in games:
                game = games[game_id]
                if not data:
                    break
                else:
                    if data == 'reset':
                        game.reset_moves()
                    elif data != 'get':
                        game.play(p,data)
                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break
    print("Lost connection")
    try:
        del games[game_id]
        print("Closing the game", game_id)

    except:
        pass
    id_count -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    # new person joined the game
    id_count += 1
    p = 0
    game_id = (id_count - 1) // 2
    if id_count % 2 ==1:
        games[game_id] = Game(game_id)
        print ("Creating new game...")
    else:
        games[game_id].ready = True
        p = 1
    start_new_thread(threaded_client, (conn,p,game_id))












# print("Waiting for connection.Server started")
# players = [Player(0, 0, 50,50,(255,0,0)), Player(100, 100, 50,50,(0,255,0))]
# print(players)
# def threaded_client(conn, player):
#     #  when the connection is estavblished for the first time - server sends initial position of the player
#     data_curr_player = pickle.dumps(players[player])
#     print(pickle.loads(data_curr_player))
#     conn.send(data_curr_player)
#     while True:
#         try:
#             # from client the server receives its position, for ex. player1 sends its position
#             # server uses this information to update pos
#             # and sends the position of other player (player0 ) to player1
#             data = pickle.loads(conn.recv(2048))
#             players[player] = data
#             # reply = data.decode('utf-8')
#             if not data:
#                 print('Disconnected')
#                 break
#             else:
#                 # after the initialconnection the server always send the
#                 # position of player1 to player 0 and visa versa
#
#                 if player == 1:
#                     reply = players[0]
#                 else:
#                     reply = players[1]
#                 # print('Received from player ', player, data)
#                 # print('Sending to player:',player, reply)
#             conn.sendall(pickle.dumps(reply))
#         except:
#             break
#     print('Lost connection')
#     conn.close()
#
#
# current_player = 0
# while True:
#     conn, addr = s.accept()
#     print(f"connected to {addr} with conn {conn}, You are player {current_player}")
#     start_new_thread(threaded_client, (conn, current_player))
#     current_player += 1