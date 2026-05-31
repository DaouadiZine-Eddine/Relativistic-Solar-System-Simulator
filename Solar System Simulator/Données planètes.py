import tkinter as tk
from tkinter import ttk
import json
import os
import math
from datetime import datetime
from PIL import Image, ImageTk

def riemann_reel(masse_kg, rayon_km):
    G = 6.67430e-11
    c = 299792458.0
    r_m = rayon_km * 1000.0
    if r_m == 0:
        return float('inf')
    R = (2 * G * masse_kg) / (c**2 * r_m**3)
    return R * 1e18

physical_data = {
    "Soleil":  {"masse_kg": 1.989e30, "rayon_km": 695700.0},
    "Mercure": {"masse_kg": 3.30e23,  "rayon_km": 2439.7},
    "Vénus":   {"masse_kg": 4.87e24,  "rayon_km": 6051.8},
    "Terre":   {"masse_kg": 5.97e24,  "rayon_km": 6371.0},
    "Mars":    {"masse_kg": 6.42e23,  "rayon_km": 3389.5},
    "Jupiter": {"masse_kg": 1.90e27,  "rayon_km": 69911.0},
    "Saturne": {"masse_kg": 5.68e26,  "rayon_km": 58232.0},
    "Uranus":  {"masse_kg": 8.68e25,  "rayon_km": 25362.0},
    "Neptune": {"masse_kg": 1.02e26,  "rayon_km": 24622.0},
    "Lune":    {"masse_kg": 7.35e22,  "rayon_km": 1737.4}
}

real_riemann = {name: riemann_reel(data["masse_kg"], data["rayon_km"]) for name, data in physical_data.items()}

extra_stats = {
    "Soleil":  {"Excentricité": 0.0,    "Inclinaison (°)": 0.0, "Albédo": 0.999, "Densité (g/cm³)": 1.41},
    "Mercure": {"Excentricité": 0.2056, "Inclinaison (°)": 7.0, "Albédo": 0.088, "Densité (g/cm³)": 5.43},
    "Vénus":   {"Excentricité": 0.0068, "Inclinaison (°)": 3.4, "Albédo": 0.65,  "Densité (g/cm³)": 5.24},
    "Terre":   {"Excentricité": 0.0167, "Inclinaison (°)": 0.0, "Albédo": 0.306, "Densité (g/cm³)": 5.51},
    "Mars":    {"Excentricité": 0.0934, "Inclinaison (°)": 1.9, "Albédo": 0.170, "Densité (g/cm³)": 3.93},
    "Jupiter": {"Excentricité": 0.0489, "Inclinaison (°)": 1.3, "Albédo": 0.52,  "Densité (g/cm³)": 1.33},
    "Saturne": {"Excentricité": 0.0565, "Inclinaison (°)": 2.5, "Albédo": 0.47,  "Densité (g/cm³)": 0.69},
    "Uranus":  {"Excentricité": 0.0457, "Inclinaison (°)": 0.8, "Albédo": 0.51,  "Densité (g/cm³)": 1.27},
    "Neptune": {"Excentricité": 0.0113, "Inclinaison (°)": 1.8, "Albédo": 0.41,  "Densité (g/cm³)": 1.64},
    "Lune":    {"Excentricité": 0.0549, "Inclinaison (°)": 5.1, "Albédo": 0.136, "Densité (g/cm³)": 3.34}
}

planet_data_static = {}
for name in physical_data.keys():
    if name == "Soleil":
        G = 6.67430e-11
        M = physical_data["Soleil"]["masse_kg"]
        R_m = physical_data["Soleil"]["rayon_km"] * 1000
        grav = (G * M) / (R_m**2)
        grav_str = f"{grav:.0f} m/s²"
    else:
        grav_str = f"{9.81 * (physical_data[name]['masse_kg']/5.97e24) / ((physical_data[name]['rayon_km']/6371.0)**2):.1f} m/s²"

    temps = {
        "Soleil":  "5 500 °C (surface)",
        "Mercure": "167 °C",
        "Vénus":   "462 °C",
        "Terre":   "15 °C",
        "Mars":    "-65 °C",
        "Jupiter": "-110 °C",
        "Saturne": "-140 °C",
        "Uranus":  "-195 °C",
        "Neptune": "-200 °C",
        "Lune":    "-20 °C (moyenne)"
    }
    jours = {
        "Soleil":  "25,05 jours",
        "Mercure": "58,6 jours",
        "Vénus":   "243 jours",
        "Terre":   "24 h",
        "Mars":    "24,6 h",
        "Jupiter": "9,9 h",
        "Saturne": "10,7 h",
        "Uranus":  "17,2 h",
        "Neptune": "16,1 h",
        "Lune":    "27,3 jours"
    }
    annees = {
        "Soleil":  "2,5 × 10⁸ ans (rotation galactique)",
        "Mercure": "88 jours",
        "Vénus":   "225 jours",
        "Terre":   "365,25 jours",
        "Mars":    "687 jours",
        "Jupiter": "11,86 ans",
        "Saturne": "29,46 ans",
        "Uranus":  "84,01 ans",
        "Neptune": "164,8 ans",
        "Lune":    "27,3 jours"
    }
    axes = {
        "Soleil":  "0 (centre)",
        "Mercure": "57,9 M km",
        "Vénus":   "108,2 M km",
        "Terre":   "149,6 M km",
        "Mars":    "227,9 M km",
        "Jupiter": "778,5 M km",
        "Saturne": "1 433,5 M km",
        "Uranus":  "2 872,5 M km",
        "Neptune": "4 495,1 M km",
        "Lune":    "0,384 M km (Terre-Lune)"
    }

    riemann_val = real_riemann[name]
    riemann_str = f"{riemann_val:.6e}" if not math.isinf(riemann_val) else "+∞ (singularité)"

    planet_data_static[name] = {
        "Diamètre": f"{physical_data[name]['rayon_km']*2:,.0f} km",
        "Masse": f"{physical_data[name]['masse_kg']:.2e} kg",
        "Gravité": grav_str,
        "Température moyenne": temps[name],
        "Jour": jours[name],
        "Année": annees[name],
        "Demi-grand axe réel (M km)": axes[name],
        "Tenseur de Riemann (réel)": riemann_str,
        "Excentricité orbitale": extra_stats[name]["Excentricité"],
        "Inclinaison orbitale (°)": extra_stats[name]["Inclinaison (°)"],
        "Albédo (réfléchissivité)": extra_stats[name]["Albédo"],
        "Densité moyenne (g/cm³)": extra_stats[name]["Densité (g/cm³)"]
    }

planet_descriptions = {
    "Soleil":  "Le Soleil, notre cher ami du quotidien. Son nom vient du latin soliculus, qui désigne un objet brillant dans le ciel. On estime qu'il mourra dans 5 à 7 milliards d'années, avant de devenir une naine blanche. Culturellement, le Soleil a été vénéré en tant que Dieu, et est lié à l'astrolâtrie en tant que pratique. Le Soleil peut aussi émettre des tempêtes solaires, qui ont déjà déstabilisé les satellites environnant la Terre et menacent même aujourd'hui nos appareils informatiques. Néanmoins, cet astre éclaire nos vies tous les jours et on ne pourrait pas vivre sans.",
    "Mercure": "Mercure, la planète la plus proche du Soleil. Elle effectue son année en seulement 88 jours, ce qui est l'année la plus courte du système solaire (la Lune est un satellite). De plus, il ne s'agit pas de la planète la plus chaude du système solaire malgré sa proximité avec notre astre. Ce titre revient à Vénus. Envoyer un satellite près de Mercure reste aussi un défi, car l'attraction solaire rend difficile l'entrée dans son orbite. Elle possède aussi un champ magnétique, qui constitue 80 % de sa densité. Une planète unique dont on entend rarement parler.",
    "Vénus":   "Vénus, la planète la plus chaude du système solaire. Sa température peut atteindre 470 degrés Celsius en raison d'un effet de serre puissant dû à son atmosphère dense en dioxyde de carbone. Elle n'a aucun champ magnétique, à cause de son noyau solide et de l'absence de convection. On la nomme 'étoile du berger' car il s'agit de l'astre qui brille le plus dans le ciel. Chez les Grecs, son nom est celui de la déesse de la beauté et de l'amour. On pense notamment à Vénus qui sort de l'eau.",
    "Terre":   "Notre planète, actuellement menacée par le réchauffement climatique et l'épuisement des ressources renouvelables. Son noyau est aussi chaud que le Soleil, et fournit un champ magnétique qui nous protège des vents solaires. Encore aujourd'hui, il s'agit de la seule planète dans l'univers où nous savons que la vie existe.",
    "Mars":    "Mars, la prochaine cible de la NASA après la Lune. Elle possède deux petites lunes, Phobos et Deimos, qui tournent autour d'elle. Plus remarquablement, la planète contient de l'eau sous forme de glace, ce qui alimente des théories sur l'idée qu'elle aurait pu abriter la vie. Néanmoins, les recherches sont toujours en cours. Aujourd'hui, certains transhumanistes envisagent la colonisation de Mars comme une étape nécessaire pour obtenir des ressources face à leur épuisement sur Terre.",
    "Jupiter": "Jupiter, la plus grande planète du système solaire. Il s'agit d'une planète impressionnante non seulement par sa taille, mais aussi par son champ magnétique qui est 20 000 fois plus puissant que celui de la Terre. La planète est étudiée de façon approfondie aujourd'hui, et possède des cyclones disposés en polygones à ses pôles.",
    "Saturne": "Saturne est une planète fascinante grâce à ses anneaux. En effet, leur épaisseur est de 10 mètres mais ils s'étendent jusqu'à 280 000 kilomètres de la planète. Ils sont également constitués d'eau mêlée à de la poussière et de la roche. Ces anneaux sont visibles tous les 14 à 15 ans en raison de l'inclinaison de la planète, malgré le fait qu'ils soient très fins.",
    "Uranus":  "Uranus est une planète encore mystérieuse pour les astronomes. En effet, initialement découverte par Herschel en 1781, il pensait avoir trouvé une comète ou une nébuleuse. Néanmoins, il s'agissait d'une planète ! Par ailleurs, une seule visite de la planète a été menée par la sonde Voyager 2 en 1986. Elle possède 27 lunes, et un champ magnétique qui n'est pas aligné avec son centre ni son inclinaison. Cela engendre une magnétosphère asymétrique en forme de tire-bouchon. Sa couleur bleue vient par ailleurs du méthane de son atmosphère.",
    "Neptune": "Neptune est une planète fascinante tant par sa découverte que par ses propriétés. Découverte par le calcul avant d'être vue, par Urbain Le Verrier et John Couch Adams : elle fut finalement observée par Johann Galle en 1846 en utilisant ces mêmes calculs pour la localiser. Il s'agit de la planète la plus venteuse, avec des vents pouvant aller jusqu'à 2 100 kilomètres par heure, et elle émet 2,6 fois plus de chaleur qu'elle n'en reçoit du Soleil. Son atmosphère est composée de méthane et d'un autre composé encore inconnu aujourd'hui.",
    "Lune":    "La Lune, notre satellite et le seul corps céleste sur lequel l'homme a marché. Seulement 12 humains y ont marché, dont le fameux Neil Armstrong. Chaque année, la Lune s'éloigne d'ailleurs de 3,8 cm de la Terre. Ses températures sont extrêmes : de 128 degrés Celsius le jour à -173 °C le soir. Un fait intéressant est qu'elle possède des tunnels volcaniques creux, pouvant atteindre plusieurs mètres de large. Certains rêvent d'en faire des abris lunaires ou des bases protégées des radiations. La Lune possède aussi des 'moonquakes' (tremblements de terre lunaires) ; bien que moins forts que ceux de la Terre, leur présence serait justifiée par la contraction de la Lune et les marées gravitationnelles terrestres."
}

DATA_FILE = os.path.join(os.path.dirname(__file__), "planet_data.json")

class RealTimePlanetInfo:
    def __init__(self, root):
        self.root = root
        try:
            icon_img = Image.open("Logo.png")
            self.icon_photo = ImageTk.PhotoImage(icon_img)
            self.root.iconphoto(True, self.icon_photo)
        except Exception as e:
            print(f"Could not load Logo.png: {e}")
        self.root.title("Système solaire - Informations en temps réel")
        self.root.minsize(1000, 600)

        try:
            self.root.state('zoomed')
        except:
            try:
                self.root.attributes('-zoomed', True)
            except:
                sw = self.root.winfo_screenwidth()
                sh = self.root.winfo_screenheight()
                self.root.geometry(f"{sw}x{sh}+0+0")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#f0f0f0", font=("Segoe UI", 9))
        style.configure("TFrame", background="#f0f0f0")
        style.configure("TNotebook", background="#f0f0f0")

        main_paned = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        left_frame = ttk.Frame(main_paned, width=220, relief=tk.RIDGE)
        main_paned.add(left_frame, weight=1)

        ttk.Label(left_frame, text="🌌 Corps célestes", font=("Segoe UI", 14, "bold")).pack(pady=10)
        ttk.Separator(left_frame, orient='horizontal').pack(fill=tk.X, padx=5, pady=5)

        self.tree = ttk.Treeview(left_frame, height=20, selectmode="browse", show="tree")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        ordered_names = ["Soleil", "Mercure", "Vénus", "Terre", "Mars", "Jupiter", "Saturne", "Uranus", "Neptune", "Lune"]
        for nom in ordered_names:
            self.tree.insert("", "end", text=nom, open=False)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        credit_label = ttk.Label(left_frame, text="Simulateur réalisé par\nDAOUADI Zine-Eddine.",
                                 font=("Segoe UI", 8, "italic"), justify=tk.CENTER)
        credit_label.pack(side=tk.BOTTOM, pady=10)

        right_frame = ttk.Frame(main_paned, relief=tk.RIDGE)
        main_paned.add(right_frame, weight=3)

        right_container = ttk.Frame(right_frame)
        right_container.pack(fill=tk.BOTH, expand=True)

        self.image_frame = ttk.Frame(right_container)
        self.image_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        self.image_label = ttk.Label(self.image_frame, background="#e0e0e0", anchor=tk.CENTER)
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.caption_label = ttk.Label(self.image_frame, text="", font=("Segoe UI", 9, "italic"))
        self.caption_label.pack(side=tk.BOTTOM, pady=5)
        self.photo = None

        notebook_frame = ttk.Frame(right_container)
        notebook_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        notebook = ttk.Notebook(notebook_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.realtime_frame = ttk.Frame(notebook)
        notebook.add(self.realtime_frame, text="📡 Temps réel (simulateur)")
        self.create_realtime_display()

        self.static_frame = ttk.Frame(notebook)
        notebook.add(self.static_frame, text="📖 Caractéristiques")
        self.create_static_display()

        self.desc_frame = ttk.Frame(notebook)
        notebook.add(self.desc_frame, text="📝 Description")
        self.create_description_display()

        self.status_var = tk.StringVar()
        self.status_var.set("En attente des données du simulateur...")
        status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.live_data = {}
        self.current_planet = None
        self.update_live_data()

        if self.tree.get_children():
            self.tree.selection_set(self.tree.get_children()[0])
            self.on_select(None)

    def create_realtime_display(self):
        self.realtime_vars = {}
        labels_info = [
            ("Coordonnées X (simulation) :", "x_value"),
            ("Coordonnées Y (simulation) :", "y_value"),
            ("Coordonnées Z (simulation) :", "z_value"),
            ("Angle orbital (modulo 360°) :", "angle_value"),
            ("Distance au Soleil (unités simu) :", "dist_sim"),
            ("Distance réelle (millions km) :", "dist_real"),
            ("Tenseur de Riemann (simulation) :", "riemann_sim")
        ]
        for i, (text, key) in enumerate(labels_info):
            ttk.Label(self.realtime_frame, text=text, font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            var = tk.StringVar(value="---")
            self.realtime_vars[key] = var
            ttk.Label(self.realtime_frame, textvariable=var, font=("Courier", 10), foreground="blue").grid(row=i, column=1, sticky=tk.W, padx=10, pady=5)
        self.realtime_frame.columnconfigure(0, weight=0)
        self.realtime_frame.columnconfigure(1, weight=1)

    def create_static_display(self):
        self.static_vars = {}
        labels_info = [
            ("Diamètre équatorial :", "diam"),
            ("Masse :", "mass"),
            ("Gravité à surface :", "gravity"),
            ("Densité moyenne :", "density"),
            ("Température moyenne :", "temp"),
            ("Durée du jour :", "day"),
            ("Durée de l'année :", "year"),
            ("Demi-grand axe réel :", "semi_major"),
            ("Excentricité orbitale :", "eccentricity"),
            ("Inclinaison orbitale :", "inclination"),
            ("Albédo :", "albedo"),
            ("Tenseur de Riemann (réel) :", "riemann_real")
        ]
        for i, (text, key) in enumerate(labels_info):
            ttk.Label(self.static_frame, text=text, font=("Segoe UI", 10, "bold")).grid(row=i, column=0, sticky=tk.W, padx=10, pady=5)
            var = tk.StringVar(value="---")
            self.static_vars[key] = var
            ttk.Label(self.static_frame, textvariable=var, font=("Segoe UI", 10)).grid(row=i, column=1, sticky=tk.W, padx=10, pady=5)
        self.static_frame.columnconfigure(0, weight=0)
        self.static_frame.columnconfigure(1, weight=1)

    def create_description_display(self):
        self.desc_text = tk.Text(self.desc_frame, wrap=tk.WORD, font=("Segoe UI", 10), bg="#fffff0", state=tk.NORMAL)
        self.desc_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.desc_text.config(state=tk.DISABLED)

    def load_planet_image(self, planet_name):
        custom_sizes = {}
        image_path = os.path.join(os.path.dirname(__file__), f"{planet_name}.jpg")
        if not os.path.exists(image_path):
            image_path = os.path.join(os.path.dirname(__file__), f"{planet_name}.png")
            if not os.path.exists(image_path):
                self.image_label.config(text=f"Image non trouvée\n{planet_name}.jpg", image="")
                self.caption_label.config(text="")
                return
        try:
            pil_img = Image.open(image_path)
            if planet_name in custom_sizes:
                pil_img = pil_img.resize(custom_sizes[planet_name], Image.LANCZOS)
            else:
                pil_img.thumbnail((2000, 200), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(pil_img)
            self.image_label.config(image=self.photo, text="")
            self.caption_label.config(text=f"{planet_name}, source : NASA")
        except Exception as e:
            self.image_label.config(text=f"Erreur chargement\n{planet_name}.jpg", image="")
            self.caption_label.config(text="")

    def update_live_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f:
                    self.live_data = json.load(f)
                self.status_var.set(f"Dernière mise à jour : {datetime.now().strftime('%H:%M:%S')}")
            else:
                self.status_var.set("En attente du simulateur 3D... (fichier manquant)")
        except (json.JSONDecodeError, IOError):
            self.status_var.set("Erreur de lecture des données du simulateur")
        if self.current_planet:
            self.update_realtime_display(self.current_planet)
        self.root.after(500, self.update_live_data)

    def update_realtime_display(self, nom):
        if nom == "Soleil":
            self.realtime_vars["x_value"].set("0.000")
            self.realtime_vars["y_value"].set("-35.000")
            self.realtime_vars["z_value"].set("2.0")
            self.realtime_vars["angle_value"].set("0.00° (fixe)")
            self.realtime_vars["dist_sim"].set("0.00 u")
            self.realtime_vars["dist_real"].set("0.0 M km")
            self.realtime_vars["riemann_sim"].set("+∞ (distance nulle → singularité gravitationnelle)")
            return

        planet_live = None
        if "planetes" in self.live_data:
            for p in self.live_data["planetes"]:
                if p["nom"] == nom:
                    planet_live = p
                    break
        if planet_live:
            angle_deg = planet_live["angle_deg"] % 360.0
            dist_sim = planet_live["distance_sim"]
            dist_real_km = dist_sim * 1_000_000 / 1e6
            riemann_sim = planet_live.get("riemann_coeff", 0.0)
            self.realtime_vars["x_value"].set(f"{planet_live['x']:.3f}")
            self.realtime_vars["y_value"].set(f"{planet_live['y']:.3f}")
            self.realtime_vars["z_value"].set(f"{planet_live['z']:.1f}")
            self.realtime_vars["angle_value"].set(f"{angle_deg:.2f}°  ({planet_live['angle_rad']:.4f} rad)")
            self.realtime_vars["dist_sim"].set(f"{dist_sim:.2f} u")
            self.realtime_vars["dist_real"].set(f"{dist_real_km:.1f} M km")
            if riemann_sim == 0:
                self.realtime_vars["riemann_sim"].set("0.000000")
            else:
                self.realtime_vars["riemann_sim"].set(f"{riemann_sim:.6e}")
        else:
            for var in self.realtime_vars.values():
                var.set("---")

    def update_static_display(self, nom):
        stat = planet_data_static.get(nom, {})
        self.static_vars["diam"].set(stat.get("Diamètre", "---"))
        self.static_vars["mass"].set(stat.get("Masse", "---"))
        self.static_vars["gravity"].set(stat.get("Gravité", "---"))
        self.static_vars["density"].set(stat.get("Densité moyenne (g/cm³)", "---"))
        self.static_vars["temp"].set(stat.get("Température moyenne", "---"))
        self.static_vars["day"].set(stat.get("Jour", "---"))
        self.static_vars["year"].set(stat.get("Année", "---"))
        self.static_vars["semi_major"].set(stat.get("Demi-grand axe réel (M km)", "---"))
        self.static_vars["eccentricity"].set(str(stat.get("Excentricité orbitale", "---")))
        self.static_vars["inclination"].set(str(stat.get("Inclinaison orbitale (°)", "---")))
        self.static_vars["albedo"].set(str(stat.get("Albédo (réfléchissivité)", "---")))
        self.static_vars["riemann_real"].set(stat.get("Tenseur de Riemann (réel)", "---"))

    def update_description_display(self, nom):
        desc = planet_descriptions.get(nom, "Aucune description fournie.")
        self.desc_text.config(state=tk.NORMAL)
        self.desc_text.delete(1.0, tk.END)
        self.desc_text.insert(tk.END, desc)
        self.desc_text.config(state=tk.DISABLED)

    def on_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        nom = self.tree.item(selection[0], "text")
        self.current_planet = nom
        self.update_realtime_display(nom)
        self.update_static_display(nom)
        self.update_description_display(nom)
        self.load_planet_image(nom)

if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimePlanetInfo(root)
    root.mainloop()