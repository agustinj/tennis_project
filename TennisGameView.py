from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
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

        # Labels de games
        self.p1_games = Label(text="0", font_size=30)
        self.p2_games = Label(text="0", font_size=30)
        self.bottom_grid.add_widget(self.p1_games)
        self.bottom_grid.add_widget(self.p2_games)
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
            self.model.points.reset()  # Reseteamos puntos después de ganar un game

        self.update_scoreboard()

    def update_scoreboard(self):
        self.p1_points.text = self.model.get_score(0)
        self.p2_points.text = self.model.get_score(1)
        self.p1_games.text = str(self.model.games[0])
        self.p2_games.text = str(self.model.games[1])

    def show_game_message(self, message):
        popup_layout = BoxLayout(orientation="vertical")
        popup_label = Label(text=message, font_size=30)
        close_button = Button(text="OK", size_hint_y=None, height=50)
        
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_button)
        
        popup = Popup(title="Game Won!", content=popup_layout, size_hint=(None, None), size=(300, 200))
        close_button.bind(on_press=popup.dismiss)
        
        popup.open()
