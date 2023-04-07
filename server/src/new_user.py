import src.handle_flag as handle_flag

payload_type = handle_flag.payload_type
get_client_nickname = handle_flag.get_client_nickname
broadcast = handle_flag.broadcast

def new_user(obj, nicknames, clients, client):
    payload = payload_type.copy()
    payload["PAYLOAD"] = "Server: {} joined the chatroom.".format(get_client_nickname(clients, nicknames, client))
    broadcast(payload)
    return payload