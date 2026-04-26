"""
File: my_scene.py
Group Members:
    1. Name Surname (Student ID)
    2. Name Surname (Student ID)
    3. Name Surname (Student ID)
"""

# นำเข้าโมดูล time สำหรับใช้ time.sleep() เพื่อหน่วงเวลาในแต่ละเฟรม
import time
# นำเข้าโมดูล random เพื่อสุ่มตำแหน่งดาว เนบิวลา และอุกกาบาต
import random
# นำเข้าคลาส Canvas จากไลบรารี graphics.py สำหรับวาดภาพ
from graphics import Canvas

# ===== ค่าคงที่ของ Canvas =====
CANVAS_WIDTH = 800              # ความกว้างของหน้าต่าง (พิกเซล)
CANVAS_HEIGHT = 600             # ความสูงของหน้าต่าง (พิกเซล)
CANVAS_TITLE = "Space Scene"    # ข้อความบนแถบชื่อหน้าต่าง
FRAME_DELAY = 1 / 30            # ระยะเวลาหน่วงต่อเฟรม → ประมาณ 30 เฟรมต่อวินาที

# ===== ค่าคงที่ของฉาก =====
NUM_STARS = 120                 # จำนวนดาวที่จะวาด
NUM_NEBULA_CLOUDS = 4           # จำนวนเนบิวลา (เมฆอวกาศ)
NUM_METEORS = 6                 # จำนวนอุกกาบาต
NUM_UFOS = 2                    # จำนวน UFO
STAR_MAX_SIZE = 3               # ขนาดดาวสูงสุด (เล็กกว่านี้ก็มี)
METEOR_SIZE = 14                # ขนาดของอุกกาบาต
METEOR_MIN_SPEED_X = 3          # ความเร็วแนวนอนขั้นต่ำของอุกกาบาต
METEOR_MAX_SPEED_X = 9          # ความเร็วแนวนอนขั้นสูงของอุกกาบาต
METEOR_MIN_SPEED_Y = 1          # ความเร็วแนวตั้งขั้นต่ำของอุกกาบาต
METEOR_MAX_SPEED_Y = 4          # ความเร็วแนวตั้งขั้นสูงของอุกกาบาต
UFO_SPEED = 2                   # ความเร็วของ UFO ในแนวนอน
ROCKET_BODY_WIDTH = 16          # ความกว้างตัวจรวด
ROCKET_BODY_HEIGHT = 36         # ความสูงตัวจรวด
ROCKET_SPEED = 7                # ความเร็วจรวดที่พุ่งขึ้น
BG_COLOR = "#05052a"            # สีพื้นหลังของอวกาศ (น้ำเงินดำเข้ม)
# รายการสีของเนบิวลา ใช้สลับกันให้ดูหลากหลาย
NEBULA_COLORS = ["#2a1052", "#102a52", "#52102a", "#1a3a5a"]


def main():
    """ฟังก์ชันหลัก: สร้าง canvas วาดฉาก และรันลูปแอนิเมชัน"""
    # สร้างหน้าต่าง canvas ตามขนาดและชื่อที่กำหนด
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, CANVAS_TITLE)

    # ----- วาดส่วนพื้นหลังของฉาก (วาดจากหลังไปหน้า) -----
    draw_background(canvas)                                     # พื้นหลังสีดำเข้ม
    draw_nebulae(canvas, NUM_NEBULA_CLOUDS)                     # เมฆอวกาศสีๆ
    draw_stars(canvas, NUM_STARS)                               # ดาวกระจายทั่วท้องฟ้า
    draw_moon(canvas, CANVAS_WIDTH - 170, 45, 95)               # ดวงจันทร์มุมขวาบน
    draw_planet(canvas, 80, 110, 80, "coral")                   # ดาวเสาร์สีส้ม (มีวงแหวน)
    draw_earth(canvas, 330, 50, 60)                             # ดาวโลก (สีน้ำเงินมีทวีปสีเขียว)

    # ----- สร้างวัตถุที่จะเคลื่อนไหว -----
    meteors = create_meteors(canvas, NUM_METEORS)   # ลิสต์ของอุกกาบาต 6 ลูก
    ufos = create_ufos(canvas, NUM_UFOS)            # ลิสต์ของ UFO 2 ลำ
    rockets = []                                    # ลิสต์ว่าง สำหรับเก็บจรวดที่ผู้ใช้ยิง

    # ----- ตั้งค่า event handler สำหรับการคลิกเมาส์ -----
    def on_mouse_pressed(x, y):
        """ฟังก์ชันที่จะถูกเรียกเมื่อผู้ใช้คลิกบน canvas → ยิงจรวดที่จุดคลิก"""
        # วาดจรวดใหม่ ณ ตำแหน่งที่คลิก แล้วเพิ่มเข้า list rockets เพื่อให้ลูปขยับ
        rockets.append(draw_rocket(canvas, x, y))

    # บอก canvas ว่าเมื่อมีการคลิกให้เรียกฟังก์ชัน on_mouse_pressed
    canvas.on_mouse_pressed = on_mouse_pressed

    # ----- ลูปแอนิเมชันหลัก (game loop) -----
    while True:
        animate_meteors(canvas, meteors)    # ขยับอุกกาบาตทุกลูก
        animate_ufos(canvas, ufos)          # ขยับ UFO ทุกลำ
        animate_rockets(canvas, rockets)    # ขยับจรวดที่ผู้ใช้ยิง
        canvas.update()                     # รีเฟรชหน้าจอให้เห็นการเคลื่อนไหว
        time.sleep(FRAME_DELAY)             # หน่วงเวลาเล็กน้อยก่อนเฟรมถัดไป


def draw_background(canvas):
    """วาดพื้นหลังอวกาศสีน้ำเงินดำเต็มหน้าจอ"""
    # ใช้สี่เหลี่ยมขนาดเท่า canvas เป็นพื้นหลัง
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT,
                            fill=BG_COLOR, outline=BG_COLOR)


def draw_nebulae(canvas, count):
    """วาดเมฆอวกาศ (เนบิวลา) สีๆ จางๆ เป็นจำนวนตามที่กำหนด

    Args:
        canvas: หน้าต่าง canvas ที่จะวาด
        count: จำนวนเนบิวลาที่จะวาด
    """
    # วนลูปสร้างเนบิวลาทีละก้อน
    for i in range(count):
        cx = random.randint(0, CANVAS_WIDTH)            # สุ่มตำแหน่ง x ของจุดศูนย์กลาง
        cy = random.randint(0, CANVAS_HEIGHT)           # สุ่มตำแหน่ง y ของจุดศูนย์กลาง
        size = random.randint(120, 220)                 # สุ่มขนาดของเมฆ
        color = NEBULA_COLORS[i % len(NEBULA_COLORS)]   # เลือกสีจาก list สลับกันไป
        # วาดเป็นวงกลมใหญ่ๆ โดยให้จุดกลางอยู่ที่ (cx, cy)
        canvas.create_oval(cx - size, cy - size, cx + size, cy + size,
                           fill=color, outline=color)


def draw_stars(canvas, count):
    """วาดดาวเล็กๆ กระจายทั่วท้องฟ้าด้วยลูป

    Args:
        canvas: หน้าต่าง canvas ที่จะวาด
        count: จำนวนดาวที่จะวาด
    """
    # วาดดาวทีละดวงด้วยตำแหน่งและขนาดสุ่ม
    for i in range(count):
        x = random.randint(0, CANVAS_WIDTH)         # สุ่มตำแหน่ง x ของดาว
        y = random.randint(0, CANVAS_HEIGHT)        # สุ่มตำแหน่ง y ของดาว
        size = random.randint(1, STAR_MAX_SIZE)     # สุ่มขนาดดาว (1 ถึง STAR_MAX_SIZE)
        # วาดดาวเป็นวงกลมเล็กๆ สีขาว
        canvas.create_oval(x, y, x + size, y + size, fill="white", outline="white")


def draw_moon(canvas, x, y, size):
    """วาดดวงจันทร์พร้อมหลุมอุกกาบาต 2 หลุม

    Args:
        canvas: หน้าต่าง canvas
        x: พิกัด x ของมุมบนซ้ายของดวงจันทร์
        y: พิกัด y ของมุมบนซ้ายของดวงจันทร์
        size: เส้นผ่านศูนย์กลางของดวงจันทร์
    """
    # วาดตัวดวงจันทร์เป็นวงกลมสีเหลือง
    canvas.create_oval(x, y, x + size, y + size, fill="#f5e642", outline="#f5e642")
    # คำนวณขนาดของหลุมจากขนาดดวงจันทร์ (1/6 ของขนาดดวงจันทร์)
    crater_size = size // 6
    # วาดหลุมที่ 1 (ค่อนไปทางซ้าย-ล่าง)
    canvas.create_oval(x + size // 4, y + size // 3,
                       x + size // 4 + crater_size, y + size // 3 + crater_size,
                       fill="#d4c830", outline="#d4c830")
    # วาดหลุมที่ 2 (ค่อนไปทางขวา-บน)
    canvas.create_oval(x + size // 2, y + size // 5,
                       x + size // 2 + crater_size, y + size // 5 + crater_size,
                       fill="#d4c830", outline="#d4c830")


def draw_planet(canvas, x, y, size, color):
    """วาดดาวเคราะห์พร้อมวงแหวน

    Args:
        canvas: หน้าต่าง canvas
        x: พิกัด x ของมุมบนซ้ายของตัวดาวเคราะห์
        y: พิกัด y ของมุมบนซ้ายของตัวดาวเคราะห์
        size: เส้นผ่านศูนย์กลางของดาวเคราะห์
        color: สีของดาวเคราะห์
    """
    # ระยะที่วงแหวนยื่นออกมาจากตัวดาว (1/3 ของขนาด)
    ring_pad = size // 3
    # วาดวงแหวนก่อน (เป็นวงรีบางๆ ไม่มีสี fill มีแต่เส้นขอบ)
    canvas.create_oval(x - ring_pad, y + size // 3,
                       x + size + ring_pad, y + size * 2 // 3,
                       fill="", outline="#cccccc", width=2)
    # วาดตัวดาวเคราะห์ทับวงแหวน เพื่อให้ดูเหมือนวงแหวนผ่านด้านหลัง
    canvas.create_oval(x, y, x + size, y + size, fill=color, outline=color)


def draw_earth(canvas, x, y, size):
    """วาดดาวโลก: ทรงกลมสีน้ำเงิน (มหาสมุทร) + ทวีปสีเขียว

    Args:
        canvas: หน้าต่าง canvas
        x: พิกัด x ของมุมบนซ้าย
        y: พิกัด y ของมุมบนซ้าย
        size: เส้นผ่านศูนย์กลางของดาวโลก
    """
    # วาดทรงกลมสีน้ำเงินเป็นมหาสมุทรก่อน
    canvas.create_oval(x, y, x + size, y + size, fill="#1e6fb8", outline="#0f4f8a")
    # วาดทวีปเป็นวงรีสีเขียวซ้อนบนพื้นน้ำเงิน 3 ก้อน (ตำแหน่งคำนวณจาก size)
    canvas.create_oval(x + size // 5, y + size // 4,
                       x + size // 2, y + size // 2,
                       fill="#2d8c3a", outline="#2d8c3a")     # ทวีปซ้ายบน
    canvas.create_oval(x + size // 2, y + size // 6,
                       x + size * 3 // 4, y + size // 3,
                       fill="#2d8c3a", outline="#2d8c3a")     # ทวีปขวาบน
    canvas.create_oval(x + size // 3, y + size * 3 // 5,
                       x + size * 2 // 3, y + size * 4 // 5,
                       fill="#2d8c3a", outline="#2d8c3a")     # ทวีปกลางล่าง


def draw_meteor(canvas, x, y):
    """วาดอุกกาบาต 1 ลูกแล้วคืนค่าวัตถุไปให้ใช้ในแอนิเมชัน

    Args:
        canvas: หน้าต่าง canvas
        x: พิกัด x เริ่มต้น
        y: พิกัด y เริ่มต้น

    Returns:
        วัตถุอุกกาบาต (oval object)
    """
    # วาดเป็นวงกลมสีขาวขนาด METEOR_SIZE และคืนค่ากลับ
    return canvas.create_oval(x, y, x + METEOR_SIZE, y + METEOR_SIZE,
                              fill="white", outline="lightyellow")


def draw_ufo(canvas, x, y):
    """วาด UFO 1 ลำ (ตัวเงิน + โดมฟ้าด้านบน) แล้วคืนค่าทั้งสองส่วน

    Args:
        canvas: หน้าต่าง canvas
        x: พิกัด x เริ่มต้นของตัว UFO
        y: พิกัด y เริ่มต้นของตัว UFO

    Returns:
        ทูเปิล (body, dome) - สองชิ้นส่วนของ UFO
    """
    # ตัว UFO เป็นวงรีแบนๆ สีเงิน
    body = canvas.create_oval(x, y, x + 60, y + 18, fill="silver", outline="gray")
    # โดมด้านบนเป็นวงรีฟ้าใส อยู่ตรงกลางและสูงกว่าตัว
    dome = canvas.create_oval(x + 15, y - 15, x + 45, y + 8,
                              fill="lightblue", outline="white")
    # คืนค่าทั้งสองชิ้นเพื่อให้ขยับพร้อมกันได้
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
    # คำนวณครึ่งของขนาดเพื่อให้วาดจากจุดกลาง
    half_w = ROCKET_BODY_WIDTH // 2
    half_h = ROCKET_BODY_HEIGHT // 2
    # ตัวจรวดสี่เหลี่ยมสีขาว
    body = canvas.create_rectangle(x - half_w, y - half_h, x + half_w, y + half_h, fill="white", outline="gray")
    # จมูกจรวดทรงวงรีสีแดง อยู่ด้านบนตัว
    nose = canvas.create_oval(x - half_w, y - half_h - 14, x + half_w, y - half_h + 6, fill="red", outline="darkred")
    # หน้าต่างวงกลมสีฟ้าตรงกลางตัวจรวด
    window = canvas.create_oval(x - 5, y - 6, x + 5, y + 4, fill="lightblue", outline="blue")
    # ครีบซ้ายสี่เหลี่ยมสีแดง อยู่มุมล่างซ้าย
    left_fin = canvas.create_rectangle(x - half_w - 6, y + half_h - 10, x - half_w, y + half_h, fill="red", outline="darkred")
    # ครีบขวาสี่เหลี่ยมสีแดง อยู่มุมล่างขวา
    right_fin = canvas.create_rectangle(x + half_w, y + half_h - 10, x + half_w + 6, y + half_h, fill="red", outline="darkred")
    # เปลวไฟวงรีสีส้ม อยู่ใต้ตัวจรวด
    flame = canvas.create_oval(x - 6, y + half_h, x + 6, y + half_h + 14, fill="orange", outline="yellow")
    # คืนค่าทุกชิ้นในรูปลิสต์ เพื่อให้ขยับและลบพร้อมกัน
    return [body, nose, window, left_fin, right_fin, flame]


def create_meteors(canvas, count):
    """สร้างอุกกาบาตหลายลูก แต่ละลูกมีตำแหน่งและความเร็วสุ่มต่างกัน

    Args:
        canvas: หน้าต่าง canvas
        count: จำนวนอุกกาบาตที่จะสร้าง

    Returns:
        ลิสต์ของ tuple (meteor, speed_x, speed_y) สำหรับแต่ละลูก
    """
    meteors = []  # ลิสต์ว่างไว้เก็บอุกกาบาต
    # สร้างอุกกาบาตทีละลูกในลูป
    for i in range(count):
        # สุ่มตำแหน่ง x จากนอกจอด้านซ้ายเข้ามาถึงกลางจอ (เพื่อให้ทยอยเข้ามา)
        x = random.randint(-CANVAS_WIDTH, CANVAS_WIDTH // 2)
        # สุ่มตำแหน่ง y จากเหนือจอเล็กน้อยจนถึงครึ่งบนของจอ
        y = random.randint(-50, CANVAS_HEIGHT // 2)
        # สุ่มความเร็วของแต่ละลูก → บางลูกช้า บางลูกเร็ว
        speed_x = random.randint(METEOR_MIN_SPEED_X, METEOR_MAX_SPEED_X)
        speed_y = random.randint(METEOR_MIN_SPEED_Y, METEOR_MAX_SPEED_Y)
        # วาดอุกกาบาตและเก็บพร้อมความเร็วของลูกนั้นเข้าลิสต์
        meteors.append((draw_meteor(canvas, x, y), speed_x, speed_y))
    return meteors


def create_ufos(canvas, count):
    """สร้าง UFO หลายลำที่ระดับความสูงต่างกัน

    Args:
        canvas: หน้าต่าง canvas
        count: จำนวน UFO ที่จะสร้าง

    Returns:
        ลิสต์ของ tuple (body, dome, y_home) สำหรับ UFO แต่ละลำ
    """
    ufos = []  # ลิสต์ว่างไว้เก็บ UFO
    for i in range(count):
        # ระดับความสูงของแต่ละลำ ห่างกันลำละ 180 พิกเซล
        y_home = 200 + i * 180
        # ตำแหน่ง x เริ่มต้น ห่างจากจอด้านซ้ายเพื่อให้ทยอยโผล่
        body, dome = draw_ufo(canvas, -60 - i * 250, y_home)
        # เก็บเป็น tuple พร้อม y_home เพื่อใช้ตอนรีเซ็ตตำแหน่ง
        ufos.append((body, dome, y_home))
    return ufos


def animate_meteors(canvas, meteors):
    """ขยับอุกกาบาตทุกลูกตามความเร็วของแต่ละลูก และรีเซ็ตเมื่อหลุดออกจากจอ

    Args:
        canvas: หน้าต่าง canvas
        meteors: ลิสต์ของ tuple (meteor, speed_x, speed_y)
    """
    # ขยับอุกกาบาตทีละลูก โดยใช้ความเร็วของแต่ละลูกเอง
    for meteor, speed_x, speed_y in meteors:
        # เลื่อนอุกกาบาตในแนวเฉียง (ขวา-ลง) ตามความเร็วของลูกนี้
        canvas.move(meteor, speed_x, speed_y)
        # ถ้าอุกกาบาตหลุดออกขอบขวาหรือขอบล่าง → รีเซ็ตกลับมาด้านซ้าย
        if canvas.get_left_x(meteor) > CANVAS_WIDTH or canvas.get_top_y(meteor) > CANVAS_HEIGHT:
            new_y = random.randint(-50, CANVAS_HEIGHT // 2)     # สุ่ม y ใหม่
            canvas.move_to(meteor, -METEOR_SIZE, new_y)         # ย้ายไปนอกจอด้านซ้าย


def animate_ufos(canvas, ufos):
    """ขยับ UFO ทุกลำไปทางขวา และรีเซ็ตเมื่อหลุดออกจอ

    Args:
        canvas: หน้าต่าง canvas
        ufos: ลิสต์ของ tuple (body, dome, y_home)
    """
    # ขยับ UFO ทีละลำ (ต้องขยับทั้งตัวและโดมพร้อมกัน)
    for body, dome, y_home in ufos:
        canvas.move(body, UFO_SPEED, 0)     # เลื่อนตัว UFO ไปขวา
        canvas.move(dome, UFO_SPEED, 0)     # เลื่อนโดมไปขวาให้พร้อมกัน
        # ถ้าหลุดขอบขวา → ย้ายกลับไปซ้ายเริ่มใหม่
        if canvas.get_left_x(body) > CANVAS_WIDTH:
            canvas.move_to(body, -60, y_home)           # รีเซ็ตตัว UFO
            canvas.move_to(dome, -45, y_home - 15)      # รีเซ็ตโดม (เลื่อนขวา 15 และอยู่สูงกว่าตัว)


def animate_rockets(canvas, rockets):
    """ขยับจรวดทุกอันขึ้นด้านบน และลบจรวดที่หลุดออกจอแล้ว

    Args:
        canvas: หน้าต่าง canvas
        rockets: ลิสต์ของลิสต์ชิ้นส่วนจรวด (จะถูกแก้ไขตรงๆ)
    """
    # ใช้ rockets[:] (สำเนา) เพื่อให้ลบ element ระหว่างวนลูปได้อย่างปลอดภัย
    for parts in rockets[:]:
        # ขยับทุกชิ้นส่วนของจรวดขึ้นพร้อมกัน
        for part in parts:
            canvas.move(part, 0, -ROCKET_SPEED)
        # ตรวจสอบว่าตัวจรวด (parts[0]) หลุดออกขอบบนหรือยัง
        if canvas.get_top_y(parts[0]) < -ROCKET_BODY_HEIGHT:
            # ถ้าหลุดแล้ว → ลบทุกชิ้นออกจาก canvas
            for part in parts:
                canvas.delete(part)
            # และเอาออกจาก list rockets เพื่อไม่ต้องขยับซ้ำ
            rockets.remove(parts)


# ---- Do not modify below this line ----
# บรรทัดนี้ตรวจว่าไฟล์ถูกรันโดยตรง (ไม่ใช่ถูก import) → เรียก main() เพื่อเริ่มโปรแกรม
if __name__ == "__main__":
    main()
