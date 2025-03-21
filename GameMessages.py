from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
import TennisGameView

class GameMessagePopup(Popup):
    def __init__(self, message, callback=None, is_match_winner=False, **kwargs):
        super().__init__(title="", size_hint=(None, None), size=(400, 200), auto_dismiss=False, **kwargs)

        # Layout del popup
        content = BoxLayout(orientation="vertical", padding=10, spacing=10)
        content.add_widget(Label(text=message, font_size=30, text_size=(350, None), halign='center'))

        # Callback para cuando se cierre
        self.callback = callback

        # Si es el ganador del partido, agregamos botón de reset
        if is_match_winner:
            reset_btn = Button(text="Reset", font_size=20, size_hint=(None, None), size=(150, 50))
            reset_btn.bind(on_press=self.dismiss_and_reset)
            content.add_widget(reset_btn)

        # Si el mensaje no es el final del partido, cerrar en 2 segundos automáticamente
        if not is_match_winner:
            Clock.schedule_once(self.dismiss_popup, 2)

        self.content = content

    def dismiss_popup(self, dt):
        self.dismiss()
        if self.callback:
            self.callback()

    def dismiss_and_reset(self, instance):
        print("DEBUG - dismiss_and_reset llamado")  # Ver si se ejecuta
        self.dismiss()
        if self.callback:
            self.callback(reset=True)

class GameMessages:
    @staticmethod
    def show_game_won(player, player1_name, player2_name):
        message = f"Game won by {player1_name}!" if player == 0 else f"Game won by {player2_name}!"
        GameMessages.show_message(message)

    @staticmethod
    def show_tiebreak():
        # Solo mostramos el mensaje de Tie Break si ambos jugadores están en 6-6
        message = "Tie Break!"
        GameMessages.show_message(message)

    @staticmethod
    def show_set_won(player, player1_name, player2_name):
        message = f"Set won by {player1_name}!" if player == 0 else f"Set won by {player2_name}!"
        GameMessages.show_message(message)

    @staticmethod
    def show_match_won(player, player1_name, player2_name, callback):
        message = f"Match won by {player1_name}!" if player == 0 else f"Match won by {player2_name}!"
        GameMessages.show_message(message, is_match_winner=True, callback=callback)

    @staticmethod
    def show_message(message, is_match_winner=False, callback=None):
        popup = GameMessagePopup(message, callback=callback, is_match_winner=is_match_winner)
        popup.open()
