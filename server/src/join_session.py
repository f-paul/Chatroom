import pickle
import src.handle_flag as handle_flag

payload_type = handle_flag.payload_type
history = handle_flag.history
broadcast = handle_flag.broadcast

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
    print("{} join the chatroom.".format(obj["USERNAME"]))
    return payload