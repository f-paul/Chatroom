from handle_flag import payload_type, get_client_nickname

def report_request(obj, nicknames, clients):
    payload = payload_type.copy()
    client_len = len(clients)

    payload["REPORT_RESPONSE_FLAG"] = 1
    payload["NUMBER"] = client_len

    if (client_len <= 0):
        return payload

    payload["PAYLOAD"] = "There are {} users in the chatroom:\n".format(client_len)

    for index, client in enumerate(clients):
        host, port = client.getpeername()
        nickname = get_client_nickname(clients, nicknames)
        payload["PAYLOAD"] += "{}. {} at IP: {} and port: {}.\n".format(index + 1, nickname, host, port)
    return payload