from socket import *
import threading

serverName = input('If you are hosting the server on your computer, enter "localhost".\n'
                   'Otherwise, enter the IP given by the host.\n'
                   'Type here: ')

def get_board(clientSocket):
    while True:
        try:
            message = clientSocket.recv(1024)
            if message:
                print(message.decode())
        except:
            print("Disconnected from server.")
            break

serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.send(serverName.encode())
if serverName == 'localhost':
    serverIP = clientSocket.recv(1024)
    print(serverIP.decode())
threading.Thread(target=get_board, args=(clientSocket,), daemon=True).start()
while True:
    message = input("\nEnter index (0-8): ")
    clientSocket.send(message.encode())

    if message == 'q':
        break

clientSocket.close()