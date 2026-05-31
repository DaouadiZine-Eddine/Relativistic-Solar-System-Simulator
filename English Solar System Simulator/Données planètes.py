import tkinter as tk
from tkinter import ttk
import json
import os
import math
from datetime import datetime
from PIL import Image, ImageTk

def real_riemann(mass_kg, radius_km):
    G = 6.67430e-11
    c = 299792458.0
    r_m = radius_km * 1000.0
    if r_m == 0:
        return float('inf')
    R = (2 * G * mass_kg) / (c**2 * r_m**3)
    return R * 1e18

physical_data = {
    "Sun":      {"mass_kg": 1.989e30, "radius_km": 695700.0},
    "Mercury":  {"mass_kg": 3.30e23,  "radius_km": 2439.7},
    "Venus":    {"mass_kg": 4.87e24,  "radius_km": 6051.8},
    "Earth":    {"mass_kg": 5.97e24,  "radius_km": 6371.0},
    "Mars":     {"mass_kg": 6.42e23,  "radius_km": 3389.5},
    "Jupiter":  {"mass_kg": 1.90e27,  "radius_km": 69911.0},
    "Saturn":   {"mass_kg": 5.68e26,  "radius_km": 58232.0},
    "Uranus":   {"mass_kg": 8.68e25,  "radius_km": 25362.0},
    "Neptune":  {"mass_kg": 1.02e26,  "radius_km": 24622.0},
    "Moon":     {"mass_kg": 7.35e22,  "radius_km": 1737.4}
}

real_riemann_dict = {name: real_riemann(data["mass_kg"], data["radius_km"]) for name, data in physical_data.items()}

extra_stats = {
    "Sun":      {"Eccentricity": 0.0,    "Inclination (°)": 0.0, "Albedo": 0.999, "Density (g/cm³)": 1.41},
    "Mercury":  {"Eccentricity": 0.2056, "Inclination (°)": 7.0, "Albedo": 0.088, "Density (g/cm³)": 5.43},
    "Venus":    {"Eccentricity": 0.0068, "Inclination (°)": 3.4, "Albedo": 0.65,  "Density (g/cm³)": 5.24},
    "Earth":    {"Eccentricity": 0.0167, "Inclination (°)": 0.0, "Albedo": 0.306, "Density (g/cm³)": 5.51},
    "Mars":     {"Eccentricity": 0.0934, "Inclination (°)": 1.9, "Albedo": 0.170, "Density (g/cm³)": 3.93},
    "Jupiter":  {"Eccentricity": 0.0489, "Inclination (°)": 1.3, "Albedo": 0.52,  "Density (g/cm³)": 1.33},
    "Saturn":   {"Eccentricity": 0.0565, "Inclination (°)": 2.5, "Albedo": 0.47,  "Density (g/cm³)": 0.69},
    "Uranus":   {"Eccentricity": 0.0457, "Inclination (°)": 0.8, "Albedo": 0.51,  "Density (g/cm³)": 1.27},
    "Neptune":  {"Eccentricity": 0.0113, "Inclination (°)": 1.8, "Albedo": 0.41,  "Density (g/cm³)": 1.64},
    "Moon":     {"Eccentricity": 0.0549, "Inclination (°)": 5.1, "Albedo": 0.136, "Density (g/cm³)": 3.34}
}

planet_data_static = {}
for name in physical_data.keys():
    if name == "Sun":
        G = 6.67430e-11
        M = physical_data["Sun"]["mass_kg"]
        R_m = physical_data["Sun"]["radius_km"] * 1000
        grav = (G * M) / (R_m**2)
        grav_str = f"{grav:.0f} m/s²"
    else:
        grav_str = f"{9.81 * (physical_data[name]['mass_kg']/5.97e24) / ((physical_data[name]['radius_km']/6371.0)**2):.1f} m/s²"

    temps = {
        "Sun":     "5 500 °C (surface)",
        "Mercury": "167 °C",
        "Venus":   "462 °C",
        "Earth":   "15 °C",
        "Mars":    "-65 °C",
        "Jupiter": "-110 °C",
        "Saturn":  "-140 °C",
        "Uranus":  "-195 °C",
        "Neptune": "-200 °C",
        "Moon":    "-20 °C (average)"
    }
    days = {
        "Sun":     "25.05 days",
        "Mercury": "58.6 days",
        "Venus":   "243 days",
        "Earth":   "24 h",
        "Mars":    "24.6 h",
        "Jupiter": "9.9 h",
        "Saturn":  "10.7 h",
        "Uranus":  "17.2 h",
        "Neptune": "16.1 h",
        "Moon":    "27.3 days"
    }
    years = {
        "Sun":     "2.5 × 10⁸ years (galactic rotation)",
        "Mercury": "88 days",
        "Venus":   "225 days",
        "Earth":   "365.25 days",
        "Mars":    "687 days",
        "Jupiter": "11.86 years",
        "Saturn":  "29.46 years",
        "Uranus":  "84.01 years",
        "Neptune": "164.8 years",
        "Moon":    "27.3 days"
    }
    axes = {
        "Sun":     "0 (center)",
        "Mercury": "57.9 M km",
        "Venus":   "108.2 M km",
        "Earth":   "149.6 M km",
        "Mars":    "227.9 M km",
        "Jupiter": "778.5 M km",
        "Saturn":  "1 433.5 M km",
        "Uranus":  "2 872.5 M km",
        "Neptune": "4 495.1 M km",
        "Moon":    "0.384 M km (Earth-Moon)"
    }

    riemann_val = real_riemann_dict[name]
    riemann_str = f"{riemann_val:.6e}" if not math.isinf(riemann_val) else "+∞ (singularity)"

    planet_data_static[name] = {
        "Diameter": f"{physical_data[name]['radius_km']*2:,.0f} km",
        "Mass": f"{physical_data[name]['mass_kg']:.2e} kg",
        "Gravity": grav_str,
        "Average temperature": temps[name],
        "Day length": days[name],
        "Year length": years[name],
        "Real semi-major axis (M km)": axes[name],
        "Riemann tensor (real)": riemann_str,
        "Orbital eccentricity": extra_stats[name]["Eccentricity"],
        "Orbital inclination (°)": extra_stats[name]["Inclination (°)"],
        "Albedo (reflectivity)": extra_stats[name]["Albedo"],
        "Average density (g/cm³)": extra_stats[name]["Density (g/cm³)"]
    }

planet_descriptions = {
    "Sun": "The Sun, our dear daily friend. Its name comes from the Latin 'soliculus', which refers to a bright object in the sky. It is estimated that it will die in 5 to 7 billion years, before becoming a white dwarf. Culturally, the Sun has been worshipped as a god and is linked to astrolatry as a practice. The Sun can also emit solar storms, which have already destabilized satellites around Earth and still threaten our computer devices today. Nevertheless, this star lights our lives every day and we could not live without it.",
    "Mercury": "Mercury, the closest planet to the Sun. It completes its year in only 88 days, which is the shortest year in the solar system (the Moon is a satellite). Moreover, it is not the hottest planet in the solar system despite its proximity to our star. That title goes to Venus. Sending a satellite near Mercury remains a challenge because the Sun's gravity makes it difficult to enter its orbit. It also has a magnetic field, which makes up 80% of its density. A unique planet that we rarely hear about.",
    "Venus": "Venus, the hottest planet in the solar system. Its temperature can reach 470 degrees Celsius due to a strong greenhouse effect from its dense carbon dioxide atmosphere. It has no magnetic field, because of its solid core and lack of convection. It is called the 'evening star' because it is the brightest object in the sky. For the Greeks, its name is that of the goddess of beauty and love. One thinks of Venus rising from the water.",
    "Earth": "Our planet, currently threatened by global warming and the depletion of renewable resources. Its core is as hot as the Sun, and provides a magnetic field that protects us from solar winds. Today, it is still the only planet in the universe where we know life exists.",
    "Mars": "Mars, NASA's next target after the Moon. It has two small moons, Phobos and Deimos, that orbit around it. More notably, the planet contains water in the form of ice, fueling theories that it might have hosted life. Nevertheless, research is ongoing. Today, some transhumanists see the colonization of Mars as a necessary step to obtain resources as they run out on Earth.",
    "Jupiter": "Jupiter, the largest planet in the solar system. It is an impressive planet not only for its size, but also for its magnetic field, which is 20,000 times stronger than Earth's. The planet is being studied extensively today, and has cyclones arranged in polygons at its poles.",
    "Saturn": "Saturn is a fascinating planet because of its rings. Indeed, they are only 10 meters thick but extend up to 280,000 kilometers from the planet. They are also made of water mixed with dust and rock. These rings are visible every 14 to 15 years due to the planet's tilt, despite being very thin.",
    "Uranus": "Uranus is still a mysterious planet for astronomers. Initially discovered by Herschel in 1781, he thought he had found a comet or a nebula. However, it was a planet! Furthermore, only one visit to the planet has been made by the Voyager 2 probe in 1986. It has 27 moons, and a magnetic field that is not aligned with its center or its tilt. This creates an asymmetric corkscrew-shaped magnetosphere. Its blue color comes from the methane in its atmosphere.",
    "Neptune": "Neptune is a fascinating planet both for its discovery and its properties. Discovered by calculation before being seen, by Urbain Le Verrier and John Couch Adams: it was finally observed by Johann Galle in 1846 using those same calculations to locate it. It is the windiest planet, with winds reaching up to 2,100 kilometers per hour, and it emits 2.6 times more heat than it receives from the Sun. Its atmosphere is composed of methane and another compound still unknown today.",
    "Moon": "The Moon, our satellite and the only celestial body on which man has walked. Only 12 humans have walked on it, including the famous Neil Armstrong. Each year, the Moon moves 3.8 cm away from Earth. Its temperatures are extreme: from 128 degrees Celsius during the day to -173 °C at night. An interesting fact is that it has hollow volcanic tunnels, which can be several meters wide. Some dream of making them lunar shelters or bases protected from radiation. The Moon also has 'moonquakes'; although weaker than those on Earth, their presence is attributed to the Moon's contraction and Earth's gravitational tides."
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
        self.root.title("Solar System - Real-time Information")
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

        ttk.Label(left_frame, text="🌌 Celestial bodies", font=("Segoe UI", 14, "bold")).pack(pady=10)
        ttk.Separator(left_frame, orient='horizontal').pack(fill=tk.X, padx=5, pady=5)

        self.tree = ttk.Treeview(left_frame, height=20, selectmode="browse", show="tree")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        ordered_names = ["Sun", "Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Moon"]
        for name in ordered_names:
            self.tree.insert("", "end", text=name, open=False)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        credit_label = ttk.Label(left_frame, text="Simulator made by\nDAOUADI Zine-Eddine.",
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
        notebook.add(self.realtime_frame, text="📡 Real time (simulator)")
        self.create_realtime_display()

        self.static_frame = ttk.Frame(notebook)
        notebook.add(self.static_frame, text="📖 Characteristics")
        self.create_static_display()

        self.desc_frame = ttk.Frame(notebook)
        notebook.add(self.desc_frame, text="📝 Description")
        self.create_description_display()

        self.status_var = tk.StringVar()
        self.status_var.set("Waiting for simulator data...")
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
            ("X coordinate (simulation):", "x_value"),
            ("Y coordinate (simulation):", "y_value"),
            ("Z coordinate (simulation):", "z_value"),
            ("Orbital angle (mod 360°):", "angle_value"),
            ("Distance to Sun (sim units):", "dist_sim"),
            ("Real distance (million km):", "dist_real"),
            ("Riemann tensor (simulation):", "riemann_sim")
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
            ("Equatorial diameter:", "diam"),
            ("Mass:", "mass"),
            ("Surface gravity:", "gravity"),
            ("Average density:", "density"),
            ("Average temperature:", "temp"),
            ("Day length:", "day"),
            ("Year length:", "year"),
            ("Real semi-major axis:", "semi_major"),
            ("Orbital eccentricity:", "eccentricity"),
            ("Orbital inclination:", "inclination"),
            ("Albedo:", "albedo"),
            ("Riemann tensor (real):", "riemann_real")
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
        file_basename = "Terre" if planet_name == "Earth" else planet_name
        
        custom_sizes = {}
        image_path = os.path.join(os.path.dirname(__file__), f"{file_basename}.jpg")
        if not os.path.exists(image_path):
            image_path = os.path.join(os.path.dirname(__file__), f"{file_basename}.png")
            if not os.path.exists(image_path):
                self.image_label.config(text=f"Image not found\n{file_basename}.jpg", image="")
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
            self.caption_label.config(text=f"{planet_name}, source: NASA")
        except Exception as e:
            self.image_label.config(text=f"Error loading\n{file_basename}.jpg", image="")
            self.caption_label.config(text="")

    def update_live_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, "r") as f:
                    self.live_data = json.load(f)
                self.status_var.set(f"Last update: {datetime.now().strftime('%H:%M:%S')}")
            else:
                self.status_var.set("Waiting for 3D simulator... (missing file)")
        except (json.JSONDecodeError, IOError):
            self.status_var.set("Error reading simulator data")
        if self.current_planet:
            self.update_realtime_display(self.current_planet)
        self.root.after(500, self.update_live_data)

    def update_realtime_display(self, name):
        if name == "Sun":
            self.realtime_vars["x_value"].set("0.000")
            self.realtime_vars["y_value"].set("-35.000")
            self.realtime_vars["z_value"].set("2.0")
            self.realtime_vars["angle_value"].set("0.00° (fixed)")
            self.realtime_vars["dist_sim"].set("0.00 u")
            self.realtime_vars["dist_real"].set("0.0 M km")
            self.realtime_vars["riemann_sim"].set("+∞ (zero distance → gravitational singularity)")
            return

        planet_live = None
        if "planetes" in self.live_data:
            for p in self.live_data["planetes"]:
                if p["nom"] == name:
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

    def update_static_display(self, name):
        stat = planet_data_static.get(name, {})
        self.static_vars["diam"].set(stat.get("Diameter", "---"))
        self.static_vars["mass"].set(stat.get("Mass", "---"))
        self.static_vars["gravity"].set(stat.get("Gravity", "---"))
        self.static_vars["density"].set(stat.get("Average density (g/cm³)", "---"))
        self.static_vars["temp"].set(stat.get("Average temperature", "---"))
        self.static_vars["day"].set(stat.get("Day length", "---"))
        self.static_vars["year"].set(stat.get("Year length", "---"))
        self.static_vars["semi_major"].set(stat.get("Real semi-major axis (M km)", "---"))
        self.static_vars["eccentricity"].set(str(stat.get("Orbital eccentricity", "---")))
        self.static_vars["inclination"].set(str(stat.get("Orbital inclination (°)", "---")))
        self.static_vars["albedo"].set(str(stat.get("Albedo (reflectivity)", "---")))
        self.static_vars["riemann_real"].set(stat.get("Riemann tensor (real)", "---"))

    def update_description_display(self, name):
        desc = planet_descriptions.get(name, "No description provided.")
        self.desc_text.config(state=tk.NORMAL)
        self.desc_text.delete(1.0, tk.END)
        self.desc_text.insert(tk.END, desc)
        self.desc_text.config(state=tk.DISABLED)

    def on_select(self, event):
        selection = self.tree.selection()
        if not selection:
            return
        name = self.tree.item(selection[0], "text")
        self.current_planet = name
        self.update_realtime_display(name)
        self.update_static_display(name)
        self.update_description_display(name)
        self.load_planet_image(name)

if __name__ == "__main__":
    root = tk.Tk()
    app = RealTimePlanetInfo(root)        
    root.mainloop()