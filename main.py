import math
import random

import pyxel


SCREEN_WIDTH = 256
SCREEN_HEIGHT = 256

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

class game:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)

        pyxel.load("assets/rock.pyxres")
        
        self.reset()

        self.player_x = 72
        self.player_y = -16
        self.player_vx = 0
        self.player_vy = 0
        self.player_is_alive = True

        self.meteors1 = [Meteor() for _ in range(METEOR_INITIAL_COUNT)]

        pyxel.run(self.update, self.draw)

    def reset(self):
        self.death = False

    def update(self):
        meteors1_count = len(self.meteors1)

        self.update_player()

        for i in range(meteors1_count - 1, -1, -1):
            mi = self.meteors1[i]

            # if abs(mi.pos.x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            # is_active = False
            # self.score += (kind + 1) * 100
            # self.player_vy = min(self.player_vy, -8)
            # pyxel.play(3, 4)

            
            mi.update()

    def update_player(self):
        if pyxel.btn(pyxel.KEY_W):
            self.player_y = max(self.player_y - 2, 0)

        if pyxel.btn(pyxel.KEY_S):
            self.player_y = min(self.player_y + 2, pyxel.height)

        if pyxel.btn(pyxel.KEY_A):
            self.player_x = max(self.player_x - 2, 0)

        if pyxel.btn(pyxel.KEY_D):
            self.player_x = min(self.player_x + 2, pyxel.width)
    
    def draw(self):
        pyxel.cls(0)

        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            0,
            0,
            15,
            15,
            12,
        )
        
        for m in self.meteors1:
            pyxel.blt(m.pos.x, m.pos.y, 0, 17, 1, 13, 13, 12)
game()
