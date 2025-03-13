
import random, Maze
import tkinter as tk
from tkinter import filedialog


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
    
    # Kérjük meg a felhasználót, hogy válasszon egy opciót
    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)
    
    # Hangfájl változó
    sound_file = None
    
    tk.Label(frame, text="Válassz egy opciót:").pack(pady=5)
    
    def start_default():
        frame.destroy()
        game = Maze.MazeGame(root, sound_file=sound_file)
    
    def start_random():
        frame.destroy()
        maze = generate_maze(15, 15)
        game = Maze.MazeGame(root, maze, sound_file=sound_file)
    
    def load_from_file():
        filename = filedialog.askopenfilename(title="Labirintus betöltése", 
                                             filetypes=[("Labirintus fájlok", "*.txt"), ("Minden fájl", "*.*")])
        if filename:
            maze = load_maze_from_file(filename)
            if maze:
                frame.destroy()
                game = Maze.MazeGame(root, maze, sound_file=sound_file)
    
    def select_sound():
        nonlocal sound_file
        filename = filedialog.askopenfilename(title="Hangfájl kiválasztása",
                                             filetypes=[("Hangfájlok", "*.wav *.mp3"), ("Minden fájl", "*.*")])
        if filename:
            sound_file = filename
            sound_label.config(text=f"Kiválasztott hang: {filename.split('/')[-1]}")
    
    tk.Button(frame, text="Alapértelmezett pálya", command=start_default).pack(fill=tk.X, pady=2)
    tk.Button(frame, text="Véletlenszerű pálya", command=start_random).pack(fill=tk.X, pady=2)
    tk.Button(frame, text="Pálya betöltése fájlból", command=load_from_file).pack(fill=tk.X, pady=2)
    
    # Hang kiválasztása
    tk.Label(frame, text="\nGratulációs hang:").pack(pady=(10, 2))
    tk.Button(frame, text="Hangfájl kiválasztása", command=select_sound).pack(fill=tk.X, pady=2)
    sound_label = tk.Label(frame, text="Nincs kiválasztva hang")
    sound_label.pack(pady=2)
    
    root.mainloop()


if __name__ == "__main__":
    main()