import src.handle_flag as handle_flag

payload_type = handle_flag.payload_type
history = handle_flag.history

MAX_USERS = 3

def join_session(obj, nicknames, clients, client):
    payload = payload_type.copy()

    if (len(clients) >= MAX_USERS):
        payload["JOIN_REJECT_FLAG"] = 1
        payload["PAYLOAD"] = 'The server rejects the join request. The chatroom has reached its maximum capacity.'
        return payload
    if (obj["USERNAME"] in nicknames):
        payload["JOIN_REJECT_FLAG"] = 1
        payload["PAYLOAD"] = 'The server rejects the join request. Another user is using this username.'
        return payload
    payload["PAYLOAD"] = '\n'.join(map(str, history))
    payload["JOIN_ACCEPT_FLAG"] = 1
    nicknames.append(obj["USERNAME"])
    return payload