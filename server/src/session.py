import pickle
import src.utils as utils
from src.payload_type import payload_type

history = utils.history
broadcast = utils.broadcast
get_client_nickname = utils.get_client_nickname

MAX_USERS = 3

def join_session(obj, nicknames, clients, client):
    payload = payload_type.copy()

    if (len(nicknames) >= MAX_USERS):
        payload["JOIN_REJECT_FLAG"] = 1
        payload["PAYLOAD"] = 'The server rejects the join request. The chatroom has reached its maximum capacity.'
        client.sendall(pickle.dumps(payload))
        return payload
    if (obj["USERNAME"] in nicknames):
        payload["JOIN_REJECT_FLAG"] = 1
        payload["PAYLOAD"] = 'The server rejects the join request. Another user is using this username.'
        client.sendall(pickle.dumps(payload))
        return payload
    payload["PAYLOAD"] = '\n'.join(map(str, history))
    payload["JOIN_ACCEPT_FLAG"] = 1
    nicknames.append(obj["USERNAME"])
    client.sendall(pickle.dumps(payload))
    nickname = "{} join the chatroom.".format(obj["USERNAME"])
    print(nickname)
    payload = payload_type.copy()
    payload["NEW_USER_FLAG"] = 1
    payload["USERNAME"] = obj["USERNAME"]
    payload["PAYLOAD"] = nickname
    broadcast(payload, clients, nicknames, client)
    return payload

def quit_session(obj, nicknames, clients, client):
    payload = payload_type.copy()
    nickname = get_client_nickname(clients, nicknames, client)
    payload["QUIT_ACCEPT_FLAG"] = 1
    payload["USERNAME"] = nickname
    payload["PAYLOAD"] = "{} left the chatroom.".format(nickname)
    broadcast(payload, clients, nicknames, client)
    nicknames.remove(nickname)
    print("{} left the chatroom.".format(nickname))
    return payload

def report_session(obj, nicknames, clients, client):
    payload = payload_type.copy()
    client_len = len(nicknames)

    payload["REPORT_RESPONSE_FLAG"] = 1
    payload["NUMBER"] = client_len
    payload["PAYLOAD"] = "There are {} users in the chatroom".format(client_len)

    if (client_len <= 0):
        payload["PAYLOAD"] += "."
        client.sendall(pickle.dumps(payload))
        return payload

    payload["PAYLOAD"] += ":\n"
    for idx, c in enumerate(clients[:-1]):
        host, port = c.getpeername()
        nickname = get_client_nickname(clients, nicknames, c)
        payload["PAYLOAD"] += "{}. {} at IP: {} and port: {}.\n".format(idx + 1, nickname, host, port)
    client.sendall(pickle.dumps(payload))
    return payload