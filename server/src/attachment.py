import src.utils as utils
import pickle
from src.payload_type import payload_type

broadcast = utils.broadcast

def attachment(obj, nicknames, clients, client):
    payload = payload_type.copy()

    filename = './download/' + obj["ATTACHMENT_FILENAME"].replace('attachments/', '')
    file = open(filename, "w")
    file.write(obj["PAYLOAD"])
    file.close()
    payload["PAYLOAD"] = obj["PAYLOAD"]
    payload["PAYLOAD_LENGTH"] = len(payload["PAYLOAD"])
    broadcast(payload, clients, nicknames, client)
    
    payload = payload_type.copy()
    payload["ATTACHMENT_FLAG"] = 1
    payload["ATTACHMENT_FILENAME"] = filename
    payload["PAYLOAD"] = obj["PAYLOAD"]
    payload["PAYLOAD_LENGTH"] = len(payload["PAYLOAD"])
    for c in clients:
        c.sendall(pickle.dumps(payload))
    return payload