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
BG_COLOR = "#05052a"

NUM_STARS = 120
STAR_MIN_SIZE = 1
STAR_MAX_SIZE = 3
STAR_COLOR = "white"

MOON_X = CANVAS_WIDTH - 170
MOON_Y = 45
MOON_SIZE = 95
MOON_COLOR = "#f5e642"
MOON_CRATER_COLOR = "#d4c830"

SATURN_X = 80
SATURN_Y = 110
SATURN_SIZE = 80
SATURN_COLOR = "coral"
RING_COLOR = "#cccccc"
RING_WIDTH = 2

EARTH_X = 330
EARTH_Y = 50
EARTH_SIZE = 60
EARTH_OCEAN_FILL = "#1e6fb8"
EARTH_OCEAN_OUTLINE = "#0f4f8a"
EARTH_LAND_COLOR = "#2d8c3a"

NUM_METEORS = 4
METEOR_SIZE = 14
METEOR_MIN_SPEED_X = 3
METEOR_MAX_SPEED_X = 9
METEOR_MIN_SPEED_Y = 1
METEOR_MAX_SPEED_Y = 4
METEOR_FILL = "white"
METEOR_OUTLINE = "lightyellow"
METEOR_SPAWN_Y_MIN = -50

NUM_UFOS = 2
UFO_SPEED = 2
UFO_BODY_WIDTH = 60
UFO_BODY_HEIGHT = 18
UFO_DOME_OFFSET_X = 15
UFO_DOME_OFFSET_Y = 15
UFO_DOME_WIDTH = 30
UFO_DOME_BOTTOM_OFFSET = 8
UFO_FIRST_Y = 200
UFO_VERTICAL_GAP = 180
UFO_HORIZONTAL_GAP = 250
UFO_RESET_X = -60
UFO_DOME_RESET_OFFSET_X = 15
UFO_BODY_FILL = "silver"
UFO_BODY_OUTLINE = "gray"
UFO_DOME_FILL = "lightblue"
UFO_DOME_OUTLINE = "white"

ROCKET_BODY_WIDTH = 16
ROCKET_BODY_HEIGHT = 36
ROCKET_NOSE_HEIGHT = 14
ROCKET_NOSE_OVERLAP = 6
ROCKET_WINDOW_HALF_W = 5
ROCKET_WINDOW_TOP_OFFSET = 6
ROCKET_WINDOW_BOTTOM_OFFSET = 4
ROCKET_FIN_WIDTH = 6
ROCKET_FIN_HEIGHT = 10
ROCKET_FLAME_HALF_W = 6
ROCKET_FLAME_HEIGHT = 14
ROCKET_SPEED = 7
ROCKET_BODY_FILL = "white"
ROCKET_BODY_OUTLINE = "gray"
ROCKET_RED_FILL = "red"
ROCKET_RED_OUTLINE = "darkred"
ROCKET_WINDOW_FILL = "lightblue"
ROCKET_WINDOW_OUTLINE = "blue"
ROCKET_FLAME_FILL = "orange"
ROCKET_FLAME_OUTLINE = "yellow"


def main():
    """ฟังก์ชันหลัก: สร้าง canvas วาดฉาก และรันลูปแอนิเมชัน"""
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, CANVAS_TITLE)
    draw_background(canvas)
    draw_stars(canvas, NUM_STARS)
    draw_moon(canvas, MOON_X, MOON_Y, MOON_SIZE)
    draw_planet(canvas, SATURN_X, SATURN_Y, SATURN_SIZE, SATURN_COLOR)
    draw_earth(canvas, EARTH_X, EARTH_Y, EARTH_SIZE)
    meteors = create_meteors(canvas, NUM_METEORS)
    ufos = create_ufos(canvas, NUM_UFOS)
    rockets = []

    def on_mouse_pressed(x, y):
        """ฟังก์ชันที่จะถูกเรียกเมื่อผู้ใช้คลิกบน canvas → ยิงจรวดที่จุดคลิก"""
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
    """วาดพื้นหลังอวกาศสีน้ำเงินดำเต็มหน้าจอ"""
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT,
                            fill=BG_COLOR, outline=BG_COLOR)


def draw_stars(canvas, count):
    """วาดดาวเล็กๆ กระจายทั่วท้องฟ้าด้วยลูป

    Args:
        canvas: หน้าต่าง canvas ที่จะวาด
        count: จำนวนดาวที่จะวาด
    """
    for i in range(count):
        x = random.randint(0, CANVAS_WIDTH)
        y = random.randint(0, CANVAS_HEIGHT)
        size = random.randint(STAR_MIN_SIZE, STAR_MAX_SIZE)
        canvas.create_oval(x, y, x + size, y + size,
                           fill=STAR_COLOR, outline=STAR_COLOR)


def draw_moon(canvas, x, y, size):
    """วาดดวงจันทร์พร้อมหลุมอุกกาบาต 2 หลุม

    Args:
        canvas: หน้าต่าง canvas
        x: พิกัด x ของมุมบนซ้ายของดวงจันทร์
        y: พิกัด y ของมุมบนซ้ายของดวงจันทร์
        size: เส้นผ่านศูนย์กลางของดวงจันทร์
    """
    canvas.create_oval(x, y, x + size, y + size,
                       fill=MOON_COLOR, outline=MOON_COLOR)
    crater_size = size // 6
    canvas.create_oval(x + size // 4, y + size // 3,
                       x + size // 4 + crater_size, y + size // 3 + crater_size,
                       fill=MOON_CRATER_COLOR, outline=MOON_CRATER_COLOR)
    canvas.create_oval(x + size // 2, y + size // 5,
                       x + size // 2 + crater_size, y + size // 5 + crater_size,
                       fill=MOON_CRATER_COLOR, outline=MOON_CRATER_COLOR)


def draw_planet(canvas, x, y, size, color):
    """วาดดาวเคราะห์พร้อมวงแหวน

    Args:
        canvas: หน้าต่าง canvas
        x: พิกัด x ของมุมบนซ้ายของตัวดาวเคราะห์
        y: พิกัด y ของมุมบนซ้ายของตัวดาวเคราะห์
        size: เส้นผ่านศูนย์กลางของดาวเคราะห์
        color: สีของดาวเคราะห์
    """
    ring_pad = size // 3
    canvas.create_oval(x - ring_pad, y + size // 3,
                       x + size + ring_pad, y + size * 2 // 3,
                       fill="", outline=RING_COLOR, width=RING_WIDTH)
    canvas.create_oval(x, y, x + size, y + size, fill=color, outline=color)


def draw_earth(canvas, x, y, size):
    """วาดดาวโลก: ทรงกลมสีน้ำเงิน (มหาสมุทร) + ทวีปสีเขียว

    Args:
        canvas: หน้าต่าง canvas
        x: พิกัด x ของมุมบนซ้าย
        y: พิกัด y ของมุมบนซ้าย
        size: เส้นผ่านศูนย์กลางของดาวโลก
    """
    canvas.create_oval(x, y, x + size, y + size,
                       fill=EARTH_OCEAN_FILL, outline=EARTH_OCEAN_OUTLINE)
    canvas.create_oval(x + size // 5, y + size // 4,
                       x + size // 2, y + size // 2,
                       fill=EARTH_LAND_COLOR, outline=EARTH_LAND_COLOR)
    canvas.create_oval(x + size // 2, y + size // 6,
                       x + size * 3 // 4, y + size // 3,
                       fill=EARTH_LAND_COLOR, outline=EARTH_LAND_COLOR)
    canvas.create_oval(x + size // 3, y + size * 3 // 5,
                       x + size * 2 // 3, y + size * 4 // 5,
                       fill=EARTH_LAND_COLOR, outline=EARTH_LAND_COLOR)


def draw_meteor(canvas, x, y):
    """วาดอุกกาบาต 1 ลูกแล้วคืนค่าวัตถุไปให้ใช้ในแอนิเมชัน

    Args:
        canvas: หน้าต่าง canvas
        x: พิกัด x เริ่มต้น
        y: พิกัด y เริ่มต้น

    Returns:
        วัตถุอุกกาบาต (oval object)
    """
    meteor = canvas.create_oval(x, y, x + METEOR_SIZE, y + METEOR_SIZE,
                                fill=METEOR_FILL, outline=METEOR_OUTLINE)
    return meteor


def draw_ufo(canvas, x, y):
    """วาด UFO 1 ลำ (ตัวเงิน + โดมฟ้าด้านบน) แล้วคืนค่าทั้งสองส่วน

    Args:
        canvas: หน้าต่าง canvas
        x: พิกัด x เริ่มต้นของตัว UFO
        y: พิกัด y เริ่มต้นของตัว UFO

    Returns:
        ทูเปิล (body, dome) - สองชิ้นส่วนของ UFO
    """
    body = canvas.create_oval(x, y, x + UFO_BODY_WIDTH, y + UFO_BODY_HEIGHT,
                              fill=UFO_BODY_FILL, outline=UFO_BODY_OUTLINE)
    dome = canvas.create_oval(x + UFO_DOME_OFFSET_X, y - UFO_DOME_OFFSET_Y,
                              x + UFO_DOME_OFFSET_X + UFO_DOME_WIDTH,
                              y + UFO_DOME_BOTTOM_OFFSET,
                              fill=UFO_DOME_FILL, outline=UFO_DOME_OUTLINE)
    return body, dome


def draw_rocket(canvas, x, y):
    """วาดจรวดที่ประกอบด้วยหลายชิ้นส่วน ณ ตำแหน่งที่กำหนด

    Args:
        canvas: หน้าต่าง canvas
        x: พิกัด x ของจุดกลางจรวด
        y: พิกัด y ของจุดกลางจรวด

    Returns:
        ลิสต์ของชิ้นส่วนจรวด (ใช้เพื่อขยับและลบทุกชิ้นพร้อมกัน)
    """
    half_w = ROCKET_BODY_WIDTH // 2
    half_h = ROCKET_BODY_HEIGHT // 2
    body = canvas.create_rectangle(x - half_w, y - half_h, x + half_w, y + half_h,
                                   fill=ROCKET_BODY_FILL, outline=ROCKET_BODY_OUTLINE)
    nose = canvas.create_oval(x - half_w, y - half_h - ROCKET_NOSE_HEIGHT,
                              x + half_w, y - half_h + ROCKET_NOSE_OVERLAP,
                              fill=ROCKET_RED_FILL, outline=ROCKET_RED_OUTLINE)
    window = canvas.create_oval(x - ROCKET_WINDOW_HALF_W, y - ROCKET_WINDOW_TOP_OFFSET,
                                x + ROCKET_WINDOW_HALF_W, y + ROCKET_WINDOW_BOTTOM_OFFSET,
                                fill=ROCKET_WINDOW_FILL, outline=ROCKET_WINDOW_OUTLINE)
    left_fin = canvas.create_rectangle(x - half_w - ROCKET_FIN_WIDTH, y + half_h - ROCKET_FIN_HEIGHT,
                                       x - half_w, y + half_h,
                                       fill=ROCKET_RED_FILL, outline=ROCKET_RED_OUTLINE)
    right_fin = canvas.create_rectangle(x + half_w, y + half_h - ROCKET_FIN_HEIGHT,
                                        x + half_w + ROCKET_FIN_WIDTH, y + half_h,
                                        fill=ROCKET_RED_FILL, outline=ROCKET_RED_OUTLINE)
    flame = canvas.create_oval(x - ROCKET_FLAME_HALF_W, y + half_h,
                               x + ROCKET_FLAME_HALF_W, y + half_h + ROCKET_FLAME_HEIGHT,
                               fill=ROCKET_FLAME_FILL, outline=ROCKET_FLAME_OUTLINE)
    parts = []
    parts.append(body)
    parts.append(nose)
    parts.append(window)
    parts.append(left_fin)
    parts.append(right_fin)
    parts.append(flame)
    return parts


def create_meteors(canvas, count):
    """สร้างอุกกาบาตหลายลูก แต่ละลูกมีตำแหน่งและความเร็วสุ่มต่างกัน

    Args:
        canvas: หน้าต่าง canvas
        count: จำนวนอุกกาบาตที่จะสร้าง

    Returns:
        ลิสต์ของ tuple (meteor, speed_x, speed_y) สำหรับแต่ละลูก
    """
    meteors = []
    for i in range(count):
        x = random.randint(-CANVAS_WIDTH, CANVAS_WIDTH // 2)
        y = random.randint(METEOR_SPAWN_Y_MIN, CANVAS_HEIGHT // 2)
        speed_x = random.randint(METEOR_MIN_SPEED_X, METEOR_MAX_SPEED_X)
        speed_y = random.randint(METEOR_MIN_SPEED_Y, METEOR_MAX_SPEED_Y)
        meteor = draw_meteor(canvas, x, y)
        meteor_data = (meteor, speed_x, speed_y)
        meteors.append(meteor_data)
    return meteors


def create_ufos(canvas, count):
    """สร้าง UFO หลายลำที่ระดับความสูงต่างกัน

    Args:
        canvas: หน้าต่าง canvas
        count: จำนวน UFO ที่จะสร้าง

    Returns:
        ลิสต์ของ tuple (body, dome, y_home) สำหรับ UFO แต่ละลำ
    """
    ufos = []
    for i in range(count):
        y_home = UFO_FIRST_Y + i * UFO_VERTICAL_GAP
        start_x = UFO_RESET_X - i * UFO_HORIZONTAL_GAP
        body, dome = draw_ufo(canvas, start_x, y_home)
        ufo_data = (body, dome, y_home)
        ufos.append(ufo_data)
    return ufos


def animate_meteors(canvas, meteors):
    """ขยับอุกกาบาตทุกลูกตามความเร็วของแต่ละลูก และรีเซ็ตเมื่อหลุดออกจากจอ

    Args:
        canvas: หน้าต่าง canvas
        meteors: ลิสต์ของ tuple (meteor, speed_x, speed_y)
    """
    for meteor_data in meteors:
        meteor = meteor_data[0]
        speed_x = meteor_data[1]
        speed_y = meteor_data[2]
        canvas.move(meteor, speed_x, speed_y)
        current_x = canvas.get_left_x(meteor)
        current_y = canvas.get_top_y(meteor)
        if current_x > CANVAS_WIDTH or current_y > CANVAS_HEIGHT:
            new_y = random.randint(METEOR_SPAWN_Y_MIN, CANVAS_HEIGHT // 2)
            canvas.move_to(meteor, -METEOR_SIZE, new_y)


def animate_ufos(canvas, ufos):
    """ขยับ UFO ทุกลำไปทางขวา และรีเซ็ตเมื่อหลุดออกจอ

    Args:
        canvas: หน้าต่าง canvas
        ufos: ลิสต์ของ tuple (body, dome, y_home)
    """
    for ufo_data in ufos:
        body = ufo_data[0]
        dome = ufo_data[1]
        y_home = ufo_data[2]
        canvas.move(body, UFO_SPEED, 0)
        canvas.move(dome, UFO_SPEED, 0)
        if canvas.get_left_x(body) > CANVAS_WIDTH:
            canvas.move_to(body, UFO_RESET_X, y_home)
            canvas.move_to(dome, UFO_RESET_X + UFO_DOME_RESET_OFFSET_X,
                           y_home - UFO_DOME_OFFSET_Y)


def animate_rockets(canvas, rockets):
    """ขยับจรวดทุกอันขึ้นด้านบน และลบจรวดที่หลุดออกจอแล้ว

    Args:
        canvas: หน้าต่าง canvas
        rockets: ลิสต์ของลิสต์ชิ้นส่วนจรวด (จะถูกแก้ไขตรงๆ)
    """
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
