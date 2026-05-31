# Importing extensions.
import sys
import pygame
import os
import subprocess

# Importing important elements.
from pygame import *
pygame.init()

# --- Safe way to get the script directory ---
if getattr(sys, 'frozen', False):
    script_dir = os.path.dirname(sys.executable)
elif '__file__' in globals():
    script_dir = os.path.dirname(os.path.abspath(__file__))
else:
    script_dir = os.getcwd()

# --- Correct paths based on your actual folder structure ---
resources_dir = os.path.join(script_dir, "Data")                         # flags & logo
resources_dir2 = os.path.join(script_dir, "Solar System Simulator")     # French version
resources_dir3 = os.path.join(script_dir, "English Solar System Simulator")  # English version

# ----------------------------------------------------------------------
# Helper function to load an image with case‑insensitive fallback
# ----------------------------------------------------------------------
def load_image(folder, filename):
    """Try to load an image, trying common case variations.
    Returns a pygame.Surface. If not found, prints error and returns a magenta placeholder."""
    base, ext = os.path.splitext(filename)
    candidates = set([
        filename,
        filename.lower(),
        filename.upper(),
        filename.capitalize(),
        base.lower() + ext,
        base.upper() + ext,
        base + ext.lower(),
        base + ext.upper()
    ])
    for cand in candidates:
        path = os.path.join(folder, cand)
        if os.path.isfile(path):
            return pygame.image.load(path)
    
    print(f"ERROR: Could not find '{filename}' in '{folder}'")
    if os.path.exists(folder):
        print("Contents of that folder:")
        for item in os.listdir(folder):
            print(f"  - {item}")
    else:
        print(f"Folder does not exist: {folder}")
    error_surf = pygame.Surface((100, 100))
    error_surf.fill((255, 0, 255))
    return error_surf

# ----------------------------------------------------------------------
# Load images (will not crash even if missing)
# ----------------------------------------------------------------------
Logo = load_image(resources_dir, "Logo.png")
French_Flag = load_image(resources_dir, "French flag.png")
UK_flag = load_image(resources_dir, "UK flag.png")

# ----------------------------------------------------------------------
# Load font with fallback
# ----------------------------------------------------------------------
font_path = os.path.join(script_dir, "3666-font.otf")
if not os.path.isfile(font_path):
    font_path = os.path.join(script_dir, "3666-font", "3666-font.otf")
try:
    font = pygame.font.Font(font_path, 32)
except:
    print("Warning: Custom font not found, using default font.")
    font = pygame.font.Font(None, 32)

text = font.render('Langue/Language :', True, (255, 255, 255), 1)
choix_1 = font.render('Français.', True, (255, 255, 255), 1)
choix_2 = font.render('English.', True, (255, 255, 255), 1)
bouton_gauche = 0   # 0 = French (left), 1 = English (right)

# --- Create the display window FIRST (so convert_alpha has a display mode) ---
screen = pygame.display.set_mode([700, 600])

# --- Now scale and prepare the logo for the taskbar icon ---
max_icon_size = 64
if Logo.get_width() > max_icon_size or Logo.get_height() > max_icon_size:
    ratio = min(max_icon_size / Logo.get_width(), max_icon_size / Logo.get_height())
    new_size = (int(Logo.get_width() * ratio), int(Logo.get_height() * ratio))
    Logo = pygame.transform.smoothscale(Logo, new_size)

# convert_alpha is safe now because a display mode exists
Logo = Logo.convert_alpha()
pygame.display.set_icon(Logo)
pygame.display.set_caption('Solar system simulator.')

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        bouton_gauche = 1
    if keys[pygame.K_LEFT]:
        bouton_gauche = 0

    screen.fill((0, 0, 0))
    screen.blit(French_Flag, (30, 230))
    screen.blit(UK_flag, (350, 250))
    screen.blit(text, (225, 115))
    screen.blit(choix_1, (115, 445))
    screen.blit(choix_2, (455, 445))
    pygame.draw.rect(screen, (10, 10, 10), (10, 20, 680, 560), 15)
    pygame.draw.rect(screen, (20, 20, 20), (15, 25, 670, 555), 5)

    if bouton_gauche == 1:   # English selected
        pygame.draw.rect(screen, (255, 0, 0), (445, 435, 150, 55), 5)
        pygame.draw.rect(screen, (225, 0, 0), (445, 435, 150, 55), 4)
        pygame.draw.rect(screen, (185, 0, 0), (445, 435, 150, 55), 3)
        pygame.draw.rect(screen, (155, 0, 0), (445, 435, 150, 55), 2)
        pygame.draw.rect(screen, (125, 0, 0), (445, 435, 150, 55), 1)
    else:   # French selected
        pygame.draw.rect(screen, (255, 0, 0), (105, 435, 150, 55), 5)
        pygame.draw.rect(screen, (225, 0, 0), (105, 435, 150, 55), 4)
        pygame.draw.rect(screen, (185, 0, 0), (105, 435, 150, 55), 3)
        pygame.draw.rect(screen, (155, 0, 0), (105, 435, 150, 55), 2)
        pygame.draw.rect(screen, (125, 0, 0), (105, 435, 150, 55), 1)

    if keys[pygame.K_RETURN]:
        if bouton_gauche == 1:
            target_dir = resources_dir3
        else:
            target_dir = resources_dir2
        script_path = os.path.join(target_dir, "Ecran.py")
        if os.path.isfile(script_path):
            subprocess.Popen([sys.executable, script_path], cwd=target_dir)
        else:
            print(f"Error: {script_path} not found!")
            pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    pygame.display.flip()

pygame.quit()