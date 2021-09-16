import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.106"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()
        # print('self.p', self.p)
        # print("Received from server initial position", self.p)
    
    def get_p(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            # raw_data = self.client.recv(2048)
            # print('raw_data',raw_data)
            return self.client.recv(2048).decode()
        except:
            return ("Smth wrong")
            pass
    
    def send(self, data):
        try:
            # self.client.send(pickle.dumps(data))
            # we are sending the string but receiving pbject
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as error:
            print(error)





