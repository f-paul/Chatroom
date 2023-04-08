import pickle, time

history = []

def format_payload(payload, nicknames, clients, client):
    current_time = time.strftime("[%H:%M:%S]", time.localtime())
    nickname = get_client_nickname(clients, nicknames, client)
    if (payload["QUIT_ACCEPT_FLAG"] == 1):
        nickname = "Server"
    payload["PAYLOAD"] = '{} {}: {}'.format(current_time, nickname, payload["PAYLOAD"])
    payload["PAYLOAD_LENGTH"] = len(payload["PAYLOAD"])
    return payload

def get_client_nickname(clients, nicknames, client):
    index = clients.index(client)
    nickname = nicknames[index]
    return nickname

def broadcast(data, clients, nicknames, client):
    if data["PAYLOAD_LENGTH"] == 0 and data["QUIT_ACCEPT_FLAG"] == 0:
        return
    data = format_payload(data, nicknames, clients, client)
    history.append(data["PAYLOAD"])
    print('Sending to clients:')
    print(data)
    for c in clients:
        c.sendall(pickle.dumps(data))