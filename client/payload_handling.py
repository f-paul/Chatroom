import pickle

payload_type = {
    "REPORT_REQUEST_FLAG": 0,
    "REPORT_RESPONSE_FLAG": 0,
    "JOIN_REQUEST_FLAG": 0,
    "JOIN_REJECT_FLAG": 0,
    "JOIN_ACCEPT_FLAG": 0,
    "NEW_USER_FLAG": 0,
    "QUIT_REQUEST_FLAG": 0,
    "QUIT_ACCEPT_FLAG": 0,
    "ATTACHMENT_FLAG": 0,
    "NUMBER": 0,
    "USERNAME": "",
    "FILENAME": "",
    "PAYLOAD_LENGTH": 0,
    "PAYLOAD": "",
    "TIME": ""
}

def send_chat(message):
    payload = payload_type.copy()
    payload["PAYLOAD"] = message
    payload["PAYLOAD_LENGTH"] = len(payload["PAYLOAD"])
    return pickle.dumps(payload)
    
def join_session(username):
    payload = payload_type.copy()
    payload["USERNAME"] = username
    payload["JOIN_REQUEST_FLAG"] = 1
    return pickle.dumps(payload)


def quit_session():
    payload = payload_type.copy()
    payload["QUIT_REQUEST_FLAG"] = 1
    return pickle.dumps(payload)

def report_request():
    payload = payload_type.copy()
    payload["REPORT_REQUEST_FLAG"] = 1
    return pickle.dumps(payload)