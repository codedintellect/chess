from logic import game
import ui
import engine

GAME = game()

ui.init(GAME)
engine.start(GAME)
