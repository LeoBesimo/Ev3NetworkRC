import Controller
import socket
import threading
import time

host = '192.168.1.28'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

print(f"Started server with ip: {host}, port: {port}")

threshold = 1000
inputs = {Controller.InputMethods.LStickY: 0,
        Controller.InputMethods.RStickY: 0}

ctrlr = Controller.ControllerHandler()

client, address = server.accept()
print(f"Connected to adress: {address}")

def transmit():
    while True:
        try:
            client.send(f"{Controller.InputMethods.LStickY.name}:{inputs[Controller.InputMethods.LStickY]} {Controller.InputMethods.RStickY.name}:{inputs[Controller.InputMethods.RStickY]}".encode('utf-8'))
        except:
            print("Something went wrong! Trying to reconnect! \n")
            client, address = server.accept()
            print(f"Connected to adress: {address}")
        time.sleep(0.3)

def map(value, start1, stop1, start2, stop2):
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))

def updateDictionary(event):
    if event[0] in inputs:
        if event[1] <= threshold and event[1] >= -threshold:
            inputs[event[0]] = 0
        else:
            inputs[event[0]] = map(event[1],-32768,32767,-100,100)

def getInput():
    print("Getting Input")
    while True:
        try:
            events = ctrlr.getInputs()
            for event in events:
                #print(event[0].name, event[1])
                updateDictionary(event)
            #print(inputs)
            #sendData()
        except Controller.UnpluggedError:
            print("test")
            pass


inputThread = threading.Thread(target=getInput)
inputThread.start()
transmitThread = threading.Thread(target=transmit)
transmitThread.start()
