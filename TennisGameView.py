from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from TennisGameModel import Games, TennisGameModel

class TennisGameView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(cols=1, padding=20, spacing=10, **kwargs)
        
        # Modelo que gestiona la lógica
        self.model = TennisGameModel()

        # Sección de puntos, juegos y sets
        self.scoreboard = GridLayout(cols=4, size_hint_y=None, height=80)  # Añadir columna para sets
        self.scoreboard.add_widget(Label(text="Points", font_size=30, bold=True))
        self.scoreboard.add_widget(Label(text="Games", font_size=30, bold=True, size_hint_x=None, width=100))
        self.scoreboard.add_widget(Label(text="Sets", font_size=30, bold=True, size_hint_x=None, width=100))  # Columna de sets
        self.scoreboard.add_widget(Label(text="", font_size=30))
        self.add_widget(self.scoreboard)
        
        # Filas de jugadores
        self.player1_row = BoxLayout()
        self.btn1 = Button(text="Player 1", font_size=30, on_press=lambda x: self.score_point(0))
        self.p1_points = Label(text="0", font_size=30)
        self.p1_games = Label(text="0", font_size=30)
        self.p1_sets = Label(text="0", font_size=30)  # Label para sets de Player 1
        self.player1_row.add_widget(self.btn1)
        self.player1_row.add_widget(self.p1_points)
        self.player1_row.add_widget(self.p1_games)
        self.player1_row.add_widget(self.p1_sets)  # Agregar al layout
        self.add_widget(self.player1_row)

        self.player2_row = BoxLayout()
        self.btn2 = Button(text="Player 2", font_size=30, on_press=lambda x: self.score_point(1))
        self.p2_points = Label(text="0", font_size=30)
        self.p2_games = Label(text="0", font_size=30)
        self.p2_sets = Label(text="0", font_size=30)  # Label para sets de Player 2
        self.player2_row.add_widget(self.btn2)
        self.player2_row.add_widget(self.p2_points)
        self.player2_row.add_widget(self.p2_games)
        self.player2_row.add_widget(self.p2_sets)  # Agregar al layout
        self.add_widget(self.player2_row)

    def score_point(self, player):
        # Llamar al modelo para procesar el punto
        game_winner, set_winner = self.model.score_point(player)

        if game_winner:
            print(f"Game won by Player {player+1}")
            self.model.points.reset()  # Después de ganar el game, reiniciar los puntos

        if set_winner == "tie_break":
            print("Entering tie-break mode!")  # Mensaje para depuración

        if self.model.sets.tie_break:
            print("Entering tie-break mode!")  # Mensaje para depuración

        elif set_winner:  # Si alguien ganó el set normalmente
            self.model.games = Games()  # Resetear juegos después de un set ganado
            print(f"Set won by Player {set_winner}")

        self.update_scoreboard()  # Actualizar la interfaz con los puntajes

    def update_scoreboard(self):
        # Si está en tie-break, muestra los puntos de tie-break en lugar de los normales
        if self.model.sets.tie_break:
            self.p1_points.text = str(self.model.tie_break.points[0])
            self.p2_points.text = str(self.model.tie_break.points[1])
        else:
            self.p1_points.text = self.model.get_score(0)
            self.p2_points.text = self.model.get_score(1)

        # Actualiza games y sets como siempre
        self.p1_games.text = str(self.model.get_game_score(0))
        self.p2_games.text = str(self.model.get_game_score(1))
        self.p1_sets.text = str(self.model.get_set_score(0))
        self.p2_sets.text = str(self.model.get_set_score(1))


    def show_game_message(self, message):
        print(message)
