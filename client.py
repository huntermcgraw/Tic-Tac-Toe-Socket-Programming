from socket import *

serverName = input('If you are hosting the server on your computer, enter "localhost".\n'
                   'Otherwise, enter the IP given by the host.\n'
                   'Type here: ')
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.send(serverName.encode())
if serverName == 'localhost':
    serverIP = clientSocket.recv(1024)
    print(serverIP.decode())

while True:


    sentence = input('Input lowercase sentence:')
    clientSocket.send(sentence.encode())
    modifiedSentence = clientSocket.recv(1024)
    print ('From Server:', modifiedSentence.decode())
    if sentence == 'q':
        break
clientSocket.close()