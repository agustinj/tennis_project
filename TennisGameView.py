from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from TennisGameModel import TennisGameModel

class TennisGameView(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(cols=2, padding=20, spacing=10, **kwargs)
        
        # Modelo que gestiona la lógica
        self.model = TennisGameModel()

        # Grids para la UI
        self.top_grid = GridLayout(cols=2, size_hint_y=None, height=60)
        self.top_grid.add_widget(Label(text="Points", font_size=30))
        self.top_grid.add_widget(Label(text="0", font_size=30))
        self.add_widget(self.top_grid)

        self.bottom_grid = GridLayout(cols=3, size_hint_y=None, height=60)
        self.bottom_grid.add_widget(Label(text="Games", font_size=30))
        self.bottom_grid.add_widget(Label(text="0", font_size=30))
        self.bottom_grid.add_widget(Label(text="0", font_size=30))
        self.add_widget(self.bottom_grid)

        # Botones para los jugadores
        self.player1_row = GridLayout(cols=2, size_hint_y=None, height=60)
        self.btn1 = Button(text="Player 1", font_size=30, on_press=lambda x: self.score_point(0))
        self.p1_points = Label(text="0", font_size=30)
        self.player1_row.add_widget(self.btn1)
        self.player1_row.add_widget(self.p1_points)
        self.add_widget(self.player1_row)

        self.player2_row = GridLayout(cols=2, size_hint_y=None, height=60)
        self.btn2 = Button(text="Player 2", font_size=30, on_press=lambda x: self.score_point(1))
        self.p2_points = Label(text="0", font_size=30)
        self.player2_row.add_widget(self.btn2)
        self.player2_row.add_widget(self.p2_points)
        self.add_widget(self.player2_row)

    def score_point(self, player):
        game_winner = self.model.score_point(player)
        if game_winner:
            self.show_game_message(f"Game - Player {game_winner}")

        self.update_scoreboard()

    def update_scoreboard(self):
        self.p1_points.text = self.model.get_score(0)
        self.p2_points.text = self.model.get_score(1)
        self.bottom_grid.children[1].text = str(self.model.games[0])
        self.bottom_grid.children[2].text = str(self.model.games[1])

    def show_game_message(self, message):
        print(message)
