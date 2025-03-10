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
        self.tie_break = False  # Indicador de si se está jugando un tie-break

    def win_set(self, player):
        print(f"Set ganado por el jugador {player + 1}")
        self.sets[player] += 1

    def get_sets(self, player):
        return self.sets[player]

    def check_set_winner(self, games_player1, games_player2):
        # Si hay empate en 6-6, activar el tie-break
        if games_player1 == 6 and games_player2 == 6:
            self.tie_break = True
            print("Entering tie-break mode!")
            return 'tie_break'  # Debe retornar 'tie_break' para que el código lo detecte

        # Si alguien gana con diferencia de 2 games, gana el set
        if (games_player1 >= 6 or games_player2 >= 6) and abs(games_player1 - games_player2) >= 2:
            self.tie_break = False  # Resetear el tie-break si termina el set
            return 1 if games_player1 > games_player2 else 2  

        return 0  # No hay ganador del set todavía


class TieBreak:
    def __init__(self):
        self.points = [0, 0]  # Tie-break puntos para los jugadores

    def score_point(self, player):
        self.points[player] += 1
        if self.points[player] >= 7 and abs(self.points[0] - self.points[1]) >= 2:
            return player + 1  # Retorna el jugador que gana el tie-break
        return 0

    def reset(self):
        self.points = [0, 0]


class TennisGameModel:
    def __init__(self):
        self.points = Points()
        self.games = Games()
        self.sets = Sets()
        self.tie_break = TieBreak()

class TennisGameModel:
    def __init__(self):
        self.points = Points()
        self.games = Games()
        self.sets = Sets()
        self.tie_break = TieBreak()

    def score_point(self, player):
        # Si está en tie-break, contar puntos con `TieBreak`
        if self.sets.tie_break:
            tie_winner = self.tie_break.score_point(player)
            if tie_winner:
                print(f"Set won by Player {tie_winner} (Tie-Break Mode)")
                self.sets.win_set(tie_winner - 1)
                self.games = Games()  # Resetear los games
                self.tie_break.reset()  # Resetear el tie-break
                self.sets.tie_break = False  # Salir del tie-break
                return tie_winner, tie_winner  # Retorna el ganador del set

            return 0, 0  # Sigue el tie-break sin ganador aún

        # Si no es tie-break, procesar normalmente
        game_winner, _ = self.points.score_point(player)

        if game_winner:
            self.games.win_game(player)

        # Verificar si se ha llegado a 6-6 y si es necesario iniciar un tie-break
        set_winner = self.sets.check_set_winner(self.games.get_games(0), self.games.get_games(1))

        if set_winner == 'tie_break':
            return game_winner, 'tie_break'

        if set_winner:
            self.sets.win_set(set_winner - 1)
            self.games = Games()  # Resetear los juegos
            return game_winner, set_winner

        return game_winner, 0

    def get_score(self, player):
        return self.points.get_score(player)

    def get_game_score(self, player):
        return self.games.get_games(player)

    def get_set_score(self, player):
        return self.sets.get_sets(player)
