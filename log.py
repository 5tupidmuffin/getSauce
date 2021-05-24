from datetime import datetime

def logit(message):
    print("logger ---> " + message)  # print message to console
    with open('log.txt', 'a') as logfile:
        logfile.write(f"{datetime.now().strftime('%d-%m-%Y %H:%M:%S')} - {message} \n")  # save message to log file
