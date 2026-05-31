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

LARGEUR, HAUTEUR = get_work_area()
scale_x = LARGEUR / 1600
scale_y = HAUTEUR / 900

faits_espace = [
    "Il y a plus d'étoiles dans l'univers que de grains de sable sur toutes les plages de la Terre.",
    "Une journée sur Vénus dure plus longtemps qu'une année sur Vénus.",
    "L'empreinte de pas laissée par les astronautes sur la Lune restera visible pendant des millions d'années, car il n'y a pas de vent pour l'effacer.",
    "Jupiter a 79 lunes connues, dont certaines sont plus petites que Pluton.",
    "La Grande Tache Rouge de Jupiter est une tempête qui fait rage depuis au moins 350 ans.",
    "Le soleil représente 99,86 % de la masse totale du système solaire.",
    "Un jour sur Mercure dure environ 59 jours terrestres, mais une année seulement 88 jours.",
    "Saturne n'est pas la seule planète à avoir des anneaux : Jupiter, Uranus et Neptune en ont aussi, mais moins visibles.",
    "La lumière du soleil met environ 8 minutes et 20 secondes pour atteindre la Terre.",
    "L'univers observable contient environ 2 000 milliards de galaxies.",
    "L'étoile la plus proche de nous (après le Soleil) est Proxima du Centaure, à 4,24 années-lumière.",
    "Un trou noir peut être créé par l'effondrement d'une étoile massive.",
    "Mars abrite le plus haut volcan du système solaire : Olympus Mons, haut de 21 km (2,5 fois l'Everest).",
    "La ceinture d'astéroïdes se situe entre Mars et Jupiter.",
    "Pluton a été reclassée comme planète naine en 2006 par l'Union Astronomique Internationale.",
    "Les jours sur Mars sont appelés 'sols' et durent 24 heures 39 minutes.",
    "Neptune a les vents les plus rapides du système solaire, jusqu'à 2 100 km/h.",
    "La sonde Voyager 1 a quitté le système solaire et se trouve maintenant dans l'espace interstellaire.",
    "L'ISS (Station Spatiale Internationale) fait le tour de la Terre toutes les 90 minutes.",
    "Une année-lumière correspond à la distance parcourue par la lumière en un an : environ 9 461 milliards de km.",
    "L'odeur de la poussière lunaire rappelle celle de la poudre à canon.",
    "Le cœur de la Terre est aussi chaud que la surface du Soleil (environ 5 500 °C).",
    "Les anneaux de Saturne sont composés à 99 % de glace d'eau.",
    "La Lune s'éloigne de la Terre d'environ 3,8 cm par an.",
    "Sur Vénus, le soleil se lève à l'ouest et se couche à l'est (rotation rétrograde).",
    "Il existe un lac de méthane liquide sur Titan, l'une des lunes de Saturne.",
    "L'étoile la plus massive connue, R136a1, a une masse 315 fois celle du Soleil.",
    "La Voie lactée et la galaxie d'Andromède entreront en collision dans environ 4,5 milliards d'années.",
    "Un pulsar peut tourner sur lui-même plusieurs centaines de fois par seconde.",
    "Le plus grand canyon du système solaire se trouve sur Mars : Valles Marineris, long de 4 000 km.",
    "La température à la surface de Mercure peut atteindre 430 °C le jour et -180 °C la nuit.",
    "La planète naine Cérès se trouve dans la ceinture d'astéroïdes et contient de l'eau douce sous sa surface.",
    "L'atmosphère de la Terre s'étend sur plus de 10 000 km, mais la moitié se trouve dans les 5 premiers km.",
    "La pression atmosphérique sur Vénus est 92 fois celle de la Terre (équivalent à être sous 900 m d'eau).",
    "Le champ magnétique de Jupiter est 20 000 fois plus puissant que celui de la Terre.",
    "Le télescope spatial Hubble a observé des galaxies âgées de plus de 13 milliards d'années.",
    "Une supernova peut briller plus fort que toute une galaxie pendant quelques jours.",
    "Les astronautes grandissent temporairement de quelques centimètres dans l'espace à cause de l'apesanteur.",
    "La planète Uranus a une inclinaison axiale de 98°, elle roule presque sur son côté.",
    "La lumière met environ 4 heures pour atteindre Neptune depuis le Soleil.",
    "Le Soleil perd environ 4 millions de tonnes de masse par seconde (par fusion nucléaire).",
    "La première fusée à avoir atteint l'espace était la V2 allemande en 1944.",
    "Le plus grand volcan de la Terre, le Mauna Kea, mesure plus de 10 000 m de hauteur depuis sa base sous-marine.",
    "Il existe des exoplanètes qui orbitent autour de deux étoiles (systèmes binaires).",
    "La ceinture de Kuiper contient des milliers d'objets glacés, dont Pluton.",
    "La mission Apollo 11 a rapporté 21,5 kg de roches lunaires.",
    "Les aurores boréales sont causées par les particules du vent solaire heurtant l'atmosphère terrestre.",
    "Europa, l'une des lunes de Jupiter, possède un océan d'eau liquide sous sa croûte glacée.",
    "Les trous noirs peuvent fusionner et créer des ondes gravitationnelles détectables sur Terre.",
    "Le satellite Encelade (Saturne) émet des geysers d'eau salée depuis son pôle sud.",
    "La galaxie d'Andromède se rapproche de la Voie lactée à 400 000 km/h.",
    "Une étoile à neutrons peut peser autant que le Soleil tout en ayant la taille d'une ville.",
    "L'espace n'est pas complètement vide : il contient quelques atomes par mètre cube."
]

fait_du_jour = random.choice(faits_espace)

pygame.init()
fenetre = pygame.display.set_mode((LARGEUR, HAUTEUR), pygame.NOFRAME)
pygame.display.set_caption("Simulateur 3D du système solaire")
icon = pygame.image.load('Logo.png')
pygame.display.set_icon(icon)

BLANC = (255, 255, 255)
ROUGE = (255, 0, 0)
ROUGE_FONCE = (120, 0, 0)
NOIR = (0, 0, 0)

taille_titre = max(60, int(100 * scale_y))
taille_credit = max(30, int(40 * scale_y))
taille_bouton = max(18, int(20 * scale_y))
taille_fait = max(16, int(18 * scale_y))

font_titre = pygame.font.SysFont("times", taille_titre, bold=True, italic=False)
font_credit = pygame.font.SysFont("times", taille_credit, bold=True, italic=False)
font_boutons = pygame.font.SysFont("times", taille_bouton, bold=True, italic=False)
font_fait = pygame.font.SysFont("times", taille_fait, bold=False, italic=False)

try:
    terre_pixel_art = pygame.image.load("Earth.png")
    croix_fermeture = pygame.image.load("croix.png")
except:
    terre_pixel_art = pygame.Surface((200, 200))
    terre_pixel_art.fill((0, 255, 0))
    croix_fermeture = pygame.Surface((30, 30))
    croix_fermeture.fill((255, 0, 0))

taille_terre = int(200 * min(scale_x, scale_y))
terre_pixel_art = pygame.transform.scale(terre_pixel_art, (taille_terre, taille_terre))

def pos(x, y):
    return int(x * scale_x), int(y * scale_y)

texte_titre = font_titre.render("Simulateur 3D du système solaire !", False, BLANC)
texte_credit = font_credit.render("DAOUADI Zine-Eddine Chahine.", False, BLANC)
texte_bouton_1 = font_boutons.render("Lancer le simulateur.", False, BLANC)
texte_bouton_2 = font_boutons.render("Informations.", False, BLANC)
texte_bouton_3 = font_boutons.render("Quitter.", False, BLANC)
lien_blog = font_boutons.render("https://blogmathsetscienceszineeddine.blogspot.com/", False, (0, 0, 255))

texte_info = [
    "Bienvenue sur mon simulateur 3D du système solaire.",
    "Je suis DAOUADI Zine-Eddine Chahine, un passionné",
    "des sciences physiques et mathématiques.",
    "Mon objectif, a été en concevant ce simulateur de fournir",
    "une visualisation concrète du système solaire.",
    "En effet bien que de nombreux simulateurs existent,",
    "j'ai souhaité en faire un, qui soit stable en performances.",
    "Le simulateur a été fait avec pygame et OpenGL.",
    "Le monde est fascinant, il suffit de regarder le ciel",
    "pour voir à quel point l'on importe peu à l'univers.",
    "C'est peut être ce qu'il y'a de plus fascinant...",
    "Regarder l'espace, ne pas reculer en se disant que",
    "à l'échelle de notre vie on peut marquer le monde,",
    "et peut-être espérer comprendre ce vaste infini.",
    "J'espère que mon simulateur vous plaira, et qu'il vous",
    "permettra en parallèle d'en apprendre plus sur l'espace.",
    "Je possède notamment un blog scientifique, où je traite",
    "davantage de sujets scientifiques variés.",
    "Vous pouvez le retrouver ici (cliquez) :",
    "Cordialement, DAOUADI Zine-Eddine Chahine."
]

liste_textes = []
for ligne in texte_info:
    liste_textes.append(font_boutons.render(ligne, False, BLANC))

nb_etoiles = max(100, int(150 * (LARGEUR * HAUTEUR) / (1600*900)))
etoiles = [(random.randint(0, LARGEUR), random.randint(0, HAUTEUR)) for _ in range(nb_etoiles)]

class Meteore:
    def __init__(self):
        self.x = random.randint(0, LARGEUR)
        self.y = random.randint(0, HAUTEUR)
        self.vx = random.uniform(0.5, 2.0) * scale_x
        self.vy = random.uniform(0.5, 2.0) * scale_y
        self.taille = random.randint(1, 3)

    def deplacer(self):
        self.x += self.vx
        self.y += self.vy
        if self.x > LARGEUR or self.y > HAUTEUR or self.x < 0 or self.y < 0:
            self.x = random.randint(0, LARGEUR)
            self.y = random.randint(0, HAUTEUR)
            self.vx = random.uniform(0.5, 2.0) * scale_x
            self.vy = random.uniform(0.5, 2.0) * scale_y

    def dessiner(self, surface):
        pygame.draw.rect(surface, BLANC, (int(self.x), int(self.y), self.taille, self.taille))

meteores = [Meteore() for _ in range(min(80, int(60 * scale_x)))]

def wraptext(texte, police, largeur_max):
    mots = texte.split(' ')
    lignes = []
    ligne_courante = ""
    for mot in mots:
        test_ligne = ligne_courante + (" " if ligne_courante else "") + mot
        if police.size(test_ligne)[0] <= largeur_max:
            ligne_courante = test_ligne
        else:
            if ligne_courante:
                lignes.append(ligne_courante)
            ligne_courante = mot
    if ligne_courante:
        lignes.append(ligne_courante)
    return lignes

cadre_x, cadre_y = pos(80, 300)
cadre_largeur = int(480 * scale_x)
cadre_hauteur = int(200 * scale_y)
cadre_interieur_x, cadre_interieur_y = pos(90, 310)
cadre_interieur_largeur = int(460 * scale_x)
cadre_interieur_hauteur = int(180 * scale_y)

largeur_texte = cadre_interieur_largeur - 20

en_tete = "Fait divers sur l'espace :"
lignes_en_tete = wraptext(en_tete, font_fait, largeur_texte)
lignes_fait = wraptext(fait_du_jour, font_fait, largeur_texte)

titre_x, titre_y = pos(70, 70)
credit_x, credit_y = pos(500, 200)
bouton_x, bouton_y1 = pos(650, 500)
bouton_y2 = pos(650, 600)[1]
bouton_y3 = pos(650, 700)[1]
bouton_largeur = int(300 * scale_x)
bouton_hauteur = int(50 * scale_y)

terre_x, terre_y = pos(800, 355)

conditionTexte2 = False
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    fenetre.fill(NOIR)

    for pos in etoiles:
        pygame.draw.circle(fenetre, BLANC, pos, 1)

    for m in meteores:
        m.deplacer()
        m.dessiner(fenetre)

    pygame.draw.rect(fenetre, NOIR, (bouton_x, bouton_y1, bouton_largeur, bouton_hauteur))
    pygame.draw.rect(fenetre, NOIR, (bouton_x, bouton_y2, bouton_largeur, bouton_hauteur))
    pygame.draw.rect(fenetre, NOIR, (bouton_x, bouton_y3, bouton_largeur, bouton_hauteur))

    fenetre.blit(texte_titre, (titre_x, titre_y))
    fenetre.blit(texte_credit, (credit_x, credit_y))
    fenetre.blit(texte_bouton_1, (bouton_x + (bouton_largeur - texte_bouton_1.get_width())//2, bouton_y1 + 15))
    fenetre.blit(texte_bouton_2, (bouton_x + (bouton_largeur - texte_bouton_2.get_width())//2, bouton_y2 + 15))
    fenetre.blit(texte_bouton_3, (bouton_x + (bouton_largeur - texte_bouton_3.get_width())//2, bouton_y3 + 15))

    pygame.draw.rect(fenetre, ROUGE, (bouton_x, bouton_y1, bouton_largeur, bouton_hauteur), 1)
    pygame.draw.rect(fenetre, ROUGE, (bouton_x, bouton_y2, bouton_largeur, bouton_hauteur), 1)
    pygame.draw.rect(fenetre, ROUGE, (bouton_x, bouton_y3, bouton_largeur, bouton_hauteur), 1)

    pygame.draw.rect(fenetre, NOIR, (cadre_x, cadre_y, cadre_largeur, cadre_hauteur))
    pygame.draw.rect(fenetre, ROUGE, (cadre_x, cadre_y, cadre_largeur, cadre_hauteur), 10)
    pygame.draw.rect(fenetre, ROUGE_FONCE, (cadre_interieur_x, cadre_interieur_y, cadre_interieur_largeur, cadre_interieur_hauteur), 10)

    y_start = cadre_interieur_y + 15
    for ligne in lignes_en_tete:
        surf = font_fait.render(ligne, False, (255, 200, 100))
        fenetre.blit(surf, (cadre_interieur_x + 10, y_start))
        y_start += font_fait.get_linesize()
    y_start += 5
    for ligne in lignes_fait:
        if y_start + font_fait.get_linesize() > cadre_interieur_y + cadre_interieur_hauteur - 10:
            break
        surf = font_fait.render(ligne, False, BLANC)
        fenetre.blit(surf, (cadre_interieur_x + 10, y_start))
        y_start += font_fait.get_linesize()

    fenetre.blit(terre_pixel_art, (terre_x - taille_terre//2, terre_y - taille_terre//2))

    souris_x, souris_y = pygame.mouse.get_pos()
    clic = pygame.mouse.get_pressed()[0]

    if (bouton_x <= souris_x <= bouton_x + bouton_largeur and
        bouton_y1 <= souris_y <= bouton_y1 + bouton_hauteur):
        pygame.draw.rect(fenetre, ROUGE, (bouton_x-10, bouton_y1-10, bouton_largeur+20, bouton_hauteur+20), 2)
        pygame.draw.rect(fenetre, ROUGE_FONCE, (bouton_x-7, bouton_y1-7, bouton_largeur+14, bouton_hauteur+14), 4)
        if clic:
            pygame.quit()
            subprocess.Popen([sys.executable, "Simulateur final système solaire.py"])
            sys.exit()

    if (bouton_x <= souris_x <= bouton_x + bouton_largeur and
        bouton_y2 <= souris_y <= bouton_y2 + bouton_hauteur):
        pygame.draw.rect(fenetre, ROUGE, (bouton_x-10, bouton_y2-10, bouton_largeur+20, bouton_hauteur+20), 2)
        pygame.draw.rect(fenetre, ROUGE_FONCE, (bouton_x-7, bouton_y2-7, bouton_largeur+14, bouton_hauteur+14), 4)
        if clic:
            conditionTexte2 = True

    if (bouton_x <= souris_x <= bouton_x + bouton_largeur and
        bouton_y3 <= souris_y <= bouton_y3 + bouton_hauteur):
        pygame.draw.rect(fenetre, ROUGE, (bouton_x-10, bouton_y3-10, bouton_largeur+20, bouton_hauteur+20), 2)
        pygame.draw.rect(fenetre, ROUGE_FONCE, (bouton_x-7, bouton_y3-7, bouton_largeur+14, bouton_hauteur+14), 4)
        if clic:
            running = False

    if conditionTexte2:
        info_largeur = int(580 * scale_x)
        info_hauteur = int(600 * scale_y)
        info_x = (LARGEUR - info_largeur) // 2
        info_y = (HAUTEUR - info_hauteur) // 2
        pygame.draw.rect(fenetre, NOIR, (info_x, info_y, info_largeur, info_hauteur))
        pygame.draw.rect(fenetre, ROUGE, (info_x, info_y, info_largeur, info_hauteur), 10)
        pygame.draw.rect(fenetre, ROUGE_FONCE, (info_x+10, info_y+10, info_largeur-20, info_hauteur-20), 10)

        croix_x = info_x + info_largeur - 40
        croix_y = info_y + 20
        pygame.draw.rect(fenetre, NOIR, (croix_x, croix_y, 30, 30))
        fenetre.blit(croix_fermeture, (croix_x, croix_y))

        y_offset = info_y + 50
        for ligne in liste_textes:
            fenetre.blit(ligne, (info_x + 50, y_offset))
            y_offset += font_boutons.get_linesize() + 2

        fenetre.blit(lien_blog, (info_x + 50, y_offset + 20))

        if (croix_x <= souris_x <= croix_x+30 and
            croix_y <= souris_y <= croix_y+30):
            pygame.draw.rect(fenetre, ROUGE, (croix_x, croix_y, 30, 30), 0)
            fenetre.blit(croix_fermeture, (croix_x, croix_y))
            if clic:
                conditionTexte2 = False

        lien_rect = pygame.Rect(info_x + 50, y_offset + 20, lien_blog.get_width(), lien_blog.get_height())
        if lien_rect.collidepoint(souris_x, souris_y) and clic:
            webbrowser.open("https://blogmathsetscienceszineeddine.blogspot.com/")

    pygame.display.flip()
    clock.tick(60)

pygame.quit()