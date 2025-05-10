from game_logic import *

app = Ursina(title = "Fish Fighter", borderless = True, fullscreen = True)

my_game = Game()

my_game.start_screen()

my_game.close_window_debug()

app.run()