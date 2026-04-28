"""
File: my_scene.py
Group Members:
    1. ทัศน์นุ สงค์หลง 6510742361
    2. นภัสนันท์ เคลือบวิจิตร 6710742567
"""
import time
import random
from graphics import Canvas

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CANVAS_TITLE = "Space Scene"
FRAME_DELAY = 1 / 30

NUM_STARS = 120
NUM_METEORS = 4
NUM_UFOS = 2
STAR_MAX_SIZE = 3
METEOR_SIZE = 14
METEOR_MIN_SPEED_X = 3
METEOR_MAX_SPEED_X = 9
METEOR_MIN_SPEED_Y = 1
METEOR_MAX_SPEED_Y = 4
UFO_SPEED = 2
ROCKET_BODY_WIDTH = 16
ROCKET_BODY_HEIGHT = 36
ROCKET_SPEED = 7
BG_COLOR = "#05052a"

def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, CANVAS_TITLE)
    draw_background(canvas)
    draw_stars(canvas, NUM_STARS)
    draw_moon(canvas, CANVAS_WIDTH - 170, 45, 95)
    draw_planet(canvas, 80, 110, 80, "coral")
    draw_earth(canvas, 330, 50, 60)
    meteors = create_meteors(canvas, NUM_METEORS)
    ufos = create_ufos(canvas, NUM_UFOS)
    rockets = []

    def on_mouse_pressed(x, y):
        new_rocket = draw_rocket(canvas, x, y)
        rockets.append(new_rocket)

    canvas.on_mouse_pressed = on_mouse_pressed
    while True:
        animate_meteors(canvas, meteors)
        animate_ufos(canvas, ufos)
        animate_rockets(canvas, rockets)
        canvas.update()
        time.sleep(FRAME_DELAY)

def draw_background(canvas):
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT,
                            fill=BG_COLOR, outline=BG_COLOR)

def draw_stars(canvas, count):
    for i in range(count):
        x = random.randint(0, CANVAS_WIDTH)
        y = random.randint(0, CANVAS_HEIGHT)
        size = random.randint(1, STAR_MAX_SIZE)
        canvas.create_oval(x, y, x + size, y + size, fill="white", outline="white")

def draw_moon(canvas, x, y, size):
    canvas.create_oval(x, y, x + size, y + size, fill="#f5e642", outline="#f5e642")
    crater_size = size // 6
    canvas.create_oval(x + size // 4, y + size // 3,
                       x + size // 4 + crater_size, y + size // 3 + crater_size,
                       fill="#d4c830", outline="#d4c830")
    canvas.create_oval(x + size // 2, y + size // 5,
                       x + size // 2 + crater_size, y + size // 5 + crater_size,
                       fill="#d4c830", outline="#d4c830")

def draw_planet(canvas, x, y, size, color):
    ring_pad = size // 3
    canvas.create_oval(x - ring_pad, y + size // 3,
                       x + size + ring_pad, y + size * 2 // 3,
                       fill="", outline="#cccccc", width=2)
    canvas.create_oval(x, y, x + size, y + size, fill=color, outline=color)

def draw_earth(canvas, x, y, size):
    canvas.create_oval(x, y, x + size, y + size, fill="#1e6fb8", outline="#0f4f8a")
    canvas.create_oval(x + size // 5, y + size // 4,
                       x + size // 2, y + size // 2,
                       fill="#2d8c3a", outline="#2d8c3a")
    canvas.create_oval(x + size // 2, y + size // 6,
                       x + size * 3 // 4, y + size // 3,
                       fill="#2d8c3a", outline="#2d8c3a")
    canvas.create_oval(x + size // 3, y + size * 3 // 5,
                       x + size * 2 // 3, y + size * 4 // 5,
                       fill="#2d8c3a", outline="#2d8c3a")

def draw_meteor(canvas, x, y):
    meteor = canvas.create_oval(x, y, x + METEOR_SIZE, y + METEOR_SIZE,
                                fill="white", outline="lightyellow")
    return meteor

def draw_ufo(canvas, x, y):
    body = canvas.create_oval(x, y, x + 60, y + 18, fill="silver", outline="gray")
    dome = canvas.create_oval(x + 15, y - 15, x + 45, y + 8,
                              fill="lightblue", outline="white")
    return body, dome

def draw_rocket(canvas, x, y):
    half_w = ROCKET_BODY_WIDTH // 2
    half_h = ROCKET_BODY_HEIGHT // 2
    body = canvas.create_rectangle(x - half_w, y - half_h, x + half_w, y + half_h, fill="white", outline="gray")
    nose = canvas.create_oval(x - half_w, y - half_h - 14, x + half_w, y - half_h + 6, fill="red", outline="darkred")
    window = canvas.create_oval(x - 5, y - 6, x + 5, y + 4, fill="lightblue", outline="blue")
    left_fin = canvas.create_rectangle(x - half_w - 6, y + half_h - 10, x - half_w, y + half_h, fill="red", outline="darkred")
    right_fin = canvas.create_rectangle(x + half_w, y + half_h - 10, x + half_w + 6, y + half_h, fill="red", outline="darkred")
    flame = canvas.create_oval(x - 6, y + half_h, x + 6, y + half_h + 14, fill="orange", outline="yellow")
    parts = []
    parts.append(body)
    parts.append(nose)
    parts.append(window)
    parts.append(left_fin)
    parts.append(right_fin)
    parts.append(flame)
    return parts

def create_meteors(canvas, count):
    meteors = []
    for i in range(count):
        x = random.randint(-CANVAS_WIDTH, CANVAS_WIDTH // 2)
        y = random.randint(-50, CANVAS_HEIGHT // 2)
        speed_x = random.randint(METEOR_MIN_SPEED_X, METEOR_MAX_SPEED_X)
        speed_y = random.randint(METEOR_MIN_SPEED_Y, METEOR_MAX_SPEED_Y)
        meteor = draw_meteor(canvas, x, y)
        meteor_data = (meteor, speed_x, speed_y)
        meteors.append(meteor_data)
    return meteors

def create_ufos(canvas, count):
    ufos = []
    for i in range(count):
        y_home = 200 + i * 180
        body, dome = draw_ufo(canvas, -60 - i * 250, y_home)
        ufo_data = (body, dome, y_home)
        ufos.append(ufo_data)
    return ufos

def animate_meteors(canvas, meteors):
    for meteor_data in meteors:
        meteor = meteor_data[0]
        speed_x = meteor_data[1]
        speed_y = meteor_data[2]
        canvas.move(meteor, speed_x, speed_y)
        current_x = canvas.get_left_x(meteor)
        current_y = canvas.get_top_y(meteor)
        if current_x > CANVAS_WIDTH or current_y > CANVAS_HEIGHT:
            new_y = random.randint(-50, CANVAS_HEIGHT // 2)
            canvas.move_to(meteor, -METEOR_SIZE, new_y)

def animate_ufos(canvas, ufos):
    for ufo_data in ufos:
        body = ufo_data[0]
        dome = ufo_data[1]
        y_home = ufo_data[2]
        canvas.move(body, UFO_SPEED, 0)
        canvas.move(dome, UFO_SPEED, 0)
        if canvas.get_left_x(body) > CANVAS_WIDTH:
            canvas.move_to(body, -60, y_home)
            canvas.move_to(dome, -45, y_home - 15)

def animate_rockets(canvas, rockets):
    rockets_copy = list(rockets)
    for parts in rockets_copy:
        for part in parts:
            canvas.move(part, 0, -ROCKET_SPEED)
        body = parts[0]
        body_top_y = canvas.get_top_y(body)
        if body_top_y < -ROCKET_BODY_HEIGHT:
            for part in parts:
                canvas.delete(part)
            rockets.remove(parts)

if __name__ == "__main__":
    main()
