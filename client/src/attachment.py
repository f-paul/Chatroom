import pickle
from src.payload_type import payload_type

def upload_attachment(filename):
    payload = payload_type.copy()
    try:
        payload["PAYLOAD"] = open(filename, 'r').read()
        payload["ATTACHMENT_FLAG"] = 1
        payload["ATTACHMENT_FILENAME"] = filename
        payload["PAYLOAD_LENGTH"] = len(payload["PAYLOAD"])
        return pickle.dumps(payload)
    except:
        print("File not found!")
        return pickle.dumps(payload)
    
    