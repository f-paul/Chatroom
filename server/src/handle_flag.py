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

def save_payload(payload):
    history.append(payload)

def get_client_nickname(clients, nicknames, client):
    index = clients.index(client)
    nickname = nicknames[index]
    return nickname

def report_request(obj, nicknames, clients, client):
    payload = payload_type.copy()
    client_len = len(clients) - 1


    payload["REPORT_RESPONSE_FLAG"] = 1
    payload["NUMBER"] = client_len
    payload["PAYLOAD"] = "There are {} users in the chatroom:\n".format(client_len)

    if (client_len <= 0):
        return payload

    print(client_len, nicknames, len(clients))

    for idx, c in enumerate(clients[:-1]):
        host, port = c.getpeername()
        nickname = get_client_nickname(clients, nicknames, c)
        payload["PAYLOAD"] += "{}. {} at IP: {} and port: {}.\n".format(idx + 1, nickname, host, port)

    return payload

from src.join_session import join_session
from src.new_user import new_user

funcdict = {
    "JOIN_REQUEST_FLAG": join_session,
    "NEW_USER_FLAG": new_user,
    "REPORT_REQUEST_FLAG": report_request
}

def handle_flag(obj, nicknames, clients, client):
    print(obj)
    for key in obj:
        if (key in funcdict and obj[key] == 1):
            return funcdict[key](obj, nicknames, clients, client)
    else:
        save_payload(obj["PAYLOAD"])
        return obj
