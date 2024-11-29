from socket import *
import threading
import pygame


WIDTH = 900
HEIGHT = 900
board_image = pygame.image.load("img/board.png")
index0 = pygame.Rect(0, 0, 300, 300)
index1 = pygame.Rect(300, 0, 300, 300)
index2 = pygame.Rect(600, 0, 300, 300)
index3 = pygame.Rect(0, 300, 300, 300)
index4 = pygame.Rect(300, 300, 300, 300)
index5 = pygame.Rect(600, 300, 300, 300)
index6 = pygame.Rect(0, 600, 300, 300)
index7 = pygame.Rect(300, 600, 300, 300)
index8 = pygame.Rect(600, 600, 300, 300)
index = [index0, index1, index2, index3, index4, index5, index6, index7, index8]
index_spaces = [(75, 75), (375, 75), (675, 75), (75, 375), (375, 375), (675, 375), (75, 675), (375, 675), (675, 675)]
x = pygame.image.load("img/x.png")
o = pygame.image.load("img/o.png")
board_array = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

serverName = input('If you are hosting the server on your computer, enter "localhost".\n'
                   'Otherwise, enter the IP given by the host.\n'
                   'Type here: ')


def get_board(clientSocket, curr_player):
    global board_array
    while True:
        game.blit(board_image, (0, 0))
        for i in range(len(board_array)):
            if board_array[i] == 'X':
                game.blit(x, index_spaces[i])
            if board_array[i] == 'O':
                game.blit(o, index_spaces[i])

        pygame.display.update()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(index)):
                    if index[i].collidepoint(event.pos):
                        board_array[i] = curr_player
                        send_array(clientSocket)


def get_array():
    global board_array
    while True:
        board_string = clientSocket.recv(1024).decode()
        if board_string:
            board_array = [i for i in board_string]


def send_array(clientSocket):
    global board_array
    board_str = "".join(board_array)
    clientSocket.send(board_str.encode())


serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
clientSocket.send(serverName.encode())
if serverName == 'localhost':
    serverIP = clientSocket.recv(1024)
    print(serverIP.decode())
    curr_player = 'X'
else:
    curr_player = 'O'
pygame.init()
game = pygame.display.set_mode((WIDTH, HEIGHT))

threading.Thread(target=get_array, daemon=True).start()
get_board(clientSocket, curr_player)
