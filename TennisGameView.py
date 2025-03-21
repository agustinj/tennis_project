from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from TennisGameModel import Games, TennisGameModel
from GameMessages import GameMessagePopup, GameMessages
from kivy.core.window import Window

# Tamaño inicial de la ventana
Window.size = (800, 350)  # Ajusta según lo que prefieras

class TennisGameView(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, spacing=10, **kwargs)
        self.size_hint = (1, 1)  # Que este layout ocupe toda la ventana
        self.points_font_size = 60  # Tamaño de fuente para los puntos
        self.last_set_scores = [0, 0]  # Guardar la cantidad anterior de sets ganados por cada jugador
        self.last_game_scores = [0, 0]  # Guardar la cantidad anterior de games ganados por cada jugador


        # Inicializar el modelo aquí
        self.model = TennisGameModel()

        # Asignar los nombres a las variables de jugador
        self.player1_name = "Djokovic"
        self.player2_name = "Federer"

        # Contenedor principal
        container = GridLayout(cols=1, size_hint=(1, 1))  # Ocupa todo el espacio disponible

        # Encabezados
        self.scoreboard = GridLayout(cols=4, size_hint_y=None, height=50)
        self.scoreboard.add_widget(Label(text="Player", font_size=self.points_font_size, bold=True, size_hint_x=0.4))
        self.scoreboard.add_widget(Label(text="Points", font_size=self.points_font_size, bold=True, size_hint_x=0.2))
        self.scoreboard.add_widget(Label(text="Games", font_size=self.points_font_size, bold=True, size_hint_x=0.2))
        self.scoreboard.add_widget(Label(text="Sets", font_size=self.points_font_size, bold=True, size_hint_x=0.2))

        container.add_widget(self.scoreboard)

        # Filas de jugadores
        self.players_grid = GridLayout(cols=4, size_hint=(1, 1))  # Expande según el tamaño de la ventana

        self.btn1 = Button(text=self.player1_name, font_size=self.points_font_size, size_hint_x=0.4)
        self.p1_points = Label(text="0", font_size=self.points_font_size, size_hint_x=0.2)
        self.p1_games = Label(text="0", font_size=self.points_font_size, size_hint_x=0.2)
        self.p1_sets = Label(text="0", font_size=self.points_font_size, size_hint_x=0.2)

        self.players_grid.add_widget(self.btn1)
        self.players_grid.add_widget(self.p1_points)
        self.players_grid.add_widget(self.p1_games)
        self.players_grid.add_widget(self.p1_sets)

        self.btn2 = Button(text=self.player2_name, font_size=self.points_font_size, size_hint_x=0.4)
        self.p2_points = Label(text="0", font_size=self.points_font_size, size_hint_x=0.2)
        self.p2_games = Label(text="0", font_size=self.points_font_size, size_hint_x=0.2)
        self.p2_sets = Label(text="0", font_size=self.points_font_size, size_hint_x=0.2)

        self.players_grid.add_widget(self.btn2)
        self.players_grid.add_widget(self.p2_points)
        self.players_grid.add_widget(self.p2_games)
        self.players_grid.add_widget(self.p2_sets)

        container.add_widget(self.players_grid)

        self.add_widget(container)  # Agregarlo al layout principal

        self.btn1.bind(on_press=lambda instance: self.score_point(0))  # Jugador 1
        self.btn2.bind(on_press=lambda instance: self.score_point(1))  # Jugador 2

    def score_point(self, player):
        previous_game_score = [self.model.get_game_score(0), self.model.get_game_score(1)]

        game_winner, set_winner = self.model.score_point(player)

        current_game_score = [self.model.get_game_score(0), self.model.get_game_score(1)]

        # Si el modelo indica que entramos en Tie Break, mostramos el mensaje
        if set_winner == 'tie_break' and not self.model.tie_break.started:
            self.model.tie_break.start()
            GameMessages.show_tiebreak()

        # Muestra el ganador del juego solo si no estamos en Tie Break
        if game_winner and not self.model.tie_break.started:
            GameMessages.show_game_won(player, self.player1_name, self.player2_name)

        # Muestra el ganador del set si es necesario
        if isinstance(set_winner, int) and set_winner > 0:
            GameMessages.show_set_won(player, self.player1_name, self.player2_name)

        # Verifica si alguien ganó el partido
        if self.model.get_set_score(player) == 2:
            GameMessages.show_match_won(player, self.player1_name, self.player2_name, self.on_message_dismissed)

        # Actualiza la UI después de procesar el punto
        self.update_scoreboard()

    def update_scoreboard(self):
        print(f"DEBUG - Actualizando UI: Sets P1: {self.model.get_set_score(0)}, P2: {self.model.get_set_score(1)}")

        # Si está en tie-break, muestra los puntos de tie-break
        if self.model.tie_break.started:
            self.p1_points.text = str(self.model.tie_break.points[0])  # Mostrar puntos del tie-break
            self.p2_points.text = str(self.model.tie_break.points[1])
        else:
            # Actualiza los puntos normales si no está en tie-break
            self.p1_points.text = str(self.model.get_score(0))
            self.p2_points.text = str(self.model.get_score(1))

        # Siempre actualizar juegos y sets, sin importar si es tie-break o no
        self.p1_games.text = str(self.model.get_game_score(0))
        self.p2_games.text = str(self.model.get_game_score(1))
        self.p1_sets.text = str(self.model.get_set_score(0))
        self.p2_sets.text = str(self.model.get_set_score(1))

    def show_game_message(self, message, is_match_winner=False):
        # Desactivar botones
        self.btn1.disabled = True
        self.btn2.disabled = True

        # Mostrar popup con callback para reactivar botones
        popup = GameMessagePopup(message, callback=self.on_message_dismissed, is_match_winner=is_match_winner)
        popup.open()

    def on_message_dismissed(self, reset=False):
        # Reactivar botones
        print("Popup cerrado. Reactivando botones.")
        self.btn1.disabled = False
        self.btn2.disabled = False

        if reset:
            self.reset_match(reset=True)

    def reset_game(self):
        self.model = TennisGameModel()
        self.update_scoreboard()

    def reset_match(self, reset=False):
        print("DEBUG - reset_match fue llamado con reset =", reset)

        if reset:
            print("DEBUG - reset_match fue llamado y ejecutado")
            print(f"DEBUG - Antes de reset: P1 sets: {self.model.get_set_score(0)}, P2 sets: {self.model.get_set_score(1)}")

            self.model.reset()  

            # Verificar que el modelo tiene valores en 0
            print(f"DEBUG - Después del reset: Player 1 games: {self.model.get_game_score(0)}, Player 2 games: {self.model.get_game_score(1)}")
            print(f"DEBUG - Después del reset: Player 1 sets: {self.model.get_set_score(0)}, Player 2 sets: {self.model.get_set_score(1)}")

            # Forzar actualización de la UI
            self.update_scoreboard()

            # Debug para verificar si los sets realmente están en 0
            print(f"DEBUG - Después del reset: Player 1 sets: {self.model.get_set_score(0)}, Player 2 sets: {self.model.get_set_score(1)}")

    def handle_popup_callback(self, reset=False):
        print(f"DEBUG - handle_popup_callback llamado con reset={reset}")
        if reset:
            self.reset_match()  # Reinicia el partido si el popup lo indica
