import math
import random
import datetime

import pyxel


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

METEOR_WIDTH = 13
METEOR_HEIGHT = 13

PLAYER_WIDTH = 16
PLAYER_HEIGHT = 48

PLAYER_SPAWN_X = 128
PLAYER_SPAWN_Y = 128

METEOR_MAX_SPEED = 1
METEOR_INITIAL_COUNT = 20

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Meteor:
    def __init__(self, type):

        self.type = type # type from 1 to 6 specifies the type of meteor

        self.pos = Vec2(
            random.randint(*random.choice([(0, PLAYER_SPAWN_X - 20), (PLAYER_SPAWN_X + 20, 255)])),
            random.randint(*random.choice([(0, PLAYER_SPAWN_Y - 20), (PLAYER_SPAWN_Y + 20, 255)]))
            # random.uniform(self.r, SCREEN_WIDTH - self.r),
            # random.uniform(self.r, SCREEN_HEIGHT - self.r),
            )

        self.vel = Vec2(
            random.uniform(-METEOR_MAX_SPEED, METEOR_MAX_SPEED),
            random.uniform(-METEOR_MAX_SPEED, METEOR_MAX_SPEED),
            )

    def update(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        # when a rock exits the screen, another rock is added
        if self.pos.x > 255 or self.pos.y > 255:
            if random.uniform(0, 10) > 5:
                self.pos.x = random.uniform(0, 255)
                self.pos.y = 0
            else:
                self.pos.y = random.uniform(0, 255)
                self.pos.x = 0
        if self.pos.x < 0 or self.pos.y < 0:
            if random.uniform(0, 10) > 5:
                self.pos.x = random.uniform(0, 255)
                self.pos.y = 255
            else:
                self.pos.y = random.uniform(0, 255)
                self.pos.x = 255

class game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.time = datetime.datetime.now()
        self.current_score = 0

        pyxel.load("assets/rock.pyxres")
        
        self.reset()

        pyxel.run(self.update, self.draw)

    def reset(self):
        self.time = datetime.datetime.now()
        self.current_score = 0
        self.game_start = False
        self.death = False
        self.player_x = PLAYER_SPAWN_X
        self.player_y = PLAYER_SPAWN_Y
        self.player_vx = 2
        self.player_vy = 2

        self.meteors1 = [Meteor(random.randint(1, 6)) for _ in range(METEOR_INITIAL_COUNT)]


    def update(self):
        if self.game_start:
            if not self.death:

                meteors1_count = len(self.meteors1)

                self.update_player()

                for i in range(meteors1_count - 1, -1, -1):
                    mi = self.meteors1[i]

                    if ((mi.pos.x <= self.player_x + PLAYER_WIDTH 
                        and mi.pos.x >= self.player_x 
                        and mi.pos.y <= self.player_y + PLAYER_HEIGHT 
                        and mi.pos.y >= self.player_y)
                        or (mi.pos.x + METEOR_WIDTH <= self.player_x + PLAYER_WIDTH 
                        and mi.pos.x + METEOR_WIDTH >= self.player_x 
                        and mi.pos.y + METEOR_HEIGHT <= self.player_y + PLAYER_HEIGHT 
                        and mi.pos.y + METEOR_HEIGHT >= self.player_y)
                        or (mi.pos.x <= self.player_x + PLAYER_WIDTH 
                        and mi.pos.x >= self.player_x 
                        and mi.pos.y + METEOR_HEIGHT <= self.player_y + PLAYER_HEIGHT 
                        and mi.pos.y + METEOR_HEIGHT >= self.player_y)
                        or (mi.pos.x + METEOR_WIDTH <= self.player_x + PLAYER_WIDTH 
                        and mi.pos.x + METEOR_WIDTH >= self.player_x 
                        and mi.pos.y <= self.player_y + PLAYER_HEIGHT 
                        and mi.pos.y >= self.player_y)):
                        self.death_event()

                    mi.update()
            
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
        elif pyxel.btn(pyxel.KEY_S):
            self.reset()
            self.game_start = True

        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

    def death_event(self):
        self.death = True

        pyxel.stop()

    def update_player(self):
        if pyxel.btn(pyxel.KEY_W):
            self.player_y = max(self.player_y - self.player_vy, 0)

        if pyxel.btn(pyxel.KEY_S):
            self.player_y = min(self.player_y + self.player_vy, pyxel.height)

        if pyxel.btn(pyxel.KEY_A):
            self.player_x = max(self.player_x - self.player_vx, 0)

        if pyxel.btn(pyxel.KEY_D):
            self.player_x = min(self.player_x + self.player_vx, pyxel.width)
    
    def draw(self):
        pyxel.cls(0)
        if not self.game_start:
            self.draw_start()
        elif not self.death:
            pyxel.blt(
                self.player_x,
                self.player_y,
                0,
                0,
                0,
                PLAYER_WIDTH,
                PLAYER_HEIGHT,
                12,
            )
        
            for m in self.meteors1:
                if m.type == 1:
                    pyxel.blt(m.pos.x, m.pos.y, 0, 17, 1, METEOR_WIDTH, METEOR_HEIGHT, 12)
                if m.type == 2:
                    pyxel.blt(m.pos.x, m.pos.y, 0, 33, 1, METEOR_WIDTH, METEOR_HEIGHT, 12)
                if m.type == 3:
                    pyxel.blt(m.pos.x, m.pos.y, 0, 17, 17, METEOR_WIDTH, METEOR_HEIGHT, 12)
                if m.type == 4:
                    pyxel.blt(m.pos.x, m.pos.y, 0, 33, 17, METEOR_WIDTH, METEOR_HEIGHT, 12)
                if m.type == 5:
                    pyxel.blt(m.pos.x, m.pos.y, 0, 17, 33, METEOR_WIDTH, METEOR_HEIGHT, 12)
                if m.type == 6:
                    pyxel.blt(m.pos.x, m.pos.y, 0, 33, 33, METEOR_WIDTH, METEOR_HEIGHT, 12)

            self.current_score = (datetime.datetime.now() - self.time).seconds
            pyxel.text(1, 1, "Survive time: " + str(self.current_score) + " seconds", 7)

        else:
            self.draw_death()

    def draw_start(self):
        pyxel.cls(col=8)
        text_x = self.center_text("You are happy to get your first personal spaceship.", SCREEN_WIDTH)
        pyxel.text(text_x, 5, "You are happy to get your first personal spaceship.", 0)
        text_x = self.center_text("And you can't wait to go to space. However, the space", SCREEN_WIDTH)
        pyxel.text(text_x, 15, "And you can't wait to go to space. However, the space", 0)
        text_x = self.center_text("is cluttered with space garbage...", SCREEN_WIDTH)
        pyxel.text(text_x, 25, "is cluttered with space garbage...", 0)
        text_x = self.center_text("Press S to start your journey!!", SCREEN_WIDTH)
        pyxel.text(text_x, 45, "Press S to start your journey!!", 0)
        text_x = self.center_text("Press Q to quit", SCREEN_WIDTH)
        pyxel.text(text_x, 55, "Press Q to quit", 0)

    def draw_death(self):
        pyxel.cls(col=8)

        text_x = self.center_text("GAME OVER", SCREEN_WIDTH)
        pyxel.text(text_x, 5, "GAME OVER", 0)
        text_x = self.center_text("Your score: " + str(self.current_score) + " seconds! WOW!", SCREEN_WIDTH)
        pyxel.text(text_x, 15, "Your score: " + str(self.current_score) + " seconds! WOW!", 0)
        text_x = self.center_text("PRESS R TO RESTART. PRESS Q TO QUIT", SCREEN_WIDTH)
        pyxel.text(text_x, 25, "PRESS R TO RESTART. PRESS Q TO QUIT", 0)

    @staticmethod
    def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
        text_width = len(text) * char_width
        return (page_width - text_width) // 2
game()
