from datetime import datetime
def getNowTS():
    time = datetime.utcnow().strftime("%m/%d/%Y, %H:%M:%S")
    return time