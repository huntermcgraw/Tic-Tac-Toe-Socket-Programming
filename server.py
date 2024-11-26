from socket import *
import threading
from _thread import *

#print_lock = threading.Lock()


def newClient(connectionSocket):
    host = connectionSocket.recv(1024).decode()
    if host == 'localhost':
        print("localhost connected")
        connectionSocket.send(serverIP.encode())
    else:
        print("Another computer has connected")
    while True:
        sentence = connectionSocket.recv(1024).decode()
        capitalizedSentence = sentence.upper()
        connectionSocket.send(capitalizedSentence.encode())
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
client2 = None
while True:

    print("The server is ready to receive")
    connectionSocket, addr = serverSocket.accept()

    #print_lock.acquire()

    start_new_thread(newClient, (connectionSocket,))


