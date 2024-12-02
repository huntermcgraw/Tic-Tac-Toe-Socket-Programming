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
index_list = [index0, index1, index2, index3, index4, index5, index6, index7, index8]
index_spaces = [
    (75, 75),
    (375, 75),
    (675, 75),
    (75, 375),
    (375, 375),
    (675, 375),
    (75, 675),
    (375, 675),
    (675, 675),
]
x = pygame.image.load("img/x.png")
o = pygame.image.load("img/o.png")
board_array = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
white = (255, 255, 255)
black = (0, 0, 0)

pygame.init()


def check_win(board_array, curr):
    win_cases = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6),
    ]
    for i in win_cases:
        count = 0
        for j in i:
            if board_array[j] == curr:
                count += 1
        if count == 3:
            return True

    return False


def get_board(client_socket, curr_player, other_player, server_ip):
    global board_array
    global opp_score
    score = 0
    opp_score = 0

    game = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont("arial", 40)
    p1_text = font.render(f"You: {opp_score}", True, white, black)
    p2_text = font.render(f"Other Player: {score}", True, white, black)
    ip_text = font.render(f"{server_ip}", True, white, black)
    turn = font.render(f"Your turn!", True, white, black)
    not_turn = font.render(f"Opponents turn!", True, white, black)
    game_over = font.render(f"Game over!", True, white, black)
    p1_text_rect = p1_text.get_rect()
    p2_text_rect = p1_text.get_rect()
    ip_text_rect = ip_text.get_rect()
    turn_rect = turn.get_rect()
    not_turn_rect = turn.get_rect()
    game_over_rect = game_over.get_rect()
    p1_text_rect.center = (1100, 150)
    p2_text_rect.center = (1100, 220)
    ip_text_rect.center = (1020, 870)
    reset_text = font.render("Reset Board", True, black, white)
    reset_rect = reset_text.get_rect()
    reset_rect.center = (1385, 870)

    while True:

        game.blit(board_image, (0, 0))
        game.blit(p1_text, p1_text_rect)
        game.blit(p2_text, p2_text_rect)
        game.blit(ip_text, ip_text_rect)
        game.blit(reset_text, reset_rect)

        if not (check_win(board_array, curr_player) or check_win(board_array, other_player)):
            if take_turn(curr_player, board_array):
                game.blit(turn, turn_rect)
            else:
                game.blit(not_turn, not_turn_rect)
        else:
            game.blit(game_over, game_over_rect)

        for i in range(len(board_array)):
            if board_array[i] == "X":
                game.blit(x, index_spaces[i])
            if board_array[i] == "O":
                game.blit(o, index_spaces[i])

        p1_text = font.render(f"({curr_player}) You: {score}", True, white, black)
        p2_text = font.render(f"({other_player}) Opponent: {opp_score}", True, white, black)
        ip_text = font.render(f"{server_ip}", True, white, black)

        pygame.display.update()

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                client_socket.send("q".encode())
                quit()

            if not (check_win(board_array, curr_player) or check_win(board_array, other_player)):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_rect.collidepoint(event.pos):
                        board_array = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
                        send_array(client_socket)
                        break

                    if take_turn(curr_player, board_array):
                        for i in range(len(index_list)):
                            if index_list[i].collidepoint(event.pos):
                                if board_array[i] == " ":
                                    board_array[i] = curr_player
                                    send_array(client_socket)
                                    break

                if check_win(board_array, curr_player):
                    score += 1

            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if reset_rect.collidepoint(event.pos):
                        board_array = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
                        send_array(client_socket)
                        break


def take_turn(curr_player, board_array):
    x_count = 0
    o_count = 0

    for i in board_array:
        if i == "X":
            x_count += 1
        elif i == "O":
            o_count += 1

    if curr_player == "X":
        if x_count == o_count:
            return True
        return False
    else:
        if x_count > o_count:
            return True
        return False


def get_array(client_socket, other_player):
    global board_array
    global opp_score

    while True:
        board_string = client_socket.recv(1024).decode()
        if board_string:
            board_array = [i for i in board_string]
            if check_win(board_array, other_player):
                opp_score += 1


def send_array(client_socket):
    global board_array

    board_str = "".join(board_array)
    client_socket.send(board_str.encode())


def start_client(server_name):
    server_port = 12000
    client_socket = socket(AF_INET, SOCK_STREAM)

    client_socket.connect((server_name, server_port))

    client_socket.send(server_name.encode())
    if server_name == "localhost":
        server_IP = client_socket.recv(1024)
        server_IP = server_IP.decode()
        print(server_IP)
        curr_player = "X"
        other_player = "O"
    else:
        server_IP = server_name
        curr_player = "O"
        other_player = "X"

    threading.Thread(target=get_array, args=(client_socket, other_player), daemon=True).start()
    get_board(client_socket, curr_player, other_player, server_IP)
