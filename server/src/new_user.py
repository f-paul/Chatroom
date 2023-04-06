import src.handle_flag as handle_flag

payload_type = handle_flag.payload_type
get_client_nickname = handle_flag.get_client_nickname

def new_user(obj, nicknames, clients):
    payload = payload_type.copy()
    payload["PAYLOAD"] = "{} joined the chatroom.".format(get_client_nickname(clients, nicknames, client))
    return payload