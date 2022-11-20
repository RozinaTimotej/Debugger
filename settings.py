import os

d = 'levels'

map = []

with open("D:\Faks\Debugger\levels\level1.txt", 'r') as f: #nalaganje levela iz datoteke
    for line in f.readlines():
        map.append(line.strip().split(','))

tile_size = 64
screen_w = 1200
screen_h = tile_size * len(map)
print(screen_h)