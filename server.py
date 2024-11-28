from socket import *
import threading
from tictactoe import TicTacToe
import queue

clients = []
game = TicTacToe()
lock_input = threading.Lock()
turn = threading.Event()
q = queue.Queue()

def print_board(board):
    board_str = '\n|'
    i = 0
    while i < len(board):
        if (i != 0) and (i % 3 == 0):
            board_str = board_str + '\n|'
        board_str = board_str + board[i] + '|'
        i += 1

    return board_str

def player(clientSocket, lock, turn, q):
    while True:
        turn.wait()
        turn.clear()
        with lock:
            try:
                message = clientSocket.recv(1024)
                if message:
                    game.choice(int(message))
                    board = game.get_board()
                    response = print_board(board)
                    print(response)
                    for client in clients:
                        client.send(response.encode())
                else:
                    break
            except:
                break

    print("A computer has disconnected")
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

    turn.set()
    threading.Thread(target=player, args=(connectionSocket, lock_input, turn, q), daemon=True).start()
