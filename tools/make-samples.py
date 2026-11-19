#!/usr/bin/env python3
"""Create two reproducible illustrated Vice City sample photographs."""
from pathlib import Path
import random
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app" / "samples"
W = H = 1080
random.seed(1337)

def gradient(top, bottom):
    im = Image.new("RGB", (W, H)); p = im.load()
    for y in range(H):
        t = y / (H - 1)
        c = tuple(round(a * (1-t) + b*t) for a, b in zip(top, bottom))
        for x in range(W): p[x,y] = c
    return im

def palm(draw, x, base, scale, color):
    pts=[(x,base),(x-8*scale,base-95*scale),(x+12*scale,base-210*scale)]
    draw.line(pts,fill=color,width=max(3,int(12*scale)))
    cx,cy=pts[-1]
    for i in range(7):
        import math
        a=math.pi*2*i/7
        ex=cx+math.cos(a)*115*scale; ey=cy+math.sin(a)*60*scale-12*scale
        draw.line((cx,cy,(cx+ex)/2,cy+math.sin(a)*28*scale,ex,ey),fill=color,width=max(2,int(7*scale)))

def sunset():
    im=gradient((24,9,55),(201,53,78)); d=ImageDraw.Draw(im)
    d.ellipse((360,170,720,530),fill=(255,190,88))
    for y in range(365,540,28): d.rectangle((350,y,730,y+9+(y-365)//18),fill=(130,34,82))
    d.rectangle((0,580,W,690),fill=(235,96,104))
    for y in range(600,760,20): d.line((0,y,W,y+random.randint(-10,10)),fill=(255,176,116),width=2)
    x=0
    while x<W:
        width=random.randint(45,130); top=random.randint(420,670)
        d.rectangle((x,top,x+width,710),fill=(24,12,43))
        if random.random()<.6:d.line((x+width//2,top,x+width//2,top-random.randint(25,90)),fill=(24,12,43),width=5)
        x+=width+random.randint(3,12)
    palm(d,145,1080,1.45,(18,8,34));palm(d,940,1080,1.1,(18,8,34))
    return im

def neon():
    im=gradient((8,8,33),(50,18,65));d=ImageDraw.Draw(im)
    for _ in range(110):
        x=random.randrange(W);y=random.randrange(440);r=random.choice([1,2,3]);d.ellipse((x-r,y-r,x+r,y+r),fill=(185,205,255))
    d.ellipse((820,100,930,210),fill=(255,231,140));d.ellipse((850,75,945,188),fill=(18,12,49))
    x=0
    colors=[(255,44,151),(31,236,244),(255,199,83),(147,78,255)]
    while x<W:
        ww=random.randint(65,150);top=random.randint(390,630);d.rectangle((x,top,x+ww,760),fill=(13,12,35))
        col=random.choice(colors);d.rectangle((x,top,x+ww,top+4),fill=col)
        for wx in range(x+12,x+ww-8,24):
            for wy in range(top+25,730,42):
                if random.random()<.52:d.rectangle((wx,wy,wx+9,wy+17),fill=random.choice(colors))
        x+=ww+9
    d.polygon([(0,700),(1080,700),(1080,1080),(0,1080)],fill=(10,10,25))
    for y in range(745,1080,22):
        spread=(y-700)/380;d.line((540-350*spread,y,540+350*spread,y),fill=random.choice(colors),width=random.choice([2,3,5]))
    palm(d,100,1080,1.1,(8,6,25));palm(d,1000,1080,1.0,(8,6,25))
    return im

OUT.mkdir(parents=True,exist_ok=True)
for name,image in (("sunset",sunset()),("neon",neon())):
    image.save(OUT/f"{name}.jpg",quality=88,optimize=True)
print("Wrote sunset.jpg and neon.jpg in app/samples")
