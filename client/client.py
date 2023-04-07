import socket, threading, sys, pickle
from src.payload_type import payload_type

host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
SERVER_STATUS = False
IS_CONNECTED = False
STOP_EVENT = threading.Event()

def start_menu():
    print("Please select one of the following options:")
    print("\t 1. Get a report of the chatroom from the server.")
    print("\t 2. Request to join the chatroom.")
    print("\t 3. Quit the program.")
    choice = input("Your choice: ")
    return choice

# def connect():
#     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         client.connect((ip, PORT))
#     except:
#         print('The server cannot accept the connection.')
#         client.close()
#         sys.exit()
#     return client

from src.connect import connect
from src.connect import join_server
from src.report import get_report
from src.session import quit_session

def send_chat(message):
    payload = payload_type.copy()
    payload["PAYLOAD"] = message
    payload["PAYLOAD_LENGTH"] = len(payload["PAYLOAD"])
    return pickle.dumps(payload)

def receive(client):
    while not STOP_EVENT.is_set():
        try:
            data = client.recv(1024)
            receive_obj = pickle.loads(data)
            message = receive_obj["PAYLOAD"]
            print(message)
        except:
            print("An error occured!")
            client.close()
            break

def write(client, nickname):
    global IS_CONNECTED
    while not STOP_EVENT.is_set():
        user_input = input('')
        if (user_input.lower() == 'q'):
            client.sendall(quit_session())
            STOP_EVENT.set()
            IS_CONNECTED = False
            break
        # todo: refactor this to handle all cases
        message = '{}: {}'.format(nickname, user_input)
        client.sendall(send_chat(message))

if __name__ == "__main__":
    client = connect()
    while True:
        if (IS_CONNECTED == True):
            continue
        choice = start_menu()
        if (choice == '1'):
            get_report(client)
            IS_CONNECTED = False
        elif (choice == '2'):
            nickname = join_server(client)
            IS_CONNECTED = True
            receive_thread = threading.Thread(target=receive, args=(client, ))
            receive_thread.start()
            write_thread = threading.Thread(target=write, args=(client, nickname, ))
            write_thread.start()
        elif (choice == '3'):
            STOP_EVENT.set()
            break