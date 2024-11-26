from socket import *

serverPort = 12000
hostname = gethostname()
serverIP = gethostbyname(hostname)
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)
print("The server is ready to receive")
connectionSocket, addr = serverSocket.accept()
print(addr)
host = connectionSocket.recv(1024).decode()
if host == 'localhost':
    print("localhost connected")
    connectionSocket.send(serverIP.encode())
else:
    print("Another computer has connected")
while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()
    capitalizedSentence = sentence.upper()
    connectionSocket.send(capitalizedSentence.encode())
    connectionSocket.close()
