import pygame
import client
import server
import threading

pygame.init()
WIDTH = 1500
HEIGHT = 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
game = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont("arial", 40)
start_game = font.render("Start game", True, BLACK, WHITE)
join_game = font.render("Join game", True, BLACK, WHITE)
start_rect = start_game.get_rect()
join_rect = join_game.get_rect()
start_rect.center = (WIDTH // 2, (HEIGHT - 70) // 2)
join_rect.center = (WIDTH // 2, (HEIGHT + 70) // 2)
iptext = font.render("Enter IP: ", True, BLACK, WHITE)
ip_rect = iptext.get_rect()
ip_rect.center = (600, 600)


def run_game():
    created = False
    while True:
        if not created:
            game.fill(WHITE)
            game.blit(start_game, start_rect)
            game.blit(join_game, join_rect)
            pygame.display.update()
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
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

                    if join_rect.collidepoint(event.pos):
                        server_ip = enter_ip()
                        print(server_ip)
                        pygame.display.quit()
                        client1 = threading.Thread(
                            target=client.start_client, args=(server_ip,), daemon=True
                        )
                        client1.start()
                        client1.join()
                        quit()


def enter_ip():
    ip = ""
    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return ip
                if event.key == pygame.K_BACKSPACE:
                    ip = ip[:-1]
                else:
                    ip += event.unicode

        game.blit(iptext, ip_rect)
        pygame.draw.rect(game, WHITE, (700, 575, 350, 50))
        pygame.draw.rect(game, BLACK, (700, 575, 350, 50), 1)
        ip_input = font.render(ip, True, BLACK)
        game.blit(ip_input, (705, 575))
        pygame.display.flip()


if __name__ == "__main__":
    run_game()
