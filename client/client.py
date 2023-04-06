import socket, threading, sys, pickle
from payload_handling import send_chat, join_session, report_request

host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)

PORT = 18001
SERVER_STATUS = False

def start_menu():
    print("Please select one of the following options:")
    print("\t 1. Get a report of the chatroom from the server.")
    print("\t 2. Request to join the chatroom.")
    print("\t 3. Quit the program.")
    choice = input("Your choice: ")
    return choice

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
    nickname = input("Choose your nickname: ")
    client.sendall(join_session(nickname))
    print("The server welcomes you to the chatroom.")
    print("Type lowercase 'q' and press enter at any time to quit the chatroom.")
    print("Type lowercase 'a' and press enter at any time to upload an attachment to the chatroom.")
    data = client.recv(1024)
    receive_obj = pickle.loads(data)
    print("Here is a history of the chatroom.")
    print(receive_obj["PAYLOAD"])
    return nickname

def get_report(client):
    client.sendall(report_request())
    data = client.recv(1024)
    print(data)
    receive_obj = pickle.loads(data)
    print(receive_obj["PAYLOAD"])

def receive(client):
    while True:
        try:
            data = client.recv(1024)
            receive_obj = pickle.loads(data)
            # print(receive_obj)
            message = receive_obj["PAYLOAD"]
            time = receive_obj["TIME"]
            print('{} {}'.format(time, message))
        except:
            print("An error occured!")
            client.close()
            break

def write(client, nickname):
    while True:
        user_input = input('')
        message = '{}: {}'.format(nickname, user_input)
        client.sendall(send_chat(message))

if __name__ == "__main__":
    while True:
        if (SERVER_STATUS == True):
            continue
        choice = start_menu()
        client = connect()
        SERVER_STATUS = True
        if (choice == '1'):
            get_report(client)
        elif (choice == '2'):
            nickname = join_server(client)
            receive_thread = threading.Thread(target=receive, args=(client, ))
            receive_thread.start()
            write_thread = threading.Thread(target=write, args=(client, nickname, ))
            write_thread.start()
        elif (choice == '3'):
            break