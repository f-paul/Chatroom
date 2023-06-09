import socket, threading, pickle  
from src.handle_flag import handle_flag                               

HOST_NAME = socket.gethostname()
IP_ADDRESS = socket.gethostbyname(HOST_NAME) 
PORT = 18000
MAX_USERS = 3                                                   

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)            
server.bind((IP_ADDRESS, PORT))                                         
server.listen(100)

print('Server is listening on {}:{}'.format(IP_ADDRESS, PORT))

clients = []
nicknames = []

def broadcast(data):                          
    for client in clients:
        client.sendall(pickle.dumps(data))

def handle(client):
    while True:
        try:
            data = client.recv(1024)
            received_obj = pickle.loads(data)
            print("Received object: ")
            print(received_obj)
            handle_flag(received_obj, nicknames, clients, client)
        except:                                                        
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            message = '{} left!'.format(nickname).encode('ascii')
            broadcast(message)
            nicknames.remove(nickname)
            break

def receive():                                                          
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))      
        clients.append(client)
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
receive()