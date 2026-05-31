import pygame
import random
import webbrowser
import subprocess
import sys
import ctypes
from pygame.locals import *

def get_work_area():
    try:
        SM_CXFULLSCREEN = 61
        SM_CYFULLSCREEN = 62
        user32 = ctypes.windll.user32
        width = user32.GetSystemMetrics(SM_CXFULLSCREEN)
        height = user32.GetSystemMetrics(SM_CYFULLSCREEN)
        return width, height
    except AttributeError:
        info = pygame.display.Info()
        return info.current_w, info.current_h - 40

WIDTH, HEIGHT = get_work_area()
scale_x = WIDTH / 1600
scale_y = HEIGHT / 900

space_facts = [
    "There are more stars in the universe than grains of sand on all Earth's beaches.",
    "A day on Venus lasts longer than a year on Venus.",
    "The footprints left by astronauts on the Moon will remain visible for millions of years, because there is no wind to erase them.",
    "Jupiter has 79 known moons, some of which are smaller than Pluto.",
    "Jupiter's Great Red Spot is a storm that has been raging for at least 350 years.",
    "The Sun makes up 99.86% of the total mass of the solar system.",
    "A day on Mercury lasts about 59 Earth days, but a year only 88 days.",
    "Saturn is not the only planet with rings: Jupiter, Uranus and Neptune also have them, but less visible.",
    "Sunlight takes about 8 minutes and 20 seconds to reach Earth.",
    "The observable universe contains about 2 trillion galaxies.",
    "The closest star to us (after the Sun) is Proxima Centauri, 4.24 light-years away.",
    "A black hole can be created by the collapse of a massive star.",
    "Mars is home to the tallest volcano in the solar system: Olympus Mons, 21 km high (2.5 times Everest).",
    "The asteroid belt lies between Mars and Jupiter.",
    "Pluto was reclassified as a dwarf planet in 2006 by the International Astronomical Union.",
    "Days on Mars are called 'sols' and last 24 hours 39 minutes.",
    "Neptune has the fastest winds in the solar system, up to 2,100 km/h.",
    "The Voyager 1 probe has left the solar system and is now in interstellar space.",
    "The ISS (International Space Station) circles Earth every 90 minutes.",
    "A light-year is the distance light travels in one year: about 9.461 trillion km.",
    "The smell of moon dust resembles gunpowder.",
    "Earth's core is as hot as the surface of the Sun (about 5,500 °C).",
    "Saturn's rings are 99% water ice.",
    "The Moon is moving away from Earth by about 3.8 cm per year.",
    "On Venus, the sun rises in the west and sets in the east (retrograde rotation).",
    "There is a lake of liquid methane on Titan, one of Saturn's moons.",
    "The most massive known star, R136a1, has a mass 315 times that of the Sun.",
    "The Milky Way and the Andromeda galaxy will collide in about 4.5 billion years.",
    "A pulsar can spin several hundred times per second.",
    "The largest canyon in the solar system is on Mars: Valles Marineris, 4,000 km long.",
    "The surface temperature on Mercury can reach 430 °C during the day and -180 °C at night.",
    "The dwarf planet Ceres lies in the asteroid belt and contains fresh water beneath its surface.",
    "Earth's atmosphere extends over 10,000 km, but half of it is in the first 5 km.",
    "The atmospheric pressure on Venus is 92 times that of Earth (equivalent to being under 900 m of water).",
    "Jupiter's magnetic field is 20,000 times stronger than Earth's.",
    "The Hubble Space Telescope has observed galaxies more than 13 billion years old.",
    "A supernova can shine brighter than an entire galaxy for a few days.",
    "Astronauts temporarily grow a few centimeters in space due to weightlessness.",
    "Uranus has an axial tilt of 98°, it rolls almost on its side.",
    "Light takes about 4 hours to reach Neptune from the Sun.",
    "The Sun loses about 4 million tons of mass per second (through nuclear fusion).",
    "The first rocket to reach space was the German V2 in 1944.",
    "The largest volcano on Earth, Mauna Kea, is over 10,000 m tall from its underwater base.",
    "There are exoplanets that orbit two stars (binary systems).",
    "The Kuiper belt contains thousands of icy objects, including Pluto.",
    "The Apollo 11 mission brought back 21.5 kg of Moon rocks.",
    "Auroras are caused by particles from the solar wind hitting Earth's atmosphere.",
    "Europa, one of Jupiter's moons, has a liquid water ocean beneath its icy crust.",
    "Black holes can merge and create gravitational waves detectable on Earth.",
    "Saturn's moon Enceladus emits salty water geysers from its south pole.",
    "The Andromeda galaxy is approaching the Milky Way at 400,000 km/h.",
    "A neutron star can weigh as much as the Sun while being the size of a city.",
    "Space is not completely empty: it contains a few atoms per cubic meter."
]

fact_of_the_day = random.choice(space_facts)

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)
pygame.display.set_caption("3D Solar System Simulator")
icon = pygame.image.load('Logo.png')
pygame.display.set_icon(icon)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (120, 0, 0)
BLACK = (0, 0, 0)

title_size = max(60, int(100 * scale_y))
credit_size = max(30, int(40 * scale_y))
button_size = max(18, int(20 * scale_y))
fact_size = max(16, int(18 * scale_y))

font_title = pygame.font.SysFont("times", title_size, bold=True, italic=False)
font_credit = pygame.font.SysFont("times", credit_size, bold=True, italic=False)
font_buttons = pygame.font.SysFont("times", button_size, bold=True, italic=False)
font_fact = pygame.font.SysFont("times", fact_size, bold=False, italic=False)

def wraptext(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines

try:
    earth_pixel_art = pygame.image.load("Earth.png")
    close_cross = pygame.image.load("croix.png")
except:
    earth_pixel_art = pygame.Surface((200, 200))
    earth_pixel_art.fill((0, 255, 0))
    close_cross = pygame.Surface((30, 30))
    close_cross.fill((255, 0, 0))

earth_size = int(200 * min(scale_x, scale_y))
earth_pixel_art = pygame.transform.scale(earth_pixel_art, (earth_size, earth_size))

def pos(x, y):
    return int(x * scale_x), int(y * scale_y)

title_text = font_title.render("3D Solar System Simulator!", False, WHITE)
title_x = (WIDTH - title_text.get_width()) // 2
title_y = int(70 * scale_y)

credit_text = font_credit.render("DAOUADI Zine-Eddine Chahine.", False, WHITE)
credit_x = (WIDTH - credit_text.get_width()) // 2
credit_y = int(200 * scale_y)

button_width = int(300 * scale_x)
button_height = int(50 * scale_y)
button_spacing = int(20 * scale_y)
buttons_total_height = 3 * button_height + 2 * button_spacing
buttons_start_y = int(500 * scale_y)

button_x = (WIDTH - button_width) // 2
button_y1 = buttons_start_y
button_y2 = button_y1 + button_height + button_spacing
button_y3 = button_y2 + button_height + button_spacing

button1_text = font_buttons.render("Launch simulator.", False, WHITE)
button2_text = font_buttons.render("Information.", False, WHITE)
button3_text = font_buttons.render("Quit.", False, WHITE)

panel_x, panel_y = pos(80, 300)
panel_width = int(480 * scale_x)
panel_height = int(200 * scale_y)
inner_panel_x, inner_panel_y = pos(90, 310)
inner_panel_width = int(460 * scale_x)
inner_panel_height = int(180 * scale_y)

text_max_width = inner_panel_width - 20
header_text = "Space fact:"
header_lines = wraptext(header_text, font_fact, text_max_width)
fact_lines = wraptext(fact_of_the_day, font_fact, text_max_width)

earth_x = WIDTH // 2
earth_y = int(355 * scale_y)

info_text_lines = [
    "Welcome to my 3D Solar System simulator.",
    "I am DAOUADI Zine-Eddine Chahine, a physics and",
    "mathematics enthusiast.",
    "My goal in creating this simulator was to provide",
    "a concrete visualization of the solar system.",
    "Although many simulators exist,",
    "I wanted to make one that has stable performance.",
    "The simulator was made with pygame and OpenGL.",
    "The world is fascinating, just look at the sky",
    "to see how little we matter to the universe.",
    "Perhaps that is the most fascinating thing...",
    "Looking at space, not stepping back, thinking that",
    "on the scale of our lives we can leave a mark on the world,",
    "and perhaps hope to understand this vast infinity.",
    "I hope you enjoy my simulator, and that it will",
    "also help you learn more about space.",
    "I also have a science blog, where I discuss",
    "various scientific topics in more depth.",
    "You can find it here (click):",
    "Sincerely, DAOUADI Zine-Eddine Chahine."
]

rendered_info = [font_buttons.render(line, False, WHITE) for line in info_text_lines]
blog_link = font_buttons.render("https://blogmathsetscienceszineeddine.blogspot.com/", False, (0, 0, 255))

num_stars = max(100, int(150 * (WIDTH * HEIGHT) / (1600*900)))
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(num_stars)]

class Meteor:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.vx = random.uniform(0.5, 2.0) * scale_x
        self.vy = random.uniform(0.5, 2.0) * scale_y
        self.size = random.randint(1, 3)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x > WIDTH or self.y > HEIGHT or self.x < 0 or self.y < 0:
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT)
            self.vx = random.uniform(0.5, 2.0) * scale_x
            self.vy = random.uniform(0.5, 2.0) * scale_y

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, (int(self.x), int(self.y), self.size, self.size))

meteors = [Meteor() for _ in range(min(80, int(60 * scale_x)))]

show_info = False
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    window.fill(BLACK)

    for star_pos in stars:
        pygame.draw.circle(window, WHITE, star_pos, 1)

    for m in meteors:
        m.move()
        m.draw(window)

    pygame.draw.rect(window, BLACK, (button_x, button_y1, button_width, button_height))
    pygame.draw.rect(window, BLACK, (button_x, button_y2, button_width, button_height))
    pygame.draw.rect(window, BLACK, (button_x, button_y3, button_width, button_height))

    window.blit(title_text, (title_x, title_y))
    window.blit(credit_text, (credit_x, credit_y))

    window.blit(button1_text, (button_x + (button_width - button1_text.get_width())//2, button_y1 + 15))
    window.blit(button2_text, (button_x + (button_width - button2_text.get_width())//2, button_y2 + 15))
    window.blit(button3_text, (button_x + (button_width - button3_text.get_width())//2, button_y3 + 15))

    pygame.draw.rect(window, RED, (button_x, button_y1, button_width, button_height), 1)
    pygame.draw.rect(window, RED, (button_x, button_y2, button_width, button_height), 1)
    pygame.draw.rect(window, RED, (button_x, button_y3, button_width, button_height), 1)

    pygame.draw.rect(window, BLACK, (panel_x, panel_y, panel_width, panel_height))
    pygame.draw.rect(window, RED, (panel_x, panel_y, panel_width, panel_height), 10)
    pygame.draw.rect(window, DARK_RED, (inner_panel_x, inner_panel_y, inner_panel_width, inner_panel_height), 10)

    y_start = inner_panel_y + 15
    for line in header_lines:
        surf = font_fact.render(line, False, (255, 200, 100))
        window.blit(surf, (inner_panel_x + 10, y_start))
        y_start += font_fact.get_linesize()
    y_start += 5
    for line in fact_lines:
        if y_start + font_fact.get_linesize() > inner_panel_y + inner_panel_height - 10:
            break
        surf = font_fact.render(line, False, WHITE)
        window.blit(surf, (inner_panel_x + 10, y_start))
        y_start += font_fact.get_linesize()

    window.blit(earth_pixel_art, (earth_x - earth_size//2, earth_y - earth_size//2))

    mouse_x, mouse_y = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    if (button_x <= mouse_x <= button_x + button_width and
        button_y1 <= mouse_y <= button_y1 + button_height):
        pygame.draw.rect(window, RED, (button_x-10, button_y1-10, button_width+20, button_height+20), 2)
        pygame.draw.rect(window, DARK_RED, (button_x-7, button_y1-7, button_width+14, button_height+14), 4)
        if click:
            pygame.quit()
            subprocess.Popen([sys.executable, "Simulateur final système solaire.py"])
            sys.exit()

    if (button_x <= mouse_x <= button_x + button_width and
        button_y2 <= mouse_y <= button_y2 + button_height):
        pygame.draw.rect(window, RED, (button_x-10, button_y2-10, button_width+20, button_height+20), 2)
        pygame.draw.rect(window, DARK_RED, (button_x-7, button_y2-7, button_width+14, button_height+14), 4)
        if click:
            show_info = True

    if (button_x <= mouse_x <= button_x + button_width and
        button_y3 <= mouse_y <= button_y3 + button_height):
        pygame.draw.rect(window, RED, (button_x-10, button_y3-10, button_width+20, button_height+20), 2)
        pygame.draw.rect(window, DARK_RED, (button_x-7, button_y3-7, button_width+14, button_height+14), 4)
        if click:
            running = False

    if show_info:
        info_width = int(580 * scale_x)
        info_height = int(600 * scale_y)
        info_x = (WIDTH - info_width) // 2
        info_y = (HEIGHT - info_height) // 2

        pygame.draw.rect(window, BLACK, (info_x, info_y, info_width, info_height))
        pygame.draw.rect(window, RED, (info_x, info_y, info_width, info_height), 10)
        pygame.draw.rect(window, DARK_RED, (info_x+10, info_y+10, info_width-20, info_height-20), 10)

        cross_x = info_x + info_width - 40
        cross_y = info_y + 20
        pygame.draw.rect(window, BLACK, (cross_x, cross_y, 30, 30))
        window.blit(close_cross, (cross_x, cross_y))

        y_offset = info_y + 50
        for line in rendered_info:
            window.blit(line, (info_x + 50, y_offset))
            y_offset += font_buttons.get_linesize() + 2

        link_x = info_x + (info_width - blog_link.get_width()) // 2
        window.blit(blog_link, (link_x, y_offset + 20))

        if (cross_x <= mouse_x <= cross_x+30 and
            cross_y <= mouse_y <= cross_y+30):
            pygame.draw.rect(window, RED, (cross_x, cross_y, 30, 30), 0)
            window.blit(close_cross, (cross_x, cross_y))
            if click:
                show_info = False

        link_rect = pygame.Rect(link_x, y_offset + 20, blog_link.get_width(), blog_link.get_height())
        if link_rect.collidepoint(mouse_x, mouse_y) and click:
            webbrowser.open("https://blogmathsetscienceszineeddine.blogspot.com/")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()