import socket
import threading

HOST = '0.0.0.0'
PORT = 8000

games = []
waiting_player = None
lock = threading.Lock()


class Game:
    def __init__(self, player_x, player_o):
        self.board = [' '] * 9
        self.player_x = player_x
        self.player_o = player_o
        self.current_turn = 'X'
        self.spectators = []
        self.active = True

    def broadcast(self, message):
        for player in [self.player_x, self.player_o] + self.spectators:
            try:
                player.sendall(message.encode())
            except:
                pass

    def print_board(self):
        b = self.board
        return f"""
 {b[0]} | {b[1]} | {b[2]}
-----------
 {b[3]} | {b[4]} | {b[5]}
-----------
 {b[6]} | {b[7]} | {b[8]}
"""

    def check_winner(self):
        wins = [
            (0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)
        ]
        for a,b,c in wins:
            if self.board[a] == self.board[b] == self.board[c] != ' ':
                return self.board[a]
        if ' ' not in self.board:
            return 'Draw'
        return None


def handle_client(conn, addr):
    global waiting_player

    conn.sendall("Bienvenido a Tic-Tac-Toe!\n".encode())
    conn.sendall("Escribe PLAY para jugar o WATCH para ser espectador:\n".encode())

    try:
        option = conn.recv(1024).decode().strip().upper()

        if option == "PLAY":
            with lock:
                if waiting_player is None:
                    waiting_player = conn
                    conn.sendall("Esperando otro jugador...\n".encode())
                    return
                else:
                    game = Game(waiting_player, conn)
                    games.append(game)
                    threading.Thread(target=run_game, args=(game,)).start()
                    waiting_player = None

        elif option == "WATCH":
            conn.sendall("Esperando partida activa...\n".encode())
            while True:
                if games:
                    game = games[-1]
                    game.spectators.append(conn)
                    conn.sendall("Ahora eres espectador.\n".encode())
                    conn.sendall(game.print_board().encode())
                    break

        else:
            conn.sendall("Opción inválida.\n".encode())
            conn.close()

    except:
        conn.close()


def run_game(game):
    game.broadcast("¡Partida iniciada!\n")
    game.broadcast(game.print_board())

    while game.active:
        current_player = game.player_x if game.current_turn == 'X' else game.player_o
        other_player = game.player_o if game.current_turn == 'X' else game.player_x

        try:
            current_player.sendall(f"Tu turno ({game.current_turn}). Elige posición (0-8): ".encode())
            move = current_player.recv(1024).decode().strip()

            if not move.isdigit() or int(move) not in range(9):
                current_player.sendall("Movimiento inválido.\n".encode())
                continue

            move = int(move)

            if game.board[move] != ' ':
                current_player.sendall("Casilla ocupada.\n".encode())
                continue

            game.board[move] = game.current_turn
            game.broadcast(game.print_board())

            winner = game.check_winner()
            if winner:
                if winner == 'Draw':
                    game.broadcast("¡Empate!\n")
                else:
                    game.broadcast(f"¡Ganó {winner}!\n")
                game.active = False
                break

            game.current_turn = 'O' if game.current_turn == 'X' else 'X'

        except:
            game.active = False
            break

    game.broadcast("Partida terminada.\n")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Servidor iniciado en puerto {PORT}...")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()


if __name__ == "__main__":
    start_server()