from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

def start_screen(): 
    scene.clear()
    start_text = Text(text = "GAME", parent = camera.ui, y =+ .4, scale = 5, color = color.red, origin = (0,0,0))   
    
    start_button = Button(model='quad', scale_x=.5, scale_y = .2, y =+ .2, color=color.white, text="Start Game", text_size=1, text_color=color.black,
                        highlight_color = color.green, on_click = start_game)    

    game_stats = Button(model='quad', scale_x=.5, scale_y = .2, y =- .05, color=color.white, text="Game Stats", text_size=1, text_color=color.black,
                        highlight_color = color.green, on_click = game_stats_scene)    

    game_instructions = Button(model='quad', scale_x=.5, scale_y = .2, y =- .3, color=color.white, text="Game Instructions", text_size=1, text_color=color.black,
                        highlight_color = color.green, on_click = game_instructions_scene)
    

def start_game(): 
    scene.clear()   
    create_world()
    create_player()

def game_stats_scene(): 
    scene.clear()   
    return_button()

def game_instructions_scene():
    scene.clear()  
    return_button()

def input(key): 
    if key == "escape": 
        application.quit()

def create_world(): 
    world_base = Entity(model = "cube", scale_x = 100, scale_z = 100, texture = "grass", collider = "mesh")
    ocean_base =  Entity(model = "plane", scale = 1000, texture = "shore", color = color.azure)
    world_sky = Sky() 

def create_player(): 
    player = FirstPersonController(y=2, origin_y=-.5, speed = 10)
    

def return_button():
    return_button = Button(model='quad', scale_x=.25, scale_y = .1, x =- .6, y =+ .425, color=color.white, text="Return", text_size=1, text_color=color.black,
                        highlight_color = color.green, on_click = start_screen)