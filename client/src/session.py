import pickle
from src.payload_type import payload_type

def join_session(username):
    payload = payload_type.copy()
    payload["USERNAME"] = username
    payload["JOIN_REQUEST_FLAG"] = 1
    return pickle.dumps(payload)

def quit_session():
    payload = payload_type.copy()
    payload["QUIT_REQUEST_FLAG"] = 1
    return pickle.dumps(payload)