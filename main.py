from kivy.app import App
from TennisGameView import TennisGameView

class TennisApp(App):
    def build(self):
        return TennisGameView()

if __name__ == '__main__':
    TennisApp().run()
