
import tkinter as tk
from tkinter import filedialog
import random, json, os, Maze


def generate_maze(width, height):
    """Egyszerű labirintus generálása"""
    # 1 = fal, 0 = út, 2 = cél, 3 = kezdőpozíció
    
    # Kezdetben minden fal
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    # Kezdőpont - most már 3-as értékkel jelöljük
    maze[1][1] = 3
    
    # Egyszerű út generálása: véletlenszerű útvonal a kezdő és végpont között
    # Ez a módszer nem hoz létre igazi labirintust, csak egy útvonalat
    current = [1, 1]
    stack = [current]
    
    while stack:
        current = stack[-1]
        
        # Választunk egy random irányt
        directions = []
        # Fel
        if current[0] > 2 and maze[current[0]-2][current[1]] == 1:
            directions.append([-1, 0])
        # Le
        if current[0] < height-2 and maze[current[0]+2][current[1]] == 1:
            directions.append([1, 0])
        # Balra
        if current[1] > 2 and maze[current[0]][current[1]-2] == 1:
            directions.append([0, -1])
        # Jobbra
        if current[1] < width-2 and maze[current[0]][current[1]+2] == 1:
            directions.append([0, 1])
        
        if directions:
            # Válasszunk egy véletlenszerű irányt
            direction = random.choice(directions)
            
            # Lépünk ebben az irányban kétszer (a közfalat is átfúrjuk)
            maze[current[0] + direction[0]][current[1] + direction[1]] = 0
            maze[current[0] + 2*direction[0]][current[1] + 2*direction[1]] = 0
            
            # Új pozíció a stack-re
            stack.append([current[0] + 2*direction[0], current[1] + 2*direction[1]])
        else:
            # Ha nincs hova menni, visszalépünk
            stack.pop()
    
    # Helyezzük el a célt
    goal_row = height - 2
    goal_col = width - 2
    
    # Ellenőrzés, hogy biztosan út legyen
    if maze[goal_row][goal_col] == 1:
        # Ha fal, akkor keresünk egy közeli utat
        for i in range(height-2, 1, -1):
            for j in range(width-2, 1, -1):
                if maze[i][j] == 0:
                    goal_row, goal_col = i, j
                    break
            if maze[goal_row][goal_col] == 0:
                break
    
    maze[goal_row][goal_col] = 2
    
    return maze

def get_settings_file():
    """Visszaadja a beállítások fájl elérési útját"""
    # A felhasználó home könyvtárában hozzuk létre
    home_dir = os.path.expanduser("~")
    settings_dir = os.path.join(home_dir, ".maze_game")
    
    # Ha a könyvtár nem létezik, hozzuk létre
    if not os.path.exists(settings_dir):
        os.makedirs(settings_dir)
    
    return os.path.join(settings_dir, "settings.json")


def load_settings():
    """Betölti a beállításokat"""
    settings_file = get_settings_file()
    
    # Ha a fájl nem létezik, alapértelmezett beállításokat adunk vissza
    if not os.path.exists(settings_file):
        return {
            "sound_file": None
        }
    
    try:
        with open(settings_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Hiba a beállítások betöltése közben: {e}")
        return {
            "sound_file": None
        }

def save_settings(settings):
    """Elmenti a beállításokat"""
    settings_file = get_settings_file()
    
    try:
        with open(settings_file, 'w') as f:
            json.dump(settings, f)
        return True
    except Exception as e:
        print(f"Hiba a beállítások mentése közben: {e}")
        return False

def get_statistics_file():
    """Visszaadja a statisztika fájl elérési útját"""
    # A felhasználó home könyvtárában hozzuk létre
    home_dir = os.path.expanduser("~")
    stats_dir = os.path.join(home_dir, ".maze_game")
    
    # Ha a könyvtár nem létezik, hozzuk létre
    if not os.path.exists(stats_dir):
        os.makedirs(stats_dir)
    
    return os.path.join(stats_dir, "statistics.json")


def load_statistics():
    """Betölti a statisztikákat"""
    stats_file = get_statistics_file()
    
    # Ha a fájl nem létezik, üres statisztikát adunk vissza
    if not os.path.exists(stats_file):
        return {
            "Nagyon könnyű": 0,
            "Könnyű": 0,
            "Közepes": 0, 
            "Nehéz": 0,
            "Egyedi": 0
        }
    
    try:
        with open(stats_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Hiba a statisztika betöltése közben: {e}")
        return {
            "Nagyon könnyű": 0,
            "Könnyű": 0,
            "Közepes": 0, 
            "Nehéz": 0,
            "Egyedi": 0
        }


def save_statistics(stats):
    """Elmenti a statisztikákat"""
    stats_file = get_statistics_file()
    
    try:
        with open(stats_file, 'w') as f:
            json.dump(stats, f)
        return True
    except Exception as e:
        print(f"Hiba a statisztika mentése közben: {e}")
        return False


def load_maze_from_file(filename):
    """Labirintus betöltése fájlból"""
    maze = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Figyelmen kívül hagyjuk a kommenteket és az üres sorokat
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                row = [int(cell) for cell in line.strip()]
                maze.append(row)
        
        # Ellenőrizzük, hogy van-e kezdőpozíció (3)
        has_start = any(3 in row for row in maze)
        if not has_start:
            # Ha nincs, akkor az első üres helyet (0) kezdőpozícióvá tesszük
            for i in range(len(maze)):
                for j in range(len(maze[i])):
                    if maze[i][j] == 0:
                        maze[i][j] = 3
                        return maze
        
        return maze
    except Exception as e:
        print(f"Hiba a fájl betöltése közben: {e}")
        return None


def save_maze_to_file(maze, filename):
    """Labirintus mentése fájlba"""
    try:
        with open(filename, 'w') as f:
            # Írjunk egy fejlécet, ami elmagyarázza a számok jelentését
            f.write("# Labirintus fájl formátum:\n")
            f.write("# 0 = üres út\n")
            f.write("# 1 = fal\n")
            f.write("# 2 = cél\n")
            f.write("# 3 = kezdőpozíció\n\n")
            
            for row in maze:
                f.write(''.join(str(cell) for cell in row) + '\n')
        return True
    except Exception as e:
        print(f"Hiba a fájl mentése közben: {e}")
        return False


def main():
    # Főprogram
    root = tk.Tk()
    root.title("Labirintus Játék - Főmenü")
    
    # Statisztikák betöltése
    stats = load_statistics()

    # Beállítások betöltése
    settings = load_settings()
    
    # Kérjük meg a felhasználót, hogy válasszon egy opciót
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Cím
    title_label = tk.Label(frame, text="Labirintus Játék", font=("Arial", 18, "bold"))
    title_label.pack(pady=10)
    
    # Hangfájl változó
    sound_file = settings.get("sound_file")
    
    # Nehézségi szintek méretei
    difficulty_sizes = {
        "Nagyon könnyű": (10, 10),
        "Könnyű": (15, 15),
        "Közepes": (20, 20),
        "Nehéz": (25, 25)
    }
    
    # Játék indítási funkciók
    def start_default():
        frame.destroy()
        game = Maze.MazeGame(root, sound_file=sound_file, difficulty="Nagyon könnyű")
    
    def start_random(difficulty):
        frame.destroy()
        width, height = difficulty_sizes[difficulty]
        maze = generate_maze(width, height)
        game = Maze.MazeGame(root, maze, sound_file=sound_file, difficulty=difficulty)
    
    def load_from_file():
        filename = filedialog.askopenfilename(title="Labirintus betöltése", 
                                             filetypes=[("Labirintus fájlok", "*.txt"), ("Minden fájl", "*.*")])
        if filename:
            maze = load_maze_from_file(filename)
            if maze:
                frame.destroy()
                game = Maze.MazeGame(root, maze, sound_file=sound_file, difficulty="Egyedi")
    
    def select_sound():
        nonlocal sound_file
        filename = filedialog.askopenfilename(title="Hangfájl kiválasztása",
                                             filetypes=[("Hangfájlok", "*.wav *.mp3"), ("Minden fájl", "*.*")])
        if filename:
            sound_file = filename
            # Frissítjük a beállításokat és mentjük
            settings["sound_file"] = filename
            save_settings(settings)
            # Frissítjük a címkét
            sound_display = filename.split('/')[-1] if '/' in filename else filename.split('\\')[-1]
            sound_label.config(text=f"Kiválasztott hang: {sound_display}")
    
    # Játék választó keret
    game_frame = tk.LabelFrame(frame, text="Válassz játékot", font=("Arial", 12), padx=10, pady=10)
    game_frame.pack(fill=tk.X, pady=10)
    
    # Játék gombok - dupla mérettel
    tk.Button(game_frame, text="Alapértelmezett pálya", command=start_default,
             font=("Arial", 12), height=2).pack(fill=tk.X, pady=5)
    
    # Nehézségi szintek alcím
    tk.Label(game_frame, text="Véletlenszerű pályák:", font=("Arial", 11, "bold")).pack(anchor=tk.W, pady=(10, 5))
    
    # Nehézségi szint gombok
    tk.Button(game_frame, text="Nagyon könnyű", command=lambda: start_random("Nagyon könnyű"),
             font=("Arial", 12), height=2).pack(fill=tk.X, pady=5)
    tk.Button(game_frame, text="Könnyű", command=lambda: start_random("Könnyű"),
             font=("Arial", 12), height=2).pack(fill=tk.X, pady=5)
    tk.Button(game_frame, text="Közepes", command=lambda: start_random("Közepes"),
             font=("Arial", 12), height=2).pack(fill=tk.X, pady=5)
    tk.Button(game_frame, text="Nehéz", command=lambda: start_random("Nehéz"),
             font=("Arial", 12), height=2).pack(fill=tk.X, pady=5)
    
    # Pálya betöltése
    tk.Button(game_frame, text="Pálya betöltése fájlból", command=load_from_file,
             font=("Arial", 12), height=2).pack(fill=tk.X, pady=5)
    
    # Hang választó keret
    sound_frame = tk.LabelFrame(frame, text="Gratuláló hang", font=("Arial", 12), padx=10, pady=10)
    sound_frame.pack(fill=tk.X, pady=10)
    
     # Hang kiválasztása
    tk.Button(sound_frame, text="Hangfájl kiválasztása", command=select_sound,
             font=("Arial", 12), height=2).pack(fill=tk.X, pady=5)
    
    # Hangfájl megjelenítése
    sound_text = "Nincs kiválasztva hang"
    if sound_file:
        sound_display = sound_file.split('/')[-1] if '/' in sound_file else sound_file.split('\\')[-1]
        sound_text = f"Kiválasztott hang: {sound_display}"
    
    sound_label = tk.Label(sound_frame, text=sound_text, font=("Arial", 10))
    sound_label.pack(pady=5)
    
    # Statisztika keret
    stats_frame = tk.LabelFrame(frame, text="Teljesített pályák", font=("Arial", 12), padx=10, pady=10)
    stats_frame.pack(fill=tk.X, pady=10)
    
    # Statisztika megjelenítése
    for difficulty, count in stats.items():
        tk.Label(stats_frame, text=f"{difficulty}: {count} pálya", font=("Arial", 11)).pack(anchor=tk.W)
    
    root.mainloop()
    
    root.mainloop()


if __name__ == "__main__":
    main()