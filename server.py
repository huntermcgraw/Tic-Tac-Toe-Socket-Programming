from asyncio import Event
from queue import Queue
from socket import *
import threading
from _thread import *

def Player1(q):
    connectionSocket, addr = serverSocket.accept()
    host = connectionSocket.recv(1024).decode()
    if host == 'localhost':
        print("localhost connected")
        connectionSocket.send(serverIP.encode())
    else:
        print("Another computer has connected")
    while True:
        sentence = connectionSocket.recv(1024).decode()
        capitalizedSentence = sentence.upper()
        event = Event()
        q.put((capitalizedSentence, event))
        connectionSocket.send(capitalizedSentence.encode())
        event.wait()
    connectionSocket.close()


def Player2(q):
    connectionSocket, addr = serverSocket.accept()
    host = connectionSocket.recv(1024).decode()
    if host == 'localhost':
        print("localhost connected")
        connectionSocket.send(serverIP.encode())
    else:
        print("Another computer has connected")
    while True:
        data, event = q.get()
        connectionSocket.send(data.encode())
        sentence = connectionSocket.recv(1024).decode()
        capitalizedSentence = sentence.upper()
        event = Event()
        q.put((capitalizedSentence, event))
        event.wait()
    connectionSocket.close()


getLAN = socket(AF_INET, SOCK_DGRAM)
getLAN.connect(("1.1.1.1", 80))
serverIP = getLAN.getsockname()[0]
getLAN.close()

serverPort = 12000
#hostname = gethostname()
#serverIP = gethostbyname(hostname)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(2)

print("The server is ready to receive")
q = Queue()
t1 = threading.Thread(target=Player1, args=(q, ))
t2 = threading.Thread(target=Player2, args=(q, ))
t1.start()
t2.start()
