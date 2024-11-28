from socket import *
import threading

lock_input = threading.Lock()

serverName = input('If you are hosting the server on your computer, enter "localhost".\n'
                   'Otherwise, enter the IP given by the host.\n'
                   'Type here: ')

def get_board(clientSocket, lock_input):
    with lock_input:
        with lock_input:
            message = input("\nEnter index (0-8): ")
            clientSocket.send(message.encode())

            if message == 'q':
                quit()
        try:
            message = clientSocket.recv(1024)
            if message:
                print(message.decode())
        except:
            print("Disconnected from server.")

serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.send(serverName.encode())
if serverName == 'localhost':
    serverIP = clientSocket.recv(1024)
    print(serverIP.decode())
threading.Thread(target=get_board, args=(clientSocket, lock_input), daemon=True).start()

clientSocket.close()