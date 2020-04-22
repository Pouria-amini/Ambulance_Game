"""
        [===============================================================================================]
        [                                                                                               ]
        [                         Assignment NO: 3                                                      ]
        [                         Question NO: 5                                                        ]
        [                         Author: Mahdi Amini                                                   ]
        [                         P.Con: Using Sprite in Pygame                                         ]
        [                         Date Started: 10-04-2020                                              ]
        [                         Date Finished: 17-04-2020                                             ]
        [                         ICS3UI-02 for Ms. Harris                                              ]
        [                                                                                               ]
        [-----------------------------------------------------------------------------------------------]
        [                                 Program Description                                           ]
        [                                                                                               ]
        [   In this game, Player should not collide with other cars except police car. If player collide]
        [with any car, the game ends and move to the game over screen. If player collides with police c-]
        [ar, It increases the players score. The more player tries to stay on the police car, the more  ]
        [player gains score. the highest score will be saved on a txt file and be compared to player's  ]
        [score and if player exceeds the highest score, player's score will be th highest score.        ]
        [                                                                                               ]
        [-----------------------------------------------------------------------------------------------]
        [                                           Sources                                             ]
        [                                                                                               ]
        [    1-"Ambulance sound"                                                                        ]
        [         http://www.suonoelettronico.com/sound_effects_wav_free_download.asp?testo_            ]
        [         en=Ambulance%20siren.                                                                 ]
        [                                                                                               ]
        [    2-"City sound"                                                                             ]
        [         https://www.freesoundeffects.com/free-sounds/city-sounds-10028/                       ]
        [                                                                                               ]
        [    3-"Car images"                                                                             ]
        [        Created By UnLuckY Studio(CC0 1.0 Universal (CC0 1.0))                                 ]
        [                                                                                               ]
        [    4-"Street image"                                                                           ]
        [        from golgotha set (CC0 1.0 Universal (CC0 1.0))                                        ]
        [===============================================================================================]

       ***
       This Assignment consist of 3 Files (MahdiA3Q5_main, MahdiA3Q5_settings and MahdiA3Q5_sprites)
       ,pictures, sounds and a Text_file (high_score.txt)
       ***
"""
import pygame as pg
import random
import os
import time
from MahdiA3Q5_settings import *
from MahdiA3Q5_sprites import *

class Game:
    def __init__(self):
        """ Initializing the Game """
        pg.init()
        pg.mixer.init()
        self.score = 0
        self.finish_time = 0
        self.additional_score = 0
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.load_highest_score()
        self.city_sound = pg.mixer.Sound(os.path.join(image_dir, 'MahdiA3Q5_City.wav'))
        self.Ambulance_sound = pg.mixer.Sound(os.path.join(image_dir, 'MahdiA3Q5_Ambulance.wav'))
        self.Ambulance_Explosion = pg.mixer.Sound(os.path.join(image_dir, 'MahdiA3Q5_Ambulance_Explosion.ogg'))
        self.city_sound.set_volume(0.6)
        self.Ambulance_sound.set_volume(0.7)

    def load_highest_score(self):
        """ Load highest score from a txt file"""
        with open(path.join(image_dir, HIGH_SCORE_FILE), 'r') as f:
            try:
                self.high_score = int(f.read())
            except:
                self.high_score = 0

    def new(self):
        """ Starting a new Game """
        self.all_sprites = pg.sprite.Group()
        self.cars = pg.sprite.Group()
        self.polices = pg.sprite.Group()
        self.backgrounds = pg.sprite.Group()
        self.background = Road()
        self.all_sprites.add(self.background)
        self.backgrounds.add(self.background)
        self.player = Player()
        self.police = Police()
        self.all_sprites.add(self.police)
        self.all_sprites.add(self.player)
        self.polices.add(self.police)

        Number_of_cars = 3

        # Increase the number of cars after a certain score:
        Increase_cars_Group = [s for s in range(100) if s % 15 == 0]
        for Increase_cars in Increase_cars_Group:
            if self.score > Increase_cars:
                Number_of_cars += 1
                break

        # Create the cars
        for i in range(Number_of_cars):
            self.car = Car()
            self.all_sprites.add(self.car)
            self.cars.add(self.car)

        # Run the Game loop
        self.run()

    def run(self):
        """ The Game loop """
        self.playing = True
        self.city_sound.play(loops=-1)
        self.Ambulance_sound.play(loops=-1)
        while self.playing:
            self.clock.tick(FPS)
            self.event()
            self.update()
            self.draw()

    def event(self):
        """ Game loop events """
        for event in pg.event.get():
            # Check for closing window
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def update(self):
        """ Game loop updates """
        self.all_sprites.update()

        # End the game if Cars collide with the player's car:
        Player_Car_hits = pg.sprite.spritecollide(self.player, self.cars, False)
        if Player_Car_hits:
            self.expl = Explosion(self.player.rect.center)  # Explode the Car
            self.Ambulance_Explosion.play()  # Play the Explosion sound
            self.all_sprites.add(self.expl)
            self.background.kill()  # Stop Background from changing
            self.player.kill()  # Hide player's car
            self.Ambulance_sound.stop()  # mute the Ambulance sound
        if not self.player.alive() and not self.expl.alive():
            self.playing = False

        # Add 1 point to Player's score if it hits a police car
        Player_Police_hits = pg.sprite.spritecollide(self.player, self.polices, False)
        if Player_Police_hits:
            self.additional_score += 1

    def draw(self):
        """ Game loop Draws """

        # Stop the screen from moving after player's car explosion
        if self.background.alive():
            self.screen.fill(WHITE)
        else:
            self.screen.blit(pg.image.load(path.join(image_dir, 'MahdiA3Q5_road0.png')).convert(), (0, 0))

        self.all_sprites.draw(self.screen)

        # Determine the player's from the time passes from the beginning of the game:
        self.finish_time = time.time()
        self.score = self.finish_time - begin_time
        self.score += self.additional_score
        self.draw_text('score = ' + str(int(self.score)), WHITE, 16, WIDTH / 2, 10)

        # *after* drawing everything, flip the display
        pg.display.flip()

    def show_start_screen(self):
        """ Display the start screen """
        if not self.running:
            return
        self.screen.fill(WHITE)
        self.draw_text('Ambulance Game', BLACK, 32, WIDTH / 2, HEIGHT / 4)
        self.draw_text('Highest score: ' + str(self.high_score), BLACK, 28, WIDTH / 2, HEIGHT / 2)
        self.draw_text('!Try to collide with Police cars to gain extra points!', BLACK, 24, WIDTH / 2,
                       HEIGHT * 3 / 4)
        self.draw_text('Press Arrow keys to move', BLACK, 24, WIDTH / 2,
                       HEIGHT * 3 / 4 - 30)
        self.draw_text('Press any key to start the game', BLACK, 24, WIDTH / 2, HEIGHT * 3 / 4 + 30)
        pg.display.flip()
        self.Wait()

    def show_game_over_screen(self):
        """ Display the end screen"""
        if not self.running:
            return
        self.city_sound.stop()  # Mute the city sound
        self.screen.fill(WHITE)
        self.additional_score = 0  # restart the additional score

        # Check if the score achieved by the player is higher than the highest score:
        if self.high_score < int(self.score):
            # If it is, save the player's score as the highest score:
            self.high_score = int(self.score)
            self.draw_text("!Congrats!", BLACK, 50, WIDTH / 2, HEIGHT * 3 / 4 - 70)
            self.draw_text("You Crossed the highest score", BLACK, 32, WIDTH / 2, HEIGHT * 3 / 4)
            with open(path.join(image_dir, HIGH_SCORE_FILE), 'w') as f:
                f.write(str(int(self.score)))

        # Show the player's score:
        self.draw_text('Press any key to Play Again', BLACK, 24, WIDTH / 2, HEIGHT / 4 - 30)
        self.draw_text("Your Score: " + str(int(self.score)), BLACK, 32, WIDTH / 2, HEIGHT / 2 - 10)
        pg.display.flip()
        self.Wait()

    def Wait(self):
        """ Wait for player to press a key to proceed"""
        wait = True
        while wait:
            self.clock.tick(FPS)
            for event in pg.event.get():
                # check for closing window
                if event.type == pg.QUIT:
                    wait = False
                    self.running = False
                    self.playing = False
                if event.type == pg.KEYDOWN:
                    wait = False

    def draw_text(self, text, color, size, x, y):
        """ Draw the text assigned"""
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
begin_time = time.time()
while g.running:
    g.new()
    g.show_game_over_screen()
    begin_time = time.time()

pg.quit()