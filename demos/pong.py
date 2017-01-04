import math
import random

b0=60
b0x=4
b1=60
b1x=123
bar_len=12
spd=2
ball_spd=2.5

top=32
bottom=95

over=False
go=0
start=0

class Ball:
    def __init__(self):
        self.x=64
        self.y=64
        self.vx=0
        self.vy=0
        self.rot=0

ball = Ball()

hit0=0
hit1=0

life_max=5
life0=life_max
life1=life_max

def collide(mx1,my1,mx2,my2,ex1,ey1,ex2,ey2):
    return mx1<=ex2 and ex1<=mx2 and my1<=ey2 and ey1<=my2

def col(bar_x,bar_y):
    global ball, bar_len
    bx1=bar_x
    by1=bar_y
    bx2=bar_x+1
    by2=bar_y+bar_len
    px1=min(ball.x,ball.x+ball.vx)
    py1=min(ball.y,ball.y+ball.vy)
    px2=max(ball.x,ball.x+ball.vx)
    py2=max(ball.y,ball.y+ball.vy)
    return collide(bx1,by1,bx2,by2,px1,py1,px2,py2)

def restart():
    global ball, life0, life1, over, go, start, ball_spd

    rot=0.125+0.25*math.floor(random.randint(0, 8))
    ball.x=64
    ball.y=64
    ball.vx=ball_spd*cos(rot)
    ball.vy=ball_spd*sin(rot)
    ball.rot=rot
    life0=life_max
    life1=life_max
    over=False
    go=0
    start=60

def _init():
	restart()

def update_ball():
    global ball, start, ball_spd, bottom, top, bar_len, hit0, life0, hit1, life1, over, go

    if start>0:
        ball.rot = ball.rot + 0.0625
        ball.vx=ball_spd*cos(ball.rot)
        ball.vy=ball_spd*sin(ball.rot)
        ball.x=64+ball.vx*2
        ball.y=64+ball.vy*2
        start = start - 1

    ball.x = ball.x + ball.vx
    ball.y = ball.y + ball.vy

    bnc=False
    dam=False
    if ball.y<top:
        ball.vy = ball.vy * -1
        ball.y=top
        bnc=True

    if ball.y>bottom:
        ball.vy = ball.vy * -1
        ball.y=bottom
        bnc=True

    if over:
        return

    if ball.x>127:
        ball.vx = ball.vx * -1
        hit1 = hit1 + 20
        dam=True
        life1 = life1 - 1

    if ball.x<0:
        ball.vx = ball.vx * -1
        hit0 = hit0 + 20
        dam=True
        life0 = life0 - 1

    if life0 < 1 or life1 < 1:
        over=True
        go=60


    bx1=ball.x
    by1=ball.y
    bx2=ball.x+ball.vx
    by2=ball.y+ball.vy

    bar_y=None
    if ball.vx<0 and col(b0x,b0):
        bar_y=b0
    if ball.vx>0 and col(b1x,b1):
        bar_y=b1


    if bar_y:
        v=(ball.y-bar_y)/bar_len
        rot=0.15-v*0.3
        if ball.vx>0:
            rot=0.35+v*0.3
        if rot<0:
            rot = rot + 1
        ball.vx=ball_spd*cos(rot)
        ball.vy=ball_spd*sin(rot)
        bnc=True

def ctrl():
    global b0, spd, b1, top, bottom, bar_len

    if btn(2):
        b0 = b0 - spd
    if btn(3):
        b0 = b0 + spd
    if btn(4) or btn(2,1):
        b1 = b1 - spd
    if btn(5) or btn(3,1):
        b1 = b1 + spd
    if b0<top:
        b0=top
    if b0+bar_len>bottom:
        b0=bottom-bar_len
    if b1<top:
        b1=top
    if b1+bar_len>bottom:
        b1=bottom-bar_len

def _update():
    global hit0, hit1, go

    ctrl()
    update_ball()

    if hit0>0:
        hit0 = hit0 - 1
    if hit1>0:
        hit1 = hit1 - 1


    if go>0:
        go = go - 1
        if go==0:
            restart()

def draw_lives():
    global life0, life1

    for i in range(0, (life0)*4, 4):
        rectfill(i,top-3,i+2,top-2,8)

    i0=128-life1*4+1
    for i in range(i0, i0+(life1)*4, 4):
        rectfill(i,top-3,i+2,top-2,8)

def draw_ball():
    global ball
    pset(ball.x, ball.y, 7)

def draw_bars():
    global b0, b0x, b1, b1x, bar_len

    line(b0x, b0, b0x, b0+bar_len,7)
    line(b1x, b1, b1x, b1+bar_len,7)

def draw_tilt():
    global hit0, hit1

    if hit0>4 or hit1>4:
        dx=math.floor(random.randint(0, 8))-4
        dy=math.floor(random.randint(0, 8))-4
        camera(dx,dy)
    else:
        camera(0,0)

def _draw():
    global top, bottom, hit0, hit1, over

    rectfill(0,0,127,127,0)
    rectfill(0,top,127,bottom,5)

    if over:
        if life0>0:
            rectfill(0,top,63,bottom,12)
        elif life1>0:
            rectfill(64,top,127,bottom,12)

    else:
        if hit0>0:
            rectfill(0,top,63,bottom,8)

        if hit1>0:
            rectfill(64,top,127,bottom,8)

    draw_bars()
    draw_ball()
    draw_lives()
    draw_tilt()

def _end():
    return False