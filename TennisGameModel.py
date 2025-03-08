class Points:
    def __init__(self):
        self.points = [0, 0]  # 0 -> Player 1, 1 -> Player 2
        self.score_values = [0, 15, 30, 40, "Adv"]  # 0, 15, 30, 40, "Adv"

    def score_point(self, player):
        opponent = 1 - player
        game_winner = 0

        # Lógica de puntuación
        if self.points[player] >= 3 and self.points[opponent] >= 3:
            if self.points[player] == self.points[opponent]:  # Deuce
                self.points[player] = 4  # "Adv" para el jugador actual
            elif self.points[player] == 4:  # Ventaja
                game_winner = player + 1  # El jugador actual gana el game
                self.reset()  # Resetear puntos
            elif self.points[opponent] == 4:  # El otro jugador tiene ventaja
                self.points[opponent] = 3  # Volver a 40-40 (Deuce)
        else:
            if self.points[player] == 3:  # Si estaba en 40 y gana, gana el game
                game_winner = player + 1
                self.reset()
            else:
                self.points[player] += 1

        return game_winner

    def reset(self):
        self.points = [0, 0]

    def get_score(self, player):
        return str(self.score_values[min(self.points[player], 4)])  # Aseguramos que no se pase de "Adv"

class TennisGameModel:
    def __init__(self):
        self.points = Points()
        self.games = [0, 0]  # [P1, P2]

    def score_point(self, player):
        game_winner = self.points.score_point(player)
        return game_winner

    def get_score(self, player):
        return self.points.get_score(player)

    def reset(self):
        self.points.reset()
        self.games = [0, 0]
