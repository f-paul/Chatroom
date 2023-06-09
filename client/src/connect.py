import socket, sys
import pickle
from src.session import join_session
import src.handle_flag as handle_flag

host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
PORT = 18000

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((ip, PORT))
    except:
        print('The server cannot accept the connection.')
        client.close()
        sys.exit()
    return client

def join_server(client):
    nickname = input("Please enter a username: ")
    handle_flag.nickname = nickname
    client.sendall(join_session(nickname))
    data = client.recv(1024)
    payload = pickle.loads(data)
    if (payload["JOIN_REJECT_FLAG"] == 1):
        print(payload["PAYLOAD"])
        return False
    print("The server welcomes you to the chatroom.")
    print("Type lowercase 'q' and press enter at any time to quit the chatroom.")
    print("Type lowercase 'a' and press enter at any time to upload an attachment to the chatroom.")
    print("Here is a history of the chatroom.")
    print(payload["PAYLOAD"])
    return True
    
