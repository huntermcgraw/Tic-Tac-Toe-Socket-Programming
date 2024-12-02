from socket import *
import threading


def run_server():
    clients = []
    get_LAN = socket(AF_INET, SOCK_DGRAM)
    get_LAN.connect(("1.1.1.1", 80))
    server_IP = get_LAN.getsockname()[0]
    get_LAN.close()

    server_port = 12000
    server_socket = socket(AF_INET, SOCK_STREAM)

    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(("", server_port))
    server_socket.listen()

    print("The server is ready to receive")
    while True:

        try:
            connection_socket, addr = server_socket.accept()
        except OSError:
            quit()

        host = connection_socket.recv(1024).decode()
        if host == "localhost":
            print("localhost connected")
            connection_socket.send(server_IP.encode())
        else:
            print("Another computer has connected")
        clients.append(connection_socket)
        threading.Thread(target=player, args=(server_socket, connection_socket, clients), daemon=True).start()


def player(server_socket, client_socket, clients):
    global board_array

    while True:
        try:
            board_string = client_socket.recv(1024).decode()
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
    clients.remove(client_socket)
    client_socket.close()
    if not clients:
        print("Server has stopped running")
        server_socket.shutdown(SHUT_RDWR)
        server_socket.close()
