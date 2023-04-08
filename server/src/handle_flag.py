from src.session import join_session
from src.session import quit_session
from src.session import report_session
from src.new_user import new_user
from src.utils import broadcast
from src.attachment import attachment

funcdict = {
    "JOIN_REQUEST_FLAG": join_session,
    "NEW_USER_FLAG": new_user,
    "REPORT_REQUEST_FLAG": report_session,
    "QUIT_REQUEST_FLAG": quit_session,
    "ATTACHMENT_FLAG": attachment,
}

def handle_flag(obj, nicknames, clients, client):
    for key in obj:
        if (key in funcdict and obj[key] == 1):
            return funcdict[key](obj, nicknames, clients, client)
    else:
        broadcast(obj, clients, nicknames, client)
