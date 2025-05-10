from ursina import *
from random import *
from ursina.prefabs.first_person_controller import FirstPersonController

class Game():
    """
    Overall game manager, including all menu screens, score, score logic, health, health logic, game start logic, player, enemy, and weapon logic
    """
    def __init__(self) -> None:
        """
        initializes the class with default values to change during gameplay
        """
        self.current_state = None
        self.current_sword = None
        self.current_player = None
        self.monument = None
        self.enemies = []
        self.health = 50
        self.health_display_text = None
        self.score = 0
        self.high_score = 0 
        self.score_display_text = None

    def start_screen(self) -> None:
        """
        logic for the start screen and all its buttons/text
        """
        scene.clear()
        self.set_state("menue")
        hex_color_string = "333333"
        background_color = color.hex(hex_color_string)
        window.color = background_color
        window.exit_button.enabled = True
        

        start_text = Sprite(texture="Title", parent=camera.ui, scale=.4, position=(.03, .13))
        start_button = Button(parent=camera.ui, model="quad", scale=.35, position=(-.55, -.225), texture="Play", color=color.white, highlight_color=color.light_gray, on_click=self.start_game)
        stats_button = Button(parent=camera.ui, model="quad", scale=.35, position=(0, -.225), texture="Stats", color=color.white, highlight_color=color.light_gray, on_click=self.game_stats_scene)
        instructions_button = Button(parent=camera.ui, model="quad", scale=.35, position=(.55, -.225), texture="Inst", color=color.white, highlight_color=color.light_gray, on_click=self.game_instructions_scene)

    def start_game(self) -> None:
        """
        Logic to start the game, called from clicking play button, sets default values and starts a new game, with player, sword, and enemies
        """
        scene.clear()
        self.set_state("game")
        self.health = 50
        self.score = 0
        self.create_world()
        window.exit_button.enabled = False
        self.current_player = Player(game_ref=self, x=10, y=2, origin_y=-.5, speed=15)
        self.current_sword = Sword( game_ref=self)
        self.health_display_text = Text(text = "", color = color.red, position = (.6, .45), scale = 2)
        self.health_display_text.enabled = True 
        self.score_display_text = Text(text="", color=color.orange, position=(.6, .40), scale=2, parent=camera.ui)
        self.score_display_text.enabled = True
        self.update_health_display()
        self.update_score_display()
        self.spawn_enemies()
        

    def game_stats_scene(self) -> None:
        """
        Screen to show high score achieved during playing 
        """
        scene.clear()
        statistics_text = Sprite(texture="Stat_Title", parent=camera.ui, scale=.4, position=(.1, .325))
        stats_back = Sprite(texture="Stats_background", parent=camera.ui, scale=.125, position=(0, -.15))
        high_score = Text(text=f"{self.high_score}", color=color.red, position=(-.225, -.025), scale=10, parent=camera.ui)
        self.set_state("stats")
        self.return_button()

    def game_instructions_scene(self) -> None:
        """
        Screen to show instructions and keybinds 
        """
        scene.clear()
        instructions_text = Sprite(texture="Inst_title", parent=camera.ui, scale=.35, position=(.125, .325))
        instructions_1 = Sprite(texture="Controls", parent=camera.ui, scale=.125, position=(-.55, -.15))
        instructions_2 = Sprite(texture="Inst_2", parent=camera.ui, scale=.125, position=(.25, -.15))
        self.set_state("instructions")
        self.return_button()

    def create_world(self) -> None:
        """
        Creates the world, ocean, and monumemnt in the 3d space, as well as the sky and some subtle fog 
        """
        world_base = Entity(model="cube", scale_x=100, scale_z=100, texture="ground", collider="mesh", name="world_base")
        ocean_base = Entity(model="plane", scale=1000, texture="shore", color=color.blue)
        self.monument = Entity(model="monument", scale=7, position=(0, .5, 0), collider="box", name="monument_base")
        world_sky = Sky(texture="night")
        scene.fog_color = color.black90
        scene.fog_density = 0.02

    def return_button(self) -> None:
        """
        return button to return to start screen if your in stats or instructions window
        """
        return_button = Button(model='quad', scale=.25, position=(-.72, .33), texture="Ret", color=color.white, highlight_color=color.light_gray, on_click=self.start_screen)

    def set_state(self, new_state) -> None:
        """
        Sets current game state based on what you are doing, ie stats = "stats", game = "game"
        """
        self.current_state = new_state

    def close_window_debug(self) -> None:
        """
        Removes the annoying debug overlays present in default URSINA app
        """
        window.fps_counter.enabled = False
        window.entity_counter.enabled = False
        window.collider_counter.enabled = False

    def spawn_enemies(self) -> None:
        """
        Simply spawns 100 enemies and adds them to the list
        """
        for i in range(100): 
            new_enemy = Enemy(player=self.monument, game_ref = self)
            self.enemies.append(new_enemy)

    def update_health_display(self) -> None:
        """
        updates current health to show negative loss of life
        """
        self.health_display_text.text = f"Lives = {self.health}"
    
    def update_score_display(self) -> None:
        """
        updates current score to show positive loss of fish life
        """
        self.score_display_text.text = f"Score: {self.score}"
        
    def minus_health(self) -> None:
        """
        subtracts health, only runs during game, triggers the game over function if health goes to zero (HAPPENS A LOT)
        """
        if not self.current_state == "game":
            return
        self.health -= 1
        self.update_health_display()
        if self.health <= 0:
            self.game_over()
    
    def increment_score(self, amount = 1) -> None:
        """
        increases the score by one per fish death
        """
        if not self.current_state == "game":
            return
        self.score += amount
        self.update_score_display()

    def game_over(self) -> None:
        """
        disables and clears all present entities, updates the high score, and allows return to main menu
        """
        if self.current_player:
            self.current_player.disable()
        if self.current_sword:
            self.current_sword.disable()
        for enemy in self.enemies:
            if enemy and enemy.enabled:
                destroy(enemy)
        self.enemies.clear()
        if self.score > self.high_score:
            self.high_score = self.score
        Text(text = "GameOver", scale = 10, position = (-.65, .325), color = color.red, parent = camera.ui)
        Button(texture = "Ret", color=color.white, scale = .35, position=(0,-.2), highlight_color=color.light_gray, parent = camera.ui, on_click = self.start_screen)
   
class Player(FirstPersonController):
    """
    This class is not really needed, but the default one actually did not include sprinting (i guess i dident need it in the end either), also handles the escape key to close application
    """
    def __init__(self, game_ref, **kwargs) -> None:
        """
        intializes the player character with the option of sprinting, gameref is for accessing the game current_state, **kwargs handles any additional arguments for player   
        """
        super().__init__(**kwargs)
        self.game = game_ref 
        self.base_speed = self.speed
        self.sprint_multiplier = 1.75
        self.sprint_speed = self.base_speed * self.sprint_multiplier

    def update(self) -> None:
        """
        Handles sprinting if left shift is pressed, and closing app if escape 
        """
        if held_keys["left shift"]:
            self.speed = self.sprint_speed
        else:
            self.speed = self.base_speed
        super().update()
        if held_keys["escape"] and self.game.current_state == "game":
            application.quit()


class Sword(Entity):
    """
    This is the "Sword" (lol), had to make it a class because animation from blender aparently do not work, this entire class is to rotate the sword forward, the arguments are the for the same reason as the player class. 
    additionally because collision was not working, i decided to make the sword shoot a bullet and this code handles the swinging and shooting 
    """
    def __init__(self, game_ref, **kwargs) -> None:
        """
        initializes the sword, with its default state, model, etc, and also the parameters for bullet logic
        """
        super().__init__(model="Sword.glb", scale=2, position=(.6, -.5, 0), parent=camera.ui, collider="box", **kwargs)
        self.default_rotation = (-5, 50, 0)
        self.rotation = self.default_rotation 
        self.game = game_ref 
        self.is_swinging = False
        self.shoot_cooldown = 0.1 
        self.last_shot_time = -self.shoot_cooldown 

    def update(self) -> None:
        """
        left mouse down would not work, so if you press e while in game, the "sword" shoots a bullet and "swings"
        """
        if held_keys["e"] and self.game.current_state == "game":
            if time.time() - self.last_shot_time >= self.shoot_cooldown:
                self.swing_and_shoot()
                self.last_shot_time = time.time()

    def swing_and_shoot(self) -> None:
        """
        the way the sword swings is by rotating itself foward then back to original position, and the bullet logic is from the documentation, the bullet shoots out of the camera
        """
        if self.is_swinging: 
             return 
        self.is_swinging = True
        self.rotation = (75, 0, 0)
        bullet_start_pos = camera.world_position + camera.forward * 1.0
        bullet_direction = camera.forward
        Bullet(position=bullet_start_pos, direction=bullet_direction, enemies_list = self.game.enemies, game_ref=self.game)
        invoke(self.return_sword, delay=0.15)

    def return_sword(self) -> None:
        """
        returns sword to original position
        """
        self.rotation = self.default_rotation
        self.is_swinging = False


class Enemy(Entity):
    """
    Arguments are similar to the last two classes, creates a enemy that is a fish model, gives it a random x and z posiotion, and aditionally hadles the logic for moving towards 0,3,0 (cords of monument)
    """
    def __init__(self, player, game_ref, speed = .67, **kwargs) -> None: 
        """
        initializes the fish enemy with its model, collider, and scale, whilst also handling any additional args, 

        PS: This is why game over always instantly happens, i dont have enough time to fix it but they can sometimes spawn at 0,0,0 or nearby and instanly collide with the monument and end the game
        """
        super().__init__(model = "fish.glb", collider = "box", scale = .005, **kwargs)
        self.position = Vec3(randrange(-50, 50), 2.5, randrange(-50, 50))
        self.speed = speed
        self.player_entity = player 
        self.game = game_ref

    def update(self) -> None:
        """
        moves the enemy towards the monument, handles collision between itself and monument, and also updates health if lost
        """
        target_position = self.player_entity.position
        target_position.y = self.position.y 
        direction_to_target = target_position - self.position
        if direction_to_target.length_squared() > (1 * 1):
            self.look_at(target_position) 
            if direction_to_target.length() > 0: 
                self.position += direction_to_target.normalized() * self.speed * time.dt
        hit_info = self.intersects()
        if hit_info.hit:
            destroy(self)
            self.game.minus_health()
        return
    
class Bullet(Entity):
    """
    This is the bullet logic, and credit to this function goes to google gemini 2.5 pro, this is the only thing generated by ai, and it is without a doubt the best thing about this "game" 
    """
    def __init__(self, position, direction, game_ref, **kwargs):
        """
        Initializes the bullet with its speed and lifespan, also destroys the bullet over 3 seconds to not have infinate projectiles 
        """
        super().__init__(model="cube", color=color.yellow, scale=0.1, position=position, collider="box", **kwargs)
        self.direction = direction.normalized() 
        self.speed = 100 
        self.game_ref = game_ref
        self.lifetime = 3 
        destroy(self, delay=self.lifetime)

    def update(self) -> None:
        """
        this is the way the bullet moves, its essentially the same as the way the enemies move but much faster, also handles colision with enemies, and increase the score if needed
        """
        self.position += self.direction * self.speed * time.dt
        hit_info = self.intersects()
        if hit_info.hit:
             if isinstance(hit_info.entity, Enemy):
                if hit_info.entity.enabled: 
                    destroy(hit_info.entity) 
                    if self.game_ref: 
                        self.game_ref.increment_score() 
                    destroy(self)