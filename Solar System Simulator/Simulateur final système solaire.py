import pygame
from pygame.locals import *
from pygame import *
import math
from math import *
from OpenGL.GL import *
from OpenGL.GLU import *
import OpenGL.GL as gl
import numpy as np
import ctypes
import sys
import subprocess
import os
import json

try:
    subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "Données planètes.py")],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except Exception as e:
    print("Impossible de lancer le module d'information:", e)

def get_work_area():
    try:
        SM_CXFULLSCREEN = 61
        SM_CYFULLSCREEN = 62
        user32 = ctypes.windll.user32
        width = user32.GetSystemMetrics(SM_CXFULLSCREEN)
        height = user32.GetSystemMetrics(SM_CYFULLSCREEN)
        return width, height
    except AttributeError:
        print("Impossible de détecter la zone de travail sur ce système. Utilisation de la pleine résolution.")
        info = pygame.display.Info()
        return info.current_w, info.current_h

pygame.init()
work_w, work_h = get_work_area()
fenetre = pygame.display.set_mode((work_w, work_h), DOUBLEBUF | OPENGL | NOFRAME)
pygame.display.set_caption("Système solaire")
icon = pygame.image.load('Logo.png')
pygame.display.set_icon(icon)

glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_NORMALIZE)
glShadeModel(GL_SMOOTH)
glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
glEnable(GL_COLOR_MATERIAL)
glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
glDepthFunc(GL_LEQUAL)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, work_w / work_h, 0.1, 200.0)
glMatrixMode(GL_MODELVIEW)

quad = gluNewQuadric()
gluQuadricTexture(quad, GL_TRUE)
gluQuadricNormals(quad, GLU_SMOOTH)

glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)
glLightfv(GL_LIGHT0, GL_AMBIENT,  (0.12, 0.12, 0.12, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE,  (2.8,  2.4,  1.9,  1.0))
glLightfv(GL_LIGHT0, GL_SPECULAR, (2.4,  2.2,  1.8,  1.0))
glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION,  0.85)
glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION,    0.012)
glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.00035)
glMaterialfv(GL_FRONT, GL_AMBIENT,  (1.0, 1.0, 1.0, 1.0))
glMaterialfv(GL_FRONT, GL_DIFFUSE,  (1.0, 1.0, 1.0, 1.0))
glMaterialfv(GL_FRONT, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
glMaterialf (GL_FRONT, GL_SHININESS, 80.0)
glMaterialfv(GL_FRONT, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))

def création_texture(source):
    image = pygame.image.load(source)
    if source.lower().endswith(".png"):
        image = image.convert_alpha()
        image_data = pygame.image.tostring(image, "RGBA", 1)
        format_source = GL_RGBA
    else:
        image = image.convert()
        image_data = pygame.image.tostring(image, "RGB", 1)
        format_source = GL_RGB
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexImage2D(
        GL_TEXTURE_2D, 0, format_source,
        image.get_width(), image.get_height(),
        0, format_source, GL_UNSIGNED_BYTE, image_data
    )
    return texture_id

texture_fond = création_texture("Space_Magnific_Kues1.jpg")

liste_textures = {
    0:  [création_texture("texture_espace.jpg")],
    1:  [création_texture("texture_terre__.jpg"),   0.6, -33, 1.4],
    2:  [création_texture("texture_lune__.jpg"),    0.2, -35, 1.4],
    3:  [création_texture("texture_mars__.jpg"),    0.6, -30, 1.2],
    4:  [création_texture("texture_jupiter__.jpg"), 1.4, -25, 1.0],
    5:  [création_texture("texture_saturne__.jpg"), 1.4, -18, 0.9],
    6:  [création_texture("texture_neptune__.jpg"), 1.0, -12, 0.7],
    7:  [création_texture("texture_uranus__.jpg"),  1.0,  -6, 0.5],
    8:  [création_texture("texture_venus__.jpg"),   0.6, -40, 1.6],
    9:  [création_texture("texture_mercure__.jpg"), 0.3, -45, 2.0],
    10: [création_texture("texture_soleil__.jpg"),  2.0, -50],
    11: [création_texture("texture_anneaux__.jpg"), 2.0,   2],
    12: [création_texture("Texture_Trajectoire_Planete.png"), 2, 2],
    13: [création_texture("Texture_Nappe_2.png"),   0,   0],
}

rotation    = 0.0
angle       = 0.0
angle_lune  = 0.0

distances_Soleil_Planète = [
    liste_textures[10][2] - liste_textures[i][2]
    for i in range(1, 10)
]

DATA_FILE = os.path.join(os.path.dirname(__file__), "planet_data.json")

def write_shared_data():
    data = {
        "timestamp": pygame.time.get_ticks(),
        "soleil": {"x": 0, "y": -35, "z": 2},
        "planetes": []
    }
    noms = ["Mercure", "Vénus", "Terre", "Mars", "Jupiter", "Saturne", "Uranus", "Neptune"]
    for alpha in range(1, 10):
        if alpha == 2:
            continue
        if alpha == 1:
            nom = "Mercure"
        elif alpha == 3:
            nom = "Mars"
        elif alpha == 4:
            nom = "Jupiter"
        elif alpha == 5:
            nom = "Saturne"
        elif alpha == 6:
            nom = "Neptune"
        elif alpha == 7:
            nom = "Uranus"
        elif alpha == 8:
            nom = "Vénus"
        elif alpha == 9:
            nom = "Terre"
        else:
            continue
        dist = distances_Soleil_Planète[alpha - 1]
        a = angle * liste_textures[alpha][3]
        x = dist * math.cos(a)
        y = -35 + dist * math.sin(a)
        z = 2.0
        data["planetes"].append({
            "nom": nom,
            "alpha": alpha,
            "x": x,
            "y": y,
            "z": z,
            "angle_rad": a,
            "angle_deg": math.degrees(a),
            "distance_sim": dist,
            "rayon_visuel": liste_textures[alpha][1]
        })
    dist_terre = distances_Soleil_Planète[0]
    terre_angle = angle * liste_textures[1][3]
    lune_x = 1 * math.cos(angle_lune) + dist_terre * math.cos(terre_angle)
    lune_y = 1 * math.sin(angle_lune) + (-35 + dist_terre * math.sin(terre_angle))
    data["planetes"].append({
        "nom": "Lune",
        "alpha": 2,
        "x": lune_x,
        "y": lune_y,
        "z": 2.0,
        "angle_rad": angle_lune,
        "angle_deg": math.degrees(angle_lune),
        "distance_sim": 1.0,
        "rayon_visuel": liste_textures[2][1]
    })
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        pass

def appliquer_materiau_planete(alpha):
    specs = {
        1:  ((0.25, 0.25, 0.28, 1.0), 18.0),
        2:  ((0.20, 0.20, 0.20, 1.0),  8.0),
        3:  ((0.15, 0.15, 0.15, 1.0),  6.0),
        4:  ((0.45, 0.45, 0.45, 1.0), 35.0),
        5:  ((0.50, 0.50, 0.50, 1.0), 45.0),
        6:  ((0.20, 0.20, 0.22, 1.0), 18.0),
        7:  ((0.18, 0.20, 0.22, 1.0), 16.0),
        8:  ((0.35, 0.35, 0.32, 1.0), 22.0),
        9:  ((0.22, 0.20, 0.18, 1.0), 10.0),
        10: ((1.0,  1.0,  1.0,  1.0), 80.0),
    }
    specular, shininess = specs.get(alpha, ((0.3, 0.3, 0.3, 1.0), 20.0))
    glMaterialfv(GL_FRONT, GL_AMBIENT,   (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_DIFFUSE,   (1.0, 1.0, 1.0, 1.0))
    glMaterialfv(GL_FRONT, GL_SPECULAR,  specular)
    glMaterialf (GL_FRONT, GL_SHININESS, shininess)

Tenseurs_Riemann = [1.00, 0.08, 0.55, 9.00, 5.70, 1.80, 1.65, 0.85, 0.05, 24.00]
SIGMA_NAPPE = {1:5.5, 2:2.2, 3:4.2, 4:12.0, 5:10.0, 6:7.0, 7:6.6, 8:5.0, 9:3.0, 10:18.0}

def arriere_plan():
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, work_w, 0, work_h)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture_fond)
    glColor4f(1.0, 1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(0,    0)
    glTexCoord2f(1, 0); glVertex2f(work_w, 0)
    glTexCoord2f(1, 1); glVertex2f(work_w, work_h)
    glTexCoord2f(0, 1); glVertex2f(0,    work_h)
    glEnd()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def halo_soleil():
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glDepthMask(GL_FALSE)
    glPushMatrix()
    glTranslatef(0, -35, 2)
    for r, a in [(2.8, 0.18), (3.4, 0.12), (4.2, 0.08), (5.5, 0.05)]:
        glColor4f(1.0, 0.75, 0.25, a)
        gluSphere(quad, r, 18, 18)
    glPopMatrix()
    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)
    glColor4f(1.0, 1.0, 1.0, 1.0)

def trajectoires(numéro_planète):
    glPushMatrix()
    glTranslatef(0, -35, 2)
    glRotatef(1, 0, 0, 1)
    glDisable(GL_LIGHTING)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, liste_textures[12][0])
    anneau = gluNewQuadric()
    gluQuadricTexture(anneau, GL_TRUE)
    gluQuadricNormals(anneau, GLU_SMOOTH)
    gluDisk(anneau,
            abs(distances_Soleil_Planète[numéro_planète - 1]) - 0.05,
            abs(distances_Soleil_Planète[numéro_planète - 1]) + 0.05,
            64, 64)
    gluDeleteQuadric(anneau)
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)
    glPopMatrix()

def synthèse_planète(alpha, angle):
    appliquer_materiau_planete(alpha)
    glPushMatrix()
    dist = distances_Soleil_Planète[alpha - 1]
    a = angle * liste_textures[alpha][3]
    glTranslatef(dist * math.cos(a), -35 + dist * math.sin(a), 2)
    glRotatef(-rotation, 0, 0, 1)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, liste_textures[alpha][0])
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glColor4f(1.0, 1.0, 1.0, 1.0)
    gluSphere(quad, liste_textures[alpha][1], 24, 24)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def synthèse_lune(angle_lune):
    appliquer_materiau_planete(2)
    glPushMatrix()
    dist = distances_Soleil_Planète[0]
    glTranslatef(
        1 * math.cos(angle_lune) + dist * math.cos(angle * liste_textures[1][3]),
        1 * math.sin(angle_lune) + (-35 + dist * math.sin(angle * liste_textures[1][3])),
        2
    )
    glRotatef(-rotation, 0, 0, 1)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, liste_textures[2][0])
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glColor4f(1.0, 1.0, 1.0, 1.0)
    gluSphere(quad, liste_textures[2][1], 18, 18)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

def dessiner_soleil():
    glMaterialfv(GL_FRONT, GL_EMISSION, (1.0, 0.75, 0.25, 1.0))
    appliquer_materiau_planete(10)
    glPushMatrix()
    glTranslatef(0, -35, 2)
    glRotatef(-rotation, 0, 0, 1)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, liste_textures[10][0])
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glColor4f(1.0, 1.0, 1.0, 1.0)
    gluSphere(quad, liste_textures[10][1], 32, 32)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    glMaterialfv(GL_FRONT, GL_EMISSION, (0.0, 0.0, 0.0, 1.0))

NAPPE_RES          = 96
NAPPE_UPDATE_EVERY = 24
NAPPE_Z_BASE       = 5.0
NAPPE_Z_MIN        = -80.0
NAPPE_Z_MAX        = 30.0

nappe_x = np.linspace(-100.0, 100.0, NAPPE_RES + 1, dtype=np.float32)
nappe_y = np.linspace(-100.0, 100.0, NAPPE_RES + 1, dtype=np.float32)
NAPPE_XMESH, NAPPE_YMESH = np.meshgrid(nappe_x, nappe_y)
_N = NAPPE_RES + 1

_STRIDE   = 8
_n_verts  = _N * _N
_vbo_data = np.zeros((_n_verts, _STRIDE), dtype=np.float32)

for j in range(_N):
    for i in range(_N):
        idx = j * _N + i
        _vbo_data[idx, 0] = nappe_x[i]
        _vbo_data[idx, 1] = nappe_y[j]
        _vbo_data[idx, 2] = NAPPE_Z_BASE
        _vbo_data[idx, 5] = 1.0
        _vbo_data[idx, 6] = i / NAPPE_RES
        _vbo_data[idx, 7] = j / NAPPE_RES

_indices = []
for j in range(NAPPE_RES):
    for i in range(_N):
        _indices.append(j * _N + i)
        _indices.append((j + 1) * _N + i)
    if j < NAPPE_RES - 1:
        _indices.append((j + 1) * _N + NAPPE_RES)
        _indices.append((j + 1) * _N)
_indices_np = np.array(_indices, dtype=np.uint32)

_vbo_id = glGenBuffers(1)
_ibo_id = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, _vbo_id)
glBufferData(GL_ARRAY_BUFFER, _vbo_data.nbytes, _vbo_data, GL_DYNAMIC_DRAW)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, _ibo_id)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, _indices_np.nbytes, _indices_np, GL_STATIC_DRAW)
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

frame_count = 0

def rebuild_nappe():
    global _vbo_data
    softening = 0.8
    temps = pygame.time.get_ticks() * 0.001
    Z = np.full((_N, _N), NAPPE_Z_BASE, dtype=np.float32)
    dists    = np.array([distances_Soleil_Planète[p - 1] for p in range(1, 10)], dtype=np.float32)
    angles_p = np.array([angle * liste_textures[p][3] for p in range(1, 10)], dtype=np.float32)
    x_ps     = dists * np.cos(angles_p)
    y_ps     = -35.0 + dists * np.sin(angles_p)
    As       = np.array(Tenseurs_Riemann[:9], dtype=np.float32)
    sigmas   = np.array([SIGMA_NAPPE[p] for p in range(1, 10)], dtype=np.float32)
    for k in range(9):
        dx = NAPPE_XMESH - x_ps[k]
        dy = NAPPE_YMESH - y_ps[k]
        d2 = dx*dx + dy*dy
        r  = np.sqrt(d2 + softening*softening)
        s2 = sigmas[k]*sigmas[k]
        base = As[k] * (1.15/(r+1.0) + 0.22*np.exp(-d2/(2.0*s2)) + 0.06*np.exp(-d2/(2.0*(sigmas[k]*0.35)**2)))
        ripple = 0.018 * np.sin(0.34*r - 2.2*temps) / (1.0 + 0.03*r)
        Z += base + ripple
    A_sol   = float(Tenseurs_Riemann[9])
    sig_sol = float(SIGMA_NAPPE[10])
    dx = NAPPE_XMESH
    dy = NAPPE_YMESH - (-35.0)
    d2 = dx*dx + dy*dy
    r  = np.sqrt(d2 + softening*softening)
    Z += A_sol * (1.35/(r+1.0) + 0.30*np.exp(-d2/(2.0*sig_sol*sig_sol)) + 0.10*np.exp(-d2/(2.0*(sig_sol*0.30)**2)))
    Z += 0.025 * np.sin(0.40*r - 2.8*temps) / (1.0 + 0.02*r)
    Z = np.clip(Z, NAPPE_Z_MIN, NAPPE_Z_MAX - 0.1).astype(np.float32)
    step_x = float(nappe_x[1] - nappe_x[0])
    step_y = float(nappe_y[1] - nappe_y[0])
    dzdy, dzdx = np.gradient(Z, step_y, step_x, edge_order=2)
    NX = (-dzdx).astype(np.float32)
    NY = (-dzdy).astype(np.float32)
    NZ = np.ones_like(Z, dtype=np.float32)
    norm = np.sqrt(NX*NX + NY*NY + NZ*NZ)
    norm[norm == 0] = 1.0
    NX /= norm; NY /= norm; NZ /= norm
    _vbo_data[:, 2] = Z.ravel()
    _vbo_data[:, 3] = NX.ravel()
    _vbo_data[:, 4] = NY.ravel()
    _vbo_data[:, 5] = NZ.ravel()
    glBindBuffer(GL_ARRAY_BUFFER, _vbo_id)
    glBufferSubData(GL_ARRAY_BUFFER, 0, _vbo_data.nbytes, _vbo_data)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

def nappe():
    t = pygame.time.get_ticks() * 0.00003
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, liste_textures[13][0])
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 1.0, 1.0, 0.86)
    glMatrixMode(GL_TEXTURE)
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(t*0.20, t*0.06, 0.0)
    glRotatef(math.sin(t*0.9)*2.0, 0, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    stride = _STRIDE * _vbo_data.itemsize
    glBindBuffer(GL_ARRAY_BUFFER, _vbo_id)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, _ibo_id)
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_TEXTURE_COORD_ARRAY)
    glVertexPointer  (3, GL_FLOAT, stride, ctypes.c_void_p(0))
    glNormalPointer  (   GL_FLOAT, stride, ctypes.c_void_p(3*4))
    glTexCoordPointer(2, GL_FLOAT, stride, ctypes.c_void_p(6*4))
    glDrawElements(GL_TRIANGLE_STRIP, len(_indices_np), GL_UNSIGNED_INT, None)
    glDisableClientState(GL_VERTEX_ARRAY)
    glDisableClientState(GL_NORMAL_ARRAY)
    glDisableClientState(GL_TEXTURE_COORD_ARRAY)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    glMatrixMode(GL_TEXTURE)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glDisable(GL_TEXTURE_2D)
    glDisable(GL_BLEND)

SOLEIL_X = 0
SOLEIL_Y = -35
SOLEIL_Z = 2
PLAN_ORBITE_Z = 2
theta         = -np.pi / 2
rayon_cam     = 50
hauteur_cam   = -10
mode_camera   = 0
planete_suivie = 1

rebuild_nappe()

fin = 0
clock = pygame.time.Clock()

while fin == 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fin = 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_v:
                if mode_camera == 0:
                    mode_camera = 1
                elif mode_camera == 1:
                    mode_camera = 0
                elif mode_camera == 2:
                    mode_camera = 0
            if mode_camera == 1:
                if event.key == pygame.K_LEFT:
                    mode_camera = 2
                    planete_suivie = 9
                elif event.key == pygame.K_RIGHT:
                    mode_camera = 2
                    planete_suivie = 1
            elif mode_camera == 2:
                if event.key == pygame.K_LEFT:
                    planete_suivie = max(1, planete_suivie - 1)
                elif event.key == pygame.K_RIGHT:
                    planete_suivie = min(9, planete_suivie + 1)

    glClearColor(0, 0, 0, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    arriere_plan()

    rotation   += 0.5
    angle      += 0.005
    angle_lune += 0.005
    frame_count += 1

    if frame_count % 5 == 0:
        write_shared_data()

    if frame_count >= NAPPE_UPDATE_EVERY:
        rebuild_nappe()
        frame_count = 0

    if mode_camera == 0:
        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT]:
            theta += 0.02
        if touches[pygame.K_RIGHT]:
            theta -= 0.02
        cam_x = SOLEIL_X + rayon_cam * math.cos(theta)
        cam_y = SOLEIL_Y + rayon_cam * math.sin(theta)
        cam_z = hauteur_cam
        look_x, look_y, look_z = SOLEIL_X, SOLEIL_Y, SOLEIL_Z
        up = (0, 0, 1) if cam_z > look_z else (0, 0, -1)
    elif mode_camera == 1:
        cam_x = SOLEIL_X
        cam_y = SOLEIL_Y
        cam_z = hauteur_cam - 70
        look_x, look_y, look_z = SOLEIL_X, SOLEIL_Y, PLAN_ORBITE_Z
        up = (0, 1, 0)
    else:
        alpha = planete_suivie
        if alpha == 2:
            x = (1 * math.cos(angle_lune) + distances_Soleil_Planète[0] * math.cos(angle * liste_textures[1][3]))
            y = (1 * math.sin(angle_lune) + (-35 + distances_Soleil_Planète[0] * math.sin(angle * liste_textures[1][3])))
            z = 2
        else:
            dist = distances_Soleil_Planète[alpha - 1]
            a = angle * liste_textures[alpha][3]
            x = dist * math.cos(a)
            y = -35 + dist * math.sin(a)
            z = 2
        vx = x - SOLEIL_X
        vy = y - SOLEIL_Y
        norme = math.sqrt(vx*vx + vy*vy)
        if norme > 0:
            vx /= norme
            vy /= norme
        distance_arriere = 2.5
        cam_x = x + vx * distance_arriere
        cam_y = y + vy * distance_arriere
        cam_z = z - 6.0
        look_x, look_y, look_z = x, y, z
        up = (0, -1, 0)

    glLoadIdentity()
    gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, look_z, *up)
    glLightfv(GL_LIGHT0, GL_POSITION, (SOLEIL_X, SOLEIL_Y, SOLEIL_Z, 1.0))

    nappe()

    for alpha in [1, 3, 4, 5, 6, 7, 8, 9]:
        trajectoires(alpha)
        synthèse_planète(alpha, angle)

    synthèse_lune(angle_lune)
    halo_soleil()
    dessiner_soleil()

    glPushMatrix()
    dist = distances_Soleil_Planète[4]
    a = angle * liste_textures[5][3]
    glTranslatef(dist * math.cos(a), -35 + dist * math.sin(a), 2)
    glRotatef(-rotation, 0, 0, 1)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, liste_textures[11][0])
    glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
    glDisable(GL_LIGHTING)
    anneau = gluNewQuadric()
    gluQuadricTexture(anneau, GL_TRUE)
    gluQuadricNormals(anneau, GLU_SMOOTH)
    gluDisk(anneau, liste_textures[11][1]*1.5, liste_textures[11][1]*2.5, 48, 1)
    gluDeleteQuadric(anneau)
    glEnable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()

    pygame.display.flip()
    clock.tick(60)

glDeleteBuffers(1, [_vbo_id])
glDeleteBuffers(1, [_ibo_id])
pygame.quit()