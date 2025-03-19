from GameMessages import GameMessages


class Points:
    def __init__(self):
        self.points = [0, 0]  # 0 -> Player 1, 1 -> Player 2
        self.score_values = [0, 15, 30, 40, "Adv"]

    def score_point(self, player):
        opponent = 1 - player
        
        if self.points[player] >= 3 and self.points[opponent] >= 3:
            if self.points[player] == self.points[opponent]:  # Deuce
                self.points[player] = 4  # Ventaja para el jugador actual
            elif self.points[player] == 4:  # Si tenía ventaja, gana el game
                self.reset()
                return player + 1, 0  # El jugador que ganó el game, pero sin ganador del set
            else:
                self.points[opponent] = 3  # El rival vuelve a Deuce
        else:
            self.points[player] += 1

            if self.points[player] == 4:
                self.reset()
                return player + 1, 0  # El jugador ganó el game, pero no el set aún

        return 0, 0  # Si no hay ganador aún

    def reset(self):
        self.points = [0, 0]

    def get_score(self, player):
        return str(self.score_values[min(self.points[player], 4)])
    
class Games:
    def __init__(self):
        self.games = [0, 0]  # Games ganados por Player 1 y Player 2

    def win_game(self, player):
        print(f"Before winning game: Player 1 games: {self.games[0]}, Player 2 games: {self.games[1]}")  # Log para ver antes de sumar
        self.games[player] += 1
        print(f"After winning game: Player 1 games: {self.games[0]}, Player 2 games: {self.games[1]}")  # Log para ver después de sumar


    def get_games(self, player):
        return self.games[player]

class Sets:
    def __init__(self):
        self.sets = [0, 0]  # Sets ganados por Player 1 y Player 2
        self.tie_break = TieBreak()  # Instancia de TieBreak

    def win_set(self, player):
        print(f"Set ganado por el jugador {player + 1}")
        self.sets[player] += 1

    def get_sets(self, player):
        return self.sets[player]

    def check_set_winner(self, games_player1, games_player2):
        # Verificamos si ambos jugadores están en 6-6
        if games_player1 == 6 and games_player2 == 6:
            return 'tie_break'  # Solo devolvemos 'tie_break' cuando los dos jugadores tengan 6 juegos

        # Si algún jugador tiene más de 6 games con una diferencia de al menos 2, ese jugador gana el set
        if (games_player1 >= 6 or games_player2 >= 6) and abs(games_player1 - games_player2) >= 2:
            return 1 if games_player1 > games_player2 else 2

        return 0  # No hay ganador del set aún


class TieBreak:
    def __init__(self):
        self.points = [0, 0]  # Puntos para los jugadores
        self.started = False  # Estado de si el tie-break ha comenzado
        self.finished = False  # Estado de si el tie-break ha terminado
        self.winner = None  # Ganador del tie-break, None si no ha terminado

    def start(self):
        # Inicia el tie-break.
        if not self.started:
            self.started = True
            self.points = [0, 0]  # Resetea los puntos antes de empezar
            self.finished = False
            self.winner = None

    def score_point(self, player):
        # Añade un punto a un jugador y verifica si el tie-break ha terminado.
        if not self.started:  # No se puede puntuar si el tie-break no ha comenzado
            return 0
        
        self.points[player] += 1

        # Verificar si alguien ganó el tie-break
        if self.points[player] >= 7 and abs(self.points[0] - self.points[1]) >= 2:
            self.finished = True
            self.winner = player + 1  # Jugador 1 o 2 (empezando desde 1)
            return self.winner

        return 0

    def reset(self):
        #Resetea el estado del tie-break.
        self.started = False
        self.finished = False
        self.points = [0, 0]
        self.winner = None

class TennisGameModel:
    def __init__(self):
        self.points = Points()  # Este es el sistema de puntuación normal
        self.games = Games()  # Contador de juegos
        self.sets = Sets()  # Contador de sets
        self.tie_break = TieBreak()  # El tie-break

    def score_point(self, player):
        # Si estamos en tie-break, procesamos el punto con esa lógica
        if self.tie_break.started and not self.tie_break.finished:
            tie_break_winner = self.tie_break.score_point(player)

            if tie_break_winner:
                print(f"DEBUG - Tie-break ganado por Player {tie_break_winner}")
                self.sets.win_set(tie_break_winner - 1)
                self.games = Games()  # Reseteamos los games
                self.tie_break.reset()  # Reseteamos el tie-break para el siguiente set
                return 0, tie_break_winner  # El segundo valor indica el ganador del set

            return 0, 'tie_break'  # Seguimos en tie-break

        # Si no estamos en tie-break, seguimos con la lógica normal
        game_winner, _ = self.points.score_point(player)

        if game_winner:
            self.games.win_game(player)

        games_player1 = self.games.get_games(0)
        games_player2 = self.games.get_games(1)

        print(f"DEBUG - Games -> Player 1: {games_player1}, Player 2: {games_player2}")

        # Activar Tie Break si es necesario
        if games_player1 == 6 and games_player2 == 6 and not self.tie_break.started:
            print("DEBUG - Tie Break activado")
            GameMessages.show_tiebreak() 
            self.tie_break.start()
            self.points.reset()
            return 0, 'tie_break'

        # Verificamos si alguien ganó el set
        set_winner = self.sets.check_set_winner(games_player1, games_player2)

        if set_winner:
            self.sets.win_set(set_winner - 1)
            self.games = Games()
            self.tie_break.reset()
            return 0, set_winner

        return game_winner, 0

    def get_score(self, player):
        return self.points.get_score(player)

    def get_game_score(self, player):
        return self.games.get_games(player)

    def get_set_score(self, player):
        return self.sets.get_sets(player)