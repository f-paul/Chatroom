import pickle
from src.payload_type import payload_type

def report_request():
    payload = payload_type.copy()
    payload["REPORT_REQUEST_FLAG"] = 1
    return pickle.dumps(payload)

def get_report(client):
    client.sendall(report_request())
    data = client.recv(1024)
    print(data)
    receive_obj = pickle.loads(data)
    print(receive_obj["PAYLOAD"])