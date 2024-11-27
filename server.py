from socket import *
import threading
from tictactoe import TicTacToe

clients = []
game = TicTacToe()

def generate_response(board):
    responseString = ''
    for i in range(len(board)):
        if i == len(board) - 1:
            responseString = responseString + board[i]
        else:
            responseString = responseString + board[i] + '.'
    return responseString

def handle_client(clientSocket):
    while True:
        try:
            message = clientSocket.recv(1024)
            if message:
                game.make_move(int(message))
                board = game.get_board()
                response = generate_response(board)
                print(response)
                for client in clients:
                    client.send(response.encode('utf-8'))
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
serverSocket.listen(2)

print("The server is ready to receive")
while True:
    connectionSocket, addr = serverSocket.accept()
    clients.append(connectionSocket)
    threading.Thread(target=handle_client, args=(connectionSocket,), daemon=True).start()
