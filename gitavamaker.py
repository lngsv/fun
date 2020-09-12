import random
import math

from PIL import ImageDraw, Image

N = 5
PIC_NUM = 20

for cnt in range(PIC_NUM):
    image = Image.new("1", (N, N), 0)
    pixels = image.load()
    half = math.ceil(N / 2)
    for i in range(N):
        for j in range(half):
            pixels[j, i] = random.randint(0,1)

    for i in range(N):
        for j in range(half, N):
            pixels[j, i] = pixels[N - j - 1, i]

    image.save("avas/out" + str(cnt) + ".png", "PNG")
