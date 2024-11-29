import pygame
import client
import server
import threading

pygame.init()
WIDTH = 1500
HEIGHT = 900
white = (255, 255, 255)
black = (0, 0, 0)
game = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('arial', 40)
start_game = font.render('Start a game', True, black, white)
join_game = font.render('Join a game', True, black, white)
startRect = start_game.get_rect()
joinRect = join_game.get_rect()
startRect.center = (WIDTH // 2, (HEIGHT - 70) // 2)
joinRect.center = (WIDTH // 2, (HEIGHT + 70) // 2)


def run_game():
    created = False
    while True:
        if not created:
            game.fill(white)
            game.blit(start_game, startRect)
            game.blit(join_game, joinRect)
            pygame.display.update()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if startRect.collidepoint(event.pos):
                        server1 = threading.Thread(target=server.run_server, daemon=True)
                        server1.start()
                        pygame.display.quit()
                        client1 = threading.Thread(target=client.start_client, args=("localhost",), daemon=True)
                        client1.start()
                        client1.join()
                        print("client closed")
                        server1.join()
                        print("server closed")
                        quit()

                    if joinRect.collidepoint(event.pos):
                        server_ip = enter_ip()
                        print(server_ip)
                        pygame.display.quit()
                        client1 = threading.Thread(target=client.start_client, args=(server_ip,), daemon=True)
                        client1.start()
                        client1.join()
                        quit()

def enter_ip():
    ip = ''
    while True:
        iptext = font.render('Enter IP: ', True, black, white)
        ipRect = iptext.get_rect()
        ipRect.center = (600,600)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if ipRect.collidepoint(event.pos):
                    active = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return ip
                if event.key == pygame.K_BACKSPACE:
                    ip = ip[:-1]
                else:
                    ip += event.unicode


        game.blit(iptext, ipRect)
        pygame.draw.rect(game, white, (700, 575, 350, 50))
        pygame.draw.rect(game, black, (700, 575, 350, 50), 1)
        ip_input = font.render(ip, True, black)
        game.blit(ip_input, (705,575))
        pygame.display.flip()

if __name__ == "__main__":
    run_game()
