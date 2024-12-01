from socket import *
import threading

def run_server():
    clients = []
    getLAN = socket(AF_INET, SOCK_DGRAM)
    getLAN.connect(("1.1.1.1", 80))
    serverIP = getLAN.getsockname()[0]
    getLAN.close()

    serverPort = 12000
    serverSocket = socket(AF_INET, SOCK_STREAM)

    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(("", serverPort))
    serverSocket.listen()

    print("The server is ready to receive")
    while True:

        try:
            connectionSocket, addr = serverSocket.accept()
        except OSError:
            quit()


        host = connectionSocket.recv(1024).decode()
        if host == "localhost":
            print("localhost connected")
            connectionSocket.send(serverIP.encode())
        else:
            print("Another computer has connected")
        clients.append(connectionSocket)
        threading.Thread(target=player, args=(serverSocket, connectionSocket,clients), daemon=True).start()


def player(serverSocket, clientSocket, clients):
    global board_array

    while True:
        try:
            board_string = clientSocket.recv(1024).decode()
            if board_string == 'q':
                break
            if board_string:
                board_array = [i for i in board_string]
                board_str = "".join(board_array)
                for client in clients:
                    client.send(board_str.encode())
            else:
                break
        except:
            break
    clients.remove(clientSocket)
    clientSocket.close()
    if not clients:
        print("Server has stopped running")
        serverSocket.shutdown(SHUT_RDWR)
        serverSocket.close()
