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
                return player + 1  # El jugador que ganó el game
            else:
                self.points[opponent] = 3  # El rival vuelve a Deuce
        else:
            self.points[player] += 1

            if self.points[player] == 4:
                self.reset()
                return player + 1  # El jugador ganó el game

        return 0

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

    def win_set(self, player):
        self.sets[player] += 1

    def get_sets(self, player):
        return self.sets[player]

    def check_set_winner(self, games_player1, games_player2):
        # Verificar si se ha ganado un set
        if games_player1 >= 6 or games_player2 >= 6:
            if abs(games_player1 - games_player2) >= 2:
                return 1 if games_player1 > games_player2 else 2
        return 0

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

    def score_point(self, player):
        print(f"Before scoring: Player 1 points: {self.points.points[0]}, Player 2 points: {self.points.points[1]}")  # Log para ver los puntos antes de la acción

        game_winner = self.points.score_point(player)
        print(f"After scoring: Player 1 points: {self.points.points[0]}, Player 2 points: {self.points.points[1]}")  # Log para ver los puntos después de la acción

        if game_winner:  # Si alguien ganó el game
            self.games.win_game(player)
            print(f"Game won by Player {player + 1}")  # Log para saber si se ganó un game

        # Verificar si alguien ganó el set después de ganar un game
        set_winner = self.sets.check_set_winner(self.games.get_games(0), self.games.get_games(1))
        if set_winner:  # Si hay un ganador de set
            self.sets.win_set(set_winner - 1)  # Ganador del set
            self.games = Games()  # Reiniciar los juegos después de un set ganado
            print(f"Set won by Player {set_winner}")  # Log para saber si se ganó el set
            return game_winner, set_winner

        return game_winner, 0  # Si no se ha ganado el set, solo se devuelve el ganador del game


    def get_score(self, player):
        return self.points.get_score(player)

    def get_game_score(self, player):
        return self.games.get_games(player)

    def get_set_score(self, player):
        return self.sets.get_sets(player)
