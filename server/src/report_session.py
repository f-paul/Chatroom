import pickle
import src.handle_flag as handle_flag

payload_type = handle_flag.payload_type
get_client_nickname = handle_flag.get_client_nickname
broadcast = handle_flag.broadcast

def report_session(obj, nicknames, clients, client):
    payload = payload_type.copy()
    client_len = len(nicknames)

    payload["REPORT_RESPONSE_FLAG"] = 1
    payload["NUMBER"] = client_len
    payload["PAYLOAD"] = "There are {} users in the chatroom".format(client_len)

    if (client_len <= 0):
        payload["PAYLOAD"] += ".\n"
        client.sendall(pickle.dumps(payload))
        return payload

    payload["PAYLOAD"] += ":\n"
    for idx, c in enumerate(clients[:-1]):
        host, port = c.getpeername()
        nickname = get_client_nickname(clients, nicknames, c)
        payload["PAYLOAD"] += "{}. {} at IP: {} and port: {}.\n".format(idx + 1, nickname, host, port)
    client.sendall(pickle.dumps(payload))
    return payload