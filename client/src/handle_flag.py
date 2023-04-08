nickname = ""

def handle_flag(receive_obj):
    if (receive_obj["QUIT_ACCEPT_FLAG"] == 1 and receive_obj["USERNAME"] == nickname):
        return False
    if (receive_obj["ATTACHMENT_FLAG"] == 1):
        try:
            file = open(receive_obj["ATTACHMENT_FILENAME"], "w")
            file.write(receive_obj["PAYLOAD"])
            file.close()
            return True
        except Exception as e:
            print("An error occured while saving the file!")
            return True
    message = receive_obj["PAYLOAD"]
    print(message)
    return True