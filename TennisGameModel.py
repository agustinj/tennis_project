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
        self.games[player] += 1

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
        # Aquí incrementas el punto para el jugador
        game_winner = self.points.score_point(player)
        
        if game_winner:  # Si un jugador ganó el game
            self.games.win_game(player)
            self.points.reset()  # Reiniciar puntos después de ganar el game
        
        # Revisamos si alguien ganó el set
        set_winner = self.sets.check_set_winner(self.games.get_games(0), self.games.get_games(1))
        if set_winner:
            self.sets.win_set(set_winner - 1)
            # **Don't reset games here, only reset points after set wins**
        
        return game_winner, set_winner

    def get_score(self, player):
        return self.points.get_score(player)

    def get_game_score(self, player):
        return self.games.get_games(player)

    def get_set_score(self, player):
        return self.sets.get_sets(player)
