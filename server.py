from socket import *
import threading
import time
from tictactoe import TicTacToe

clients = []
game = TicTacToe()
board_array = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']


def print_board(board):
    board_str = "\n|"
    i = 0
    while i < len(board):
        if (i != 0) and (i % 3 == 0):
            board_str = board_str + "\n|"
        board_str = board_str + board[i] + "|"
        i += 1

    return board_str





def player(clientSocket):
    global board_array
    while True:
        try:
            board_string = clientSocket.recv(1024).decode()
            if board_string:
                board_array = [i for i in board_string]


                print(board_array)
                board_str = "".join(board_array)
                for client in clients:
                    client.send(board_str.encode())
            else:
                break
        except:
            break
    clients.remove(clientSocket)
    clientSocket.close()


getLAN = socket(AF_INET, SOCK_DGRAM)
getLAN.connect(("1.1.1.1", 80))
serverIP = getLAN.getsockname()[0]
getLAN.close()

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen()

print("The server is ready to receive")
while True:
    connectionSocket, addr = serverSocket.accept()
    host = connectionSocket.recv(1024).decode()
    if host == "localhost":
        print("localhost connected")
        connectionSocket.send(serverIP.encode())
    else:
        print("Another computer has connected")
    clients.append(connectionSocket)
    threading.Thread(target=player, args=(connectionSocket,), daemon=True).start()
