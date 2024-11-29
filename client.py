from socket import *
import threading
import pygame


WIDTH = 1500
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


pygame.init()


def check_win(board_array, curr):
    win_cases = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
    for i in win_cases:
        count = 0
        for j in i:
            if board_array[j] == curr:
                count += 1
        if count == 3:
            return True

    return False


def get_board(clientSocket, curr_player, other_player, server_ip):
    global board_array
    global opp_score
    score = 0
    opp_score = 0

    white = (255, 255, 255)
    black = (0, 0, 0)

    game = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont('arial', 40)
    p1text = font.render(f'You: {opp_score}', True, white, black)
    p2text = font.render(f'Other Player: {score}', True, white, black)
    iptext = font.render(f'{server_ip}', True, white, black)
    p1textRect = p1text.get_rect()
    p2textRect = p1text.get_rect()
    iptextRect = iptext.get_rect()
    p1textRect.center = (1100, 50)
    p2textRect.center = (1100, 120)
    iptextRect.center = (1050, 870)



    resetText = font.render('Reset Board', True, black, white)
    resetRect = resetText.get_rect()
    resetRect.center = (1100, 600)

    while True:
        game.blit(board_image, (0, 0))

        game.blit(p1text, p1textRect)
        game.blit(p2text, p2textRect)
        game.blit(iptext, iptextRect)
        game.blit(resetText, resetRect)

        for i in range(len(board_array)):
            if board_array[i] == 'X':
                game.blit(x, index_spaces[i])
            if board_array[i] == 'O':
                game.blit(o, index_spaces[i])

        p1text = font.render(f'You: {score}', True, white, black)
        p2text = font.render(f'Other Player: {opp_score}', True, white, black)
        iptext = font.render(f'{server_ip}', True, white, black)

        pygame.display.update()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                clientSocket.send('q'.encode())
                quit()

            if not (check_win(board_array, curr_player) or check_win(board_array, other_player)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resetRect.collidepoint(event.pos):
                        board_array = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
                        send_array(clientSocket)
                        break


                    for i in range(len(index)):
                        if index[i].collidepoint(event.pos):
                            board_array[i] = curr_player
                            send_array(clientSocket)
                            break
                if check_win(board_array, curr_player):
                    score += 1
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if resetRect.collidepoint(event.pos):
                        board_array = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
                        send_array(clientSocket)
                        break





def get_array(clientSocket, other_player):
    global board_array
    global opp_score
    while True:
        board_string = clientSocket.recv(1024).decode()
        if board_string:
            board_array = [i for i in board_string]
            if check_win(board_array, other_player):
                opp_score += 1


def send_array(clientSocket):
    global board_array
    board_str = "".join(board_array)
    clientSocket.send(board_str.encode())


def start_client(serverName):
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_STREAM)

    clientSocket.connect((serverName, serverPort))

    clientSocket.send(serverName.encode())
    if serverName == 'localhost':
        serverIP = clientSocket.recv(1024)
        serverIP = serverIP.decode()
        print(serverIP)
        curr_player = 'X'
        other_player = 'O'
    else:
        curr_player = 'O'
        other_player = 'X'

    threading.Thread(target=get_array, args=(clientSocket, other_player), daemon=True).start()
    get_board(clientSocket, curr_player, other_player, serverIP)




#start_client("localhost")