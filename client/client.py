import socket, threading, sys, pickle
from src.payload_type import payload_type
from src.attachment import upload_attachment
from src.handle_flag import handle_flag

host_name = socket.gethostname()
ip = socket.gethostbyname(host_name)
SERVER_STATUS = False
IS_CONNECTED = False

def start_menu():
    print("Please select one of the following options:")
    print("\t 1. Get a report of the chatroom from the server.")
    print("\t 2. Request to join the chatroom.")
    print("\t 3. Quit the program.")
    choice = input("Your choice: ")
    return choice

from src.connect import connect
from src.connect import join_server
from src.report import get_report
from src.session import quit_session

def receive(client):
    global IS_CONNECTED

    while IS_CONNECTED:
        try:
            data = client.recv(1024)
            receive_obj = pickle.loads(data)
            if not handle_flag(receive_obj):
                IS_CONNECTED = False
        except:
            print("An error occured!")
            client.close()
            break

def write(client):
    global IS_CONNECTED
    while IS_CONNECTED:
        user_input = input('')
        if (user_input.lower() == 'q'):
            client.sendall(quit_session())
            break
        elif (user_input.lower() == 'a'):
            filename = input("Please enter the file path and name: ")
            client.sendall(upload_attachment(filename))
        else:
            payload = payload_type.copy()
            payload["PAYLOAD"] = '{}'.format(user_input)
            payload["PAYLOAD_LENGTH"] = len(payload["PAYLOAD"])
            client.sendall(pickle.dumps(payload))

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
            if not join_server(client):
                continue
            IS_CONNECTED = True
            receive_thread = threading.Thread(target=receive, args=(client, ))
            receive_thread.start()
            write_thread = threading.Thread(target=write, args=(client, ))
            write_thread.start()
        elif (choice == '3'):
            client.close()
            break
        else:
            print("Invalid choice. Please try again.")
            continue