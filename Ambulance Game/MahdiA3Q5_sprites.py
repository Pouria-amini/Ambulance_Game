"""
This File defines the properties of sprites

"""
import pygame as pg
from MahdiA3Q5_settings import *
import random
from os import path

vector = pg.math.Vector2

current_dir = path.dirname(__file__)
image_dir = path.join(current_dir, 'MahdiA3Q5-img & snd')


class Car(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.load_images()
        self.image = self.Cars_frames[random.randrange(5)]
        self.image.set_colorkey(BLACK)  # Hide the dark part of the sprite
        self.rect = self.image.get_rect()  # Get the rectangular size of the sprite
        # Spread the cars to the top, right and left parts, out of the screen and randomise them:
        self.rect.x = random.randrange(-100, WIDTH + 100)
        self.rect.y = random.randrange(-1000, -50)
        self.speedx = random.randrange(-3, 6)
        self.speedy = random.randrange(5, 6)

    def load_images(self):
        """ Load the images for cars """
        self.Cars_frames = [pg.transform.scale(pg.image.load(path.join(image_dir, 'MahdiA3Q5_car1.png')).convert(), (34, 71)),
                            pg.transform.scale(pg.image.load(path.join(image_dir, 'MahdiA3Q5_car2.png')).convert(), (34, 71)),
                            pg.transform.scale(pg.image.load(path.join(image_dir, 'MahdiA3Q5_car3.png')).convert(), (34, 71)),
                            pg.transform.scale(pg.image.load(path.join(image_dir, 'MahdiA3Q5_car4.png')).convert(), (34, 71)),
                            pg.transform.scale(pg.image.load(path.join(image_dir, 'MahdiA3Q5_car5.png')).convert(), (34, 71))]

    def update(self):
        """ Move the cars to the screen """
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Hide the cars after leaving the screen and draw them again:
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(-100, WIDTH + 100)
            self.rect.y = -20
            self.speedx = random.randrange(-3, 6)
            self.speedy = random.randrange(5, 6)


class Police(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.police_frames[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        # Spread the cars to the top, right and left parts, out of the screen and randomise them:
        self.rect.x = random.randrange(-100, WIDTH + 100)
        self.rect.y = random.randrange(-600, -50)
        self.speedx = random.randrange(-3, 6)
        self.speedy = random.randrange(5, 6)

    def load_images(self):
        """ Load the images for police car """
        self.police_frames = [
            pg.transform.scale(pg.image.load(path.join(image_dir, 'MahdiA3Q5_Police1.png')).convert(), (34, 71)),
            pg.transform.scale(pg.image.load(path.join(image_dir, 'MahdiA3Q5_Police2.png')).convert(), (34, 71)),
            pg.transform.scale(pg.image.load(path.join(image_dir, 'MahdiA3Q5_Police3.png')).convert(), (34, 71))]
        # Apply set_colorkey to all the frames
        for frame in self.police_frames:
            frame.set_colorkey(BLACK)

    def update(self):
        """ Move the car to the screen """
        self.animate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # Hide the cars after leaving the screen and draw them again:
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(-100, WIDTH + 100)
            self.rect.y = -20
            self.speedx = random.randrange(-3, 6)
            self.speedy = random.randrange(5, 6)

    def animate(self):
        """ change the sprite of the police car any 150 frames"""
        now = pg.time.get_ticks()
        if now - self.last_update > 150:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.police_frames)
            self.image = self.police_frames[self.current_frame]


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.current_frame = 0
        self.last_update = 0
        self.load_image()
        self.image = self.ambulance_light_frames[0]
        # Get the rectangular size of the sprite:
        self.rect = self.image.get_rect()
        # Using vector to define position, velocity and acceleration of the sprite:
        self.pos = vector(WIDTH / 2, HEIGHT - 100)
        self.vel = vector(0, 0)
        self.acc = vector(0, 0)

    def load_image(self):
        """ Load the images for player's car """
        self.ambulance_light_frames = [
            pg.transform.scale(pg.image.load(path.join(image_dir, 'MahdiA3Q5_Ambulance1.png')).convert(), (50, 103)),
            pg.transform.scale(pg.image.load(path.join(image_dir, 'MahdiA3Q5_Ambulance2.png')).convert(), (50, 103)),
            pg.transform.scale(pg.image.load(path.join(image_dir, 'MahdiA3Q5_Ambulance3.png')).convert(), (50, 103))]
        for frame in self.ambulance_light_frames:
            frame.set_colorkey(BLACK)

    def update(self):
        """ Define the movements of the player """
        self.animate()
        self.acc = vector(0, 0)
        # Change the acceleration in the sprite:
        key = pg.key.get_pressed()
        if key[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if key[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if key[pg.K_UP]:
            self.acc.y = -PLAYER_ACC
        if key[pg.K_DOWN]:
            self.acc.y = PLAYER_ACC

        # Slowing down the movement of the sprite after its motion:
        self.acc += self.vel * PLAYER_FRICTION
        # Adding the acceleration to velocity in order to change it:
        self.vel += self.acc
        # Using the Physics formula to find the position of the sprite after changing its velocity and acceleration:
        self.pos += self.vel + 0.5 * self.acc
        # locating the sprite after applying acceleration:
        self.rect.center = self.pos

        # Making the sprite to stay on the screen
        if self.rect.top < 0:
            self.rect.top = 0
            self.pos = (self.rect.centerx, self.rect.centery)
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.pos = (self.rect.centerx, self.rect.centery)
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.pos = (self.rect.centerx, self.rect.centery)
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos = (self.rect.centerx, self.rect.centery)

    def animate(self):
        """ change the sprite of the player's car any 150 frames"""
        now = pg.time.get_ticks()
        if now - self.last_update > 150:
            self.last_update = now
            """
            Change the current frame to the next one and get the
            mode of it to stop it from crossing the limit frame
            """
            self.current_frame = (self.current_frame + 1) % len(self.ambulance_light_frames)
            self.image = self.ambulance_light_frames[self.current_frame]


class Explosion(pg.sprite.Sprite):
    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.frame = 0
        self.last_update = pg.time.get_ticks()
        self.frame_rate = 50
        self.load_images()
        self.image = self.explosion_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = center  # Set the center of the explosion to the center of the player's car

    def load_images(self):
        """ Load the explosion images """
        self.explosion_frames = []
        for i in range(8):
            file_name = 'MahdiA3Q5_sonicExplosion0{}.png'.format(i)
            picture = pg.image.load(path.join(image_dir, file_name)).convert()
            self.explosion_frames.append(picture)
        for frame in self.explosion_frames:
            frame.set_colorkey(BLACK)

    def update(self):
        """ Change the Frame of explosion according to frame_rate """
        now = pg.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1

            # Destroy the object after finishing it's frames:
            if self.frame == len(self.explosion_frames):
                self.kill()

            # Go to the next fame if there is more
            else:
                center = self.rect.center
                self.image = self.explosion_frames[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Road(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.last_update = pg.time.get_ticks()
        self.frame = 0
        self.load_images()
        self.image = self.road_frames[0]
        self.rect = self.image.get_rect()

    def load_images(self):
        """ Load the road images """
        self.road_frames = []
        for i in range(7):
            self.road_frames.append(pg.image.load(path.join(image_dir, 'MahdiA3Q5_road{}.png').format(i)).convert())

    def update(self):
        """ Change the Frame of road according to frame_rate which is 20 """
        now = pg.time.get_ticks()
        if now - self.last_update > 20:
            self.last_update = now
            self.frame += 1

            # Reload the images after reaching the last frame
            if self.frame == len(self.road_frames):
                self.frame = 0

            # Go to the next fame
            else:
                self.image = self.road_frames[self.frame]