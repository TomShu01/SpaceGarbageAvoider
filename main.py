import math
import random

import pyxel


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

METEOR_WIDTH = 13
METEOR_HEIGHT = 13

PLAYER_WIDTH = 15
PLAYER_HEIGHT = 15

METEOR_MAX_SPEED = 0.1
METEOR_INITIAL_COUNT = 10

class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Meteor:
    def __init__(self):
        self.r = 5

        self.pos = Vec2(
            random.uniform(self.r, SCREEN_WIDTH - self.r),
            random.uniform(self.r, SCREEN_HEIGHT - self.r),
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

        pyxel.load("assets/rock.pyxres")
        
        self.reset()

        pyxel.run(self.update, self.draw)

    def reset(self):
        self.death = False
        self.player_x = 10
        self.player_y = 10
        self.player_vx = 2
        self.player_vy = 2

        self.meteors1 = [Meteor() for _ in range(METEOR_INITIAL_COUNT)]


    def update(self):
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
        
        if pyxel.btn(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_R):
            self.reset()

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
        if not self.death:
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
                pyxel.blt(m.pos.x, m.pos.y, 0, 17, 1, METEOR_WIDTH, METEOR_HEIGHT, 12)

        else:
            self.draw_death()

    def draw_death(self):
        pyxel.cls(col=8)

        text_x = self.center_text("GAME OVER", SCREEN_WIDTH)
        pyxel.text(text_x, 5, "GAME OVER", 0)

    @staticmethod
    def center_text(text, page_width, char_width=pyxel.FONT_WIDTH):
        text_width = len(text) * char_width
        return (page_width - text_width) // 2
game()
