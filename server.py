from socket import *
import threading
from tictactoe import TicTacToe

clients = []
game = TicTacToe()

def print_board(board):
    board_str = ''
    i = 0
    while i < len(board):
        if (i + 1) % 3 == 0:
            print()
        if i == (len(board) - 1):
            board_str = board_str + board[i]
        else:
            board_str = board_str + board[i] + '|'
        i += 1

    return board_str

def player(clientSocket):
    while True:
        try:
            message = clientSocket.recv(1024)
            if message:
                game.make_move(int(message))
                board = game.get_board()
                response = print_board(board)
                print(response)
                for client in clients:
                    client.send(response.encode())
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
    if host == 'localhost':
        print("localhost connected")
        connectionSocket.send(serverIP.encode())
    else:
        print("Another computer has connected")
    clients.append(connectionSocket)
    threading.Thread(target=player, args=(connectionSocket,), daemon=True).start()
