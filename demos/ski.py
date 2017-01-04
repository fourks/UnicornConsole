px8 / python cartridge
version 1
__python__

import math
import random
from collections import deque

class Config(object):
    def __init__(self):
        self.speed = 0.7
        self.dist = 0.0
        self.stop = False

    def update(self):
        if not self.stop:
            self.speed += 0.003
            self.dist += self.speed

class Logo(object):
    def __init__(self):
        self.x = 34
        self.y = -150
        self.y_dest = 50
        self.y_dist = 0

class SnowParticle(object):
    def __init__(self):
        pass

    def draw(self):
        circfill(self.x, self.y, self.r, 7)


class Trail(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Player(object):
    def __init__(self, config):
        self.config = config
        self.frame_offset = 0
        self.x = 30
        self.y = 40
        self.dead = False

        self.trail = []
        self.add_trail()

        self.current_state = "center"

        self.state = {
            "center": [10],
            "right": [11, 27],
            "left": [12, 28],
            "dead": [18, 19, 20],
        }

    def add_trail(self):
        self.trail.append(Trail(self.x, self.y))

    def trail_update(self):
        for trail in self.trail:
            trail.y -= self.config.speed

    def trail_draw(self):
        for i in range(0, len(self.trail)):
            n = i + 1
            a = self.trail[i]
            if (i + 1) >= len(self.trail):
                b = self
            else:
                b = self.trail[i+1]

            if b:
                line(a.x + 2, a.y + 8, b.x + 2, b.y + 8, 6)
                line(a.x + 5, a.y + 8, b.x + 5, b.y + 8, 6)

    def set_dead(self):
        if not self.dead:
            self.dead = True
            self.current_state = "dead"
            self.y += 4

    def update(self, timer):
        self.trail_update()

        if not self.dead:
            if btn(0):
                self.x = self.x - 1.5
                self.current_state = "left"
                self.frame_offset = 0
                self.add_trail()
            elif btn(1):
                self.x = self.x + 1.5
                self.current_state = "right"
                self.frame_offset = 0
                self.add_trail()
            else:
                self.current_state = "center"
                self.frame_offset = 0
                if btnp(2):
                    if self.config.speed >= 0.1:
                        self.config.speed -= 0.1
                if btnp(3):
                    self.config.speed += 0.1

        if timer % 5:
            self.frame_offset = (self.frame_offset + 1) % len(self.state[self.current_state])

        if self.x < 0:
            self.x = 0
        if self.x > 120:
            self.x = 120

    def draw(self):
        self.trail_draw()

        if not self.dead:
            spr(3 + self.state[self.current_state][0], self.x, self.y + 3)

        spr(self.state[self.current_state][self.frame_offset], self.x, self.y)


class Background(object):
    def __init__(self, config):
        self.dots = []
        self.config = config

        for i in range(0, 20):
            self.dots.append([random.randint(0, 128), random.randint(0, 128)])

    def update(self):
        for dot in self.dots:
            dot[1] -= self.config.speed
            if dot[1] < 0:
                dot[0] = random.randint(0, 128)
                dot[1] = 127

    def draw(self):
        for dot in self.dots:
            rectfill(dot[0], dot[1], dot[0], dot[1], 6)


class Tree(object):
    def __init__(self, config):
        self.config = config
        self.f = random.randint(0, 4) + 5
        self.x = random.randint(0, 18) * 8
        self.y = 127 + random.randint(0, 8) * 8
        self.col = 0
        if self.f == 5:
            self.col = 3
        elif self.f == 6:
            self.col = 5

    def update(self):
        self.y -= self.config.speed

    def draw(self):
        spr(self.f, self.x, self.y)


class Peoples(object):
    def __init__(self, config, nb):
        self.config = config

        self.l = []
        for i in range(0, nb):
            self.l.append(People(config))

    def update(self):
        idx = 0
        l = []
        for people in self.l:
            if people.y < -10:
                l.append(idx)
                self.l.append(People(self.config))
            idx += 1

        deque((list.pop(self.l, i) for i in sorted(l, reverse=True)), maxlen=0)

        for people in self.l:
            people.update()


    def draw(self):
        for people in self.l:
            people.draw()

class People(object):
    def __init__(self, config):
        self.config = config
        self.dead = False
        self.x = ( random.randint(0, 7) * 8 ) + 28
        self.y = 127 + (random.randint(0, 8)) * 8
        self.f_start = 21
        self.intern_speed = -1

        self.f_offset = 0
        if random.randint(0, 3) < 1:
            self.f_offset = 16

        self.f = self.f_start
        self.anim_tick = 0

    def update(self):
        global timer

        self.y -= self.config.speed + self.intern_speed

        self.anim_tick += 0.5
        if timer % 7 == 0:
            if self.f == 21:
                self.f = 22
            else:
                self.f = 21

    def draw(self):
        spr(3, self.x, self.y + 2)
        spr(self.f + self.f_offset, self.x, self.y)

class Particle(object):
    def __init__(self, config, x, y, col):
        self.config = config
        self.x = x
        self.y = y
        self.col = col
        self.dx = random.randint(0, 2) -1
        self.dy = random.randint(0, 2) -1
        self.vx = random.randint(0, 4) +1
        self.vy = random.randint(0, 4) +1

    def update(self):
        self.vx -= 0.2
        self.vy -= 0.2

        self.x += (self.dx * self.vx)
        self.y += (self.dy * self.vx)

    def draw(self):
        rectfill(self.x, self.y, self.x + 1, self.y + 1, self.col)


class Particles(object):
    def __init__(self, config):
        self.config = config
        self.l = []

    def add(self, x, y, col, num):
        for _ in range(0, num):
            self.l.append(Particle(self.config, x, y, col))

    def update(self):
        idx = 0
        to_del = []
        for particle in self.l:
            if particle.vx < 0 or particle.vy < 0:
                to_del.append(idx)

        deque((list.pop(self.l, i) for i in sorted(to_del, reverse=True)), maxlen=0)

        for particle in self.l:
            particle.update()

    def draw(self):
        for particle in self.l:
            particle.draw()

config = Config()
logo = Logo()
background = Background(config)

snow_particles = []
players = [Player(config)]
peoples = Peoples(config, 3)
particles = Particles(config)

timer = 0
shakescreen = 0

trees = []
for i in range(0, 1):
    trees.append(Tree(config))

state = 'splash'

def _init():
    pass


def tween(current, dest, speed):
    fps = 60
    return dest * fps / speed + current

def logo_update():
    global logo
    logo.y_dist = logo.y_dest - logo.y
    logo.y = tween(logo.y, logo.y_dist, 900)

def collides(a, b):
    bx1 = b.x +2
    bx2 = b.x +6
    by1 = b.y +5
    by2 = b.y +8

    return not ((a.y+8<by1) or (a.y>by2) or	(a.x+8<bx1) or (a.x>bx2))

def _update():
    global config, state, players, background, timer, trees, shakescreen, particles

    timer += 1
    if state == 'splash':
        logo_update()
        if btnp(2):
            fade_out()
            state = 'main'
    else:
        background.update()
        particles.update()
        peoples.update()
        players[0].update(timer)

        config.update()

        idx = 0
        to_del = []
        for tree in trees:
            if (tree.y < -10):
                to_del.append(idx)
                trees.append(Tree(config))
            idx += 1

        deque((list.pop(trees, i) for i in sorted(to_del, reverse=True)), maxlen=0)

        for tree in trees:
            tree.update()

        for tree in trees:
            if collides(tree, players[0]):
                print("BOOM")
                if not players[0].dead:
                    shakescreen = 50
                players[0].set_dead()
                config.speed = 0
                config.stop = True
                particles.add(tree.x + 4, tree.y + 4, tree.col, 10)

                tree.y = -150


    if timer % 100 == 0:
            trees.append(Tree(config))

def fade_out(fa=0.2):
    fa=max(min(1,fa),0)
    fn=8
    pn=15
    fc=1/fn
    fi=math.floor(fa/fc)+1
    fades = [
            [1,1,1,1,0,0,0,0],
            [2,2,2,1,1,0,0,0],
            [3,3,4,5,2,1,1,0],
            [4,4,2,2,1,1,1,0],
            [5,5,2,2,1,1,1,0],
            [6,6,13,5,2,1,1,0],
            [7,7,6,13,5,2,1,0],
            [8,8,9,4,5,2,1,0],
            [9,9,4,5,2,1,1,0],
            [10,15,9,4,5,2,1,0],
            [11,11,3,4,5,2,1,0],
            [12,12,13,5,5,2,1,0],
            [13,13,5,5,2,1,1,0],
            [14,9,9,4,5,2,1,0],
            [15,14,9,4,5,2,1,0],
    ]

    for n in range(1, pn):
        pal(n,fades[n][fi],0)

def fade_out2():
    dpal=[0,1,1, 2,1,13,6,
          4,4,9,3, 13,1,13,14]

    for i in range(0, 40):
        for j in range(1, 15):
            col = j
            for k in range(1, math.floor(((i+(j%5))/4))):
                col=dpal[col]
            pal(j,col,1)


def logo_draw():
    global logo
    w = 8
    h = 4
    start = 67
    remap = 115

    for x in range(0, w):
        for y in range(0, h):
            #print(x+start + (y * 16), logo.x + (x * 8), logo.y + (y*8))
            spr(x+start + (y * 16), logo.x + (x * 8), logo.y + (y*8))

def do_shakescreen():
    global shakescreen

    shakescreen -= 1
    if shakescreen <= 0:
        camera(0,0)
    else:
        camera(random.randint(0, 4)-4, random.randint(0, 4)-4)

def _draw():
    global snow_particles, state, players, background, trees, shakescreen, config

    if state == 'splash':
        rectfill(0, 0, 127, 127, 15)
        rectfill(0, 43, 128, 44, 14)
        rectfill(0, 38, 128, 40, 14)
        rectfill(0, 0, 128, 35, 14)
        rectfill(0, 0, 128, 8, 8)
        rectfill(0, 10, 128, 11, 8)

        spr_map(16,0, 0,0, 128,128)
        spr_map(0,0, 0,0, 128,128)

        logo_draw()

        for snow_particle in snow_particles:
            snow_particle.draw()
    else:
        pal()

        if shakescreen > 0:
            do_shakescreen()
        else:
            camera(0, 0)

        rectfill(0, 0, 127, 127, 7)

        background.draw()
        peoples.draw()
        particles.draw()
        players[0].draw()

        for tree in trees:
            tree.draw()

        px8_print(str(config.dist), 110, 5, 12)


def _end():
    return False



__gfx__
0000000000055000000ee00000000000072772700006000000006000000360000000000044ee000000009000009900000000990000ddddd000d0000000000d00
00000000007575000022220000500500722222770006300000063000003330000000000044888e0000099000000999000099900000ddddd00ddd00000000ddd0
000000000999950000cffc00005005007eeeeee700633300000630000064600000000600448888e000999900000999900999900000ddddd0ddddd000000ddddd
00000000005555000ffffff00050050076666666063333000063330003333300000065604488880004444440004444444444440000ddddd00ddddd0000ddddd0
00000000555775552eeeeee2005005006677677606333330063333300664666000067560448800000b3bb3b000bbb3b33b3bbb0000ddddd000ddddd00ddddd00
0000000005777750022222200050050077777777633333336333333333333330006755564400000099999999099999999999999000ddddd0000dddddddddd000
0000000005977750022002200050050077777777333333330333333000040000067555564400000009999990009999999999990000ddddd00000dddddddd0000
00000000000009000000000000500500777777770004400000044000000400006555555544000000009009000009009009009000000ddd0000000dd00dd00000
0000000000000000077777700777777007777770000000e000000ee0072772700000000000000000000090000000000000000000004444000044440000444400
00000000000000007777797777977977779777770000eee00000ee00722222770000000000000000000990000999990000999990048448400484484004844840
000000000000000079999997799999977999999700eeee0000eeee007eeeeee70000000000000000009999000009999009999000047877400478774004787740
dd000000000000dd7996699779966997799669970022220000222200766666660000000000000000044444400044444444444400048787400487874004878740
dddd00000000dddd766776677667766776677667001ff100001ff1006677677600000000000000000b3bb3b000bbb3b33b3bbb00044444444444444444444440
00dddd0000dddd0067777776677777766777777600ffff0000ffff00777777770000000000000000999999990999999999999990004ff400004ff400004ff400
0000dddddddd000077777777777777777777777702eeee2002eeee20777777770000000000000000099999900099999999999900444ff440044ff440044ff444
000000dddd0000007777777777777777777777770020020000200200777777770000000000000000009009000009009009009000000000400400004004000000
0600006000000000060000600000000000000000000000c000000cc0071771700000000000000000000000000000000000000000000000000000000000000000
08866880060000600886688006000060000000000000ccc00000cc00711111770000000000000000000000000000000000000000000000000000000000000000
666666660886688066666666066666600000000000cccc0000cccc007cccccc70000000000000000000000000000000000000000000000000000000000000000
66ee7e666666666666ee99e606666660000000000011110000111100766666660000000000000000000000000000000000000000000000000000000000000000
067ee760667e7e66069999606699996600000000004ff400004ff400667767760000000000000000000000000000000000000000000000000000000000000000
006666000666660006966960666966960000000000ffff0000ffff00777777770000000000000000000000000000000000000000000000000000000000000000
606666000666660006666660066666600000000001cccc1001cccc10777777770000000000000000000000000000000000000000000000000000000000000000
066ff660006ff606006ff600006ff600000000000010010000100100777777770000000000000000000000000000000000000000000000000000000000000000
006ff606066ff660006ff600006ff600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
006ff600606ff600006ff600006ff600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00666600006666000066660000666600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00666600006666000066660000666600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00600600006006000060060000600600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00600600006006000060060000600600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000600006000000060060000600600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000600006000000060060000600600000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000001111111111000000000000000000000000000000000000000000000000000000000000000000000000000000010000001000000000000000000000000
00000011111111111100000000044444444440004444000044444444440444444444444000444444444400000000000011000011000000000000000000000000
00000111111111111110000000499999999994049999400499999999994499999999999404999999999940000000000011100111000000000000000000000000
00001111111111111111000000499999999999449999404999999999994499999999999449999999999940000000000011111111000000000000000000000000
00011111111111111111100000499994499999449999404999944444440044499999444049999444444400000000000011111111000000000000000000000000
00111111111111111111110000499994499999449999404999944444400000499999400049999444400000000000000011111111000000000000000000000000
01111111111111111111111000499994499999449999404999999999940000499999400049999999940000000000000011111111000000000000000000000000
11111111111111111111111100499999999999449999404999999999940000499999400049999999940000000000000011111111000000000000000000000000
0000000cccccccccc0000000004999999999940499994004999999999940004999994000499999999400000000000000cccccccc000000000000000000000000
000000cccccccccccc000000004999944444400499994000444449999940004999994000499994444000000000000000cccccccc000000000000000000000000
00000cccccccccccccc00000004999940000000499994004444449999940004999994000499994444444000000000000cccccccc000000000000000000000000
0000cccccccccccccccc0000004999940000000499994049999999999940004999994000499999999999400000000000cccccccc000000000000000000000000
000cccccccccccccccccc000004999940000000499994049999999999400004999994000049999999999400000000000cccccccc000000000000000000000000
00cccccccccccccccccccc00000444400000000044440004444444444000000444440000004444444444000000000000cccccccc000000000000000000000000
0cccccccccccccccccccccc0000000000000004444444440000444444444400044444444440000000000000000000000fcfcfcfc000000000000000000000000
cccccccccccccccccccccccc000000000000049999999994004999999999940499999999994000000000000000000000cccccccc000000000000000000000000
000000077777777770000000000000000000499999999999449999999999944999999999994000000000000000000000cfcfcfcf000000000000000000000000
000000777777777777000000000000000000499994499999449999444444404999944444440000000000000000000000ffffffff000000000000000000000000
000007777777777777700000000000000000499994499999449999444400004999944440000000000000000000000000ffffffff000000000000000000000000
000077777777777777770000000000000000499994499999449999999940004999999994000000000000000000000000ffffffff000000000000000000000000
000777777777777777777000000000000000499994499999449999999940004999999994000000000000000000000000ffffffff000000000000000000000000
007777777777777777777700000000000000499994499999449999999940004999999994000000000000000000000000ffffffff000000000000000000000000
077777777777777777777770000000000000499994499999449999444400004999944440000000000000000000000000efefefef000000000000000000000000
777777777777777777777777000000000000499994499999449999400000004999940000000000000000000000000000ffffffff000000000000000000000000
000000077777777770000000000000000000499999999999449999400000004999940000000000000000000000000000fefefefe000000000000000000000000
000000777777777777000000000000000000049999999994049999400000004999940000000000000000000000000000eeeeeeee000000000000000000000000
000007777777777777700000000000000000004444444440004444000000000444400000000000000000000000000000eeeeeeee000000000000000000000000
000077777777777777770000000000000000000000000000000000000000000000000000000000000000000000000000eeeeeeee000000000000000000000000
00077777777cc77777777000000000000000000000000000000000000000000000000000000000000000000000000000eeeeeeee000000000000000000000000
00777c7777cccc7777c77700000000000000000000000000000000000000000000000000000000000000000000000000eeeeeeee000000000000000000000000
0777ccc77cccccc77ccc7770000000000000000000000000000000000000000000000000000000000000000000000000eeeeeeee000000000000000000000000
777cccccccccccccccccc777000000000000000000000000000000000000000000000000000000000000000000000000eeeeeeee000000000000000000000000
66666666666666666666666666666666666666666666666666666666666666666666666666666000000000000000000000000000000000000000000000000000
64444664464444446444466444666446644446644466644664444664446664446444446666446000000000000000000000000000000000000000000000000000
00444464444444444444444444646446444444444464644644444444446464444444444646446660000000000000000000000000000000000000000000000000
00044444444444444444444444446444444444444444644444444444444464444444444644446446000000000000000000000000000000000000000000000000
00655555555555555555555555555555555555555555555555555555555555555555555655555556000000000000000000000000000000000000000000000000
06644444444444444444444444444444444444444444444444444444444444444444444444444444000000000000000000000000000000000000000000000000
06444444444444444444444444444444444444444444444444444444444444444444444444444444000000000000000000000000000000000000000000000000
06444444444444444444444444444444444444444444444444444444444444444444444444444444000000000000000000000000000000000000000000000000
00444444444444444444444444444444444444444444444444444444444444444444444444444444000000000000000000000000000000000000000000000000
06655555555555555555555555555555555555555555555555555555555555555555555555555556000000000000000000000000000000000000000000000000
06444444444444444444444444444444444444444444444444444444444444444444444444444446000000000000000000000000000000000000000000000000
00444444444444444444444444444444444444444444444444444444444444444444444444444446000000000000000000000000000000000000000000000000
00444444444444444444444444444444444444444444444444444444444444444444444444444466000000000000000000000000000000000000000000000000
00000000444400000000444400000000000044440000000000004444000000044400000000000006000000000000000000000000000000000000000000000000
00000000444400000000444400000000000044440000000000004444000000044400000000000006000000000000000000000000000000000000000000000000
00000006646460000006646460000000000664646000000000066464600000646460000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000002020202020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000020202020202020000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
02020202000000000000020202020202020200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0202020200000000f1f2020202020202020202000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000f1f3f3f20202020202000202020202020202000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000000000000f1f3f3f3f3f202020202000202020202020202000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000f1f3f3f3f3f3f3f2020202000000000000020202020200000000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000f1f3f3f3f3f3f3f3f3f20202000000000002020202020202020000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000002f1f3f3f3f3f3f3f3f3f3f3f202000000000000000000020202020000000000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0002f1f3f3f3f3f3f3f3f3f3f3f3f3f2020000000000000000000002020202020202000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
02f1f3f3f3f3f3f3f3f3f3f3f3f3f3f3f20000000000000000000000000202020202000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
__gff__
__map__
0000003f3f3f0000000000000000003f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000003f3f0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000003f00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
000000000000000000000000000000000000003f000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000060620000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000006061616200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000606161616162000000000000000000000000006363000000404263630000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000000606161616161616200000000424b404200000000630000404c41414c630000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
00000060616161616161616162000000414c4141420000006300404141414141630000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000707171717171717171717172000041414141414200636340414141414141630000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0050515151515151515151515151520041414141414142404c41414141414141630000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
5051515151515151515151515151515241414141414141414141414141414141000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
5151515151515151515151515151515141414141414141414141414141414141000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
5151515151515151515151515151515141414141414141414141414141414141000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
5151515151515151515151515151515141414141414141414141414141414141000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
__sfx__
__music__