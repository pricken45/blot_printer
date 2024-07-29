import requests
import time
import math
from PIL import Image


DOT_DIAMETER = 1.15
PUSH_COUNT = 1
INPUT_IMAGE = "cat.jpg"
PRINTED_WIDTH = 60

last_x = 0
last_y = 0


def dither(base_width: int = 50):
    img = Image.open("./" + INPUT_IMAGE).convert("L")
    wpercent = base_width / float(img.size[0])
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)
    px = img.load()
    res = []
    for i in range(img.height):
        res.append([])
        for j in range(img.width):
            res[i].append(0)

    for y in range(img.height - 1):
        for x in range(img.width - 1):
            old_pixel = px[x, y]
            newpixel = round(old_pixel / 255)
            res[y][x] = newpixel
            quant_error = old_pixel - newpixel * 255
            res[y][x + 1] = px[x + 1, y] + quant_error * 7 / 16
            res[y + 1][x - 1] = px[x - 1, y + 1] + quant_error * 3 / 16
            res[y + 1][x] = px[x, y + 1] + quant_error * 5 / 16
            res[y + 1][x + 1] = px[x + 1, y + 1] + quant_error * 1 / 16

    res.pop()
    for i in range(len(res)):
        res[i].pop()
    return res


def dot(x, y):
    global last_x
    global last_y

    requests.get("http://localhost:3000/goto?x=" + str(x) + "&y=" + str(y))
    distance = math.sqrt(
        abs(x - last_x) * abs(x - last_x) + abs(y - last_y) * abs(y - last_y)
    )
    last_x = x
    last_y = y
    # print(distance)
    sleep_time = distance * 0.15
    time.sleep(sleep_time)

    for i in range(PUSH_COUNT):
        requests.get("http://localhost:3000/down")
        time.sleep(0.2)
        requests.get("http://localhost:3000/up")
        time.sleep(0.2)


def zero():
    requests.get("http://localhost:3000/up")
    requests.get("http://localhost:3000/goto?x=0&y=0")
    time.sleep(5)


def test_square(w: int = 15):
    # for choosing the right dot diameter
    for i in range(w):
        for j in range(w):
            dot(i * DOT_DIAMETER, j * DOT_DIAMETER)


zero()


def print_picture():
    dithered_image = dither(PRINTED_WIDTH)
    total_dots = len(dithered_image) * len(dithered_image[0])
    completed_dots = 0
    for y in range(len(dithered_image) - 1):
        for x in range(len(dithered_image[0]) - 1):
            completed_dots += 1
            if dithered_image[y][x] == 0:
                dot(x * DOT_DIAMETER, y * DOT_DIAMETER)
                print(str(round((completed_dots / total_dots * 100))) + "% Complete")


print_picture()
