import pyxel

pyxel.init(256, 256)

# game state:
playerPos = [0, 0] # x, y
pyxel.load("rock.pyxres")

def update():
    if pyxel.btnp(pyxel.KEY_S) and playerPos[1] <= 256:
        playerPos[1] += 1
    if pyxel.btnp(pyxel.KEY_W) and playerPos[1] >= 0:
        playerPos[1] -= 1
    if pyxel.btnp(pyxel.KEY_A) and playerPos[0] >= 0:
        playerPos[0] -= 1
    if pyxel.btnp(pyxel.KEY_D) and playerPos[0] <= 256:
        playerPos[0] += 1
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    pyxel.rect(playerPos[0],playerPos[1],20,20,11)
    pyxel.blt(0, 0, 0, 0, 0, 16, 16)
    pyxel.blt(16, 0, 0, 16, 0, 16, 16)

pyxel.run(update, draw)