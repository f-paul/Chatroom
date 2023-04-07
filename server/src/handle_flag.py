import pickle, time

MAX_USERS = 3

payload_type = {
    "REPORT_REQUEST_FLAG": 0,
    "REPORT_RESPONSE_FLAG": 0,
    "JOIN_REQUEST_FLAG": 0,
    "JOIN_REJECT_FLAG": 0,
    "JOIN_ACCEPT_FLAG": 0,
    "NEW_USER_FLAG": 0,
    "QUIT_REQUEST_FLAG": 0,
    "QUIT_ACCEPT_FLAG": 0,
    "ATTACHMENT_FLAG": 0,
    "NUMBER": 0,
    "USERNAME": "",
    "FILENAME": "",
    "PAYLOAD_LENGTH": 0,
    "PAYLOAD": "",
    "TIME": ""
}

history = []

def format_payload(payload):
    current_time = time.strftime("[%H:%M:%S]", time.localtime())
    payload["PAYLOAD"] = '{} {}'.format(current_time, payload["PAYLOAD"])
    payload["PAYLOAD_LENGTH"] = len(payload["PAYLOAD"])
    return payload

def broadcast(data, clients):
    data = format_payload(data)
    save_payload(data["PAYLOAD"])
    print('envoie')
    print(data)         
    for client in clients:
        client.sendall(pickle.dumps(data))

def save_payload(payload):
    history.append(payload)

def get_client_nickname(clients, nicknames, client):
    index = clients.index(client)
    nickname = nicknames[index]
    return nickname

from src.join_session import join_session
from src.new_user import new_user
from src.report_session import report_session

def quit_session(obj, nicknames, clients, client):
    payload = payload_type.copy()
    nickname = get_client_nickname(clients, nicknames, client)
    payload["QUIT_ACCEPT_FLAG"] = 1
    payload["USERNAME"] = nickname
    payload["PAYLOAD"] = "Server: {} left the chatroom.".format(nickname)
    nicknames.remove(nickname)
    clients.remove(client)
    broadcast(payload, clients)
    print("{} left the chatroom.".format(nickname))
    return payload

funcdict = {
    "JOIN_REQUEST_FLAG": join_session,
    "NEW_USER_FLAG": new_user,
    "REPORT_REQUEST_FLAG": report_session,
    "QUIT_REQUEST_FLAG": quit_session,
}

def handle_flag(obj, nicknames, clients, client):
    for key in obj:
        if (key in funcdict and obj[key] == 1):
            return funcdict[key](obj, nicknames, clients, client)
    else:
        broadcast(obj, clients)
