
import src.utils as utils
from src.payload_type import payload_type

get_client_nickname = utils.get_client_nickname
broadcast = utils.broadcast

def new_user(obj, nicknames, clients, client):
    payload = payload_type.copy()
    payload["PAYLOAD"] = "Server: {} joined the chatroom.".format(get_client_nickname(clients, nicknames, client))
    broadcast(payload, clients, nicknames, client)
    return payload