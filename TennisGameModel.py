class Points:
    def __init__(self):
        self.points = [0, 0]  # 0 -> Player 1, 1 -> Player 2
        self.score_values = [0, 15, 30, 40, "Adv"]

    def score_point(self, player):
        opponent = 1 - player

        # Caso especial: Ambos en 40 (Deuce)
        if self.points[player] >= 3 and self.points[opponent] >= 3:
            if self.points[player] == self.points[opponent]:  # Si están en Deuce
                self.points[player] = 4  # Dar ventaja al jugador actual
            elif self.points[player] == 4:  # Si ya tenía ventaja, gana el game
                self.reset()
                return player + 1  # Retorna 1 o 2 (ganador del game)
            else:  # Si el rival tenía ventaja y el jugador anota, vuelven a Deuce
                self.points[opponent] = 3
        else:
            self.points[player] += 1  # Aumentar puntos normales
            if self.points[player] > 3:  # Si estaba en 40 y gana, gana el game
                self.reset()
                return player + 1

        return 0  # Nadie ganó el game aún

    def reset(self):
        self.points = [0, 0]

    def get_score(self, player):
        return str(self.score_values[min(self.points[player], 4)])  # Evita índices fuera de rango


class TennisGameModel:
    def __init__(self):
        self.points = Points()
        self.games = [0, 0]  # Games ganados por cada jugador

    def score_point(self, player):
        game_winner = self.points.score_point(player)
        if game_winner:  # Si alguien ganó el game
            self.games[game_winner - 1] += 1  # Sumarle un game al jugador correcto
        return game_winner

    def get_score(self, player):
        return self.points.get_score(player)

    def reset(self):
        self.points.reset()
        self.games = [0, 0]
