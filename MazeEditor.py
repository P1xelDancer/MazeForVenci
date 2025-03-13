import tkinter as tk
from tkinter import filedialog, messagebox

class MazeEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("Labirintus Szerkesztő")
        
        # Alapértelmezett színek
        self.wall_color = "black"
        self.path_color = "white"
        self.start_color = "orange"
        self.goal_color = "green"
        
        # Alapértelmezett méret
        self.width = 10
        self.height = 10
        
        # Mező mérete pixelben
        self.cell_size = 40
        
        # Aktuálisan kiválasztott típus (0: út, 1: fal, 2: cél, 3: kezdőpozíció)
        self.selected_type = 1
        
        # Frame létrehozása a beállításoknak
        self.settings_frame = tk.Frame(master)
        self.settings_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Méret beállítások
        tk.Label(self.settings_frame, text="Szélesség:").grid(row=0, column=0, padx=5, pady=5)
        self.width_var = tk.StringVar(value=str(self.width))
        tk.Entry(self.settings_frame, textvariable=self.width_var, width=5).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.settings_frame, text="Magasság:").grid(row=0, column=2, padx=5, pady=5)
        self.height_var = tk.StringVar(value=str(self.height))
        tk.Entry(self.settings_frame, textvariable=self.height_var, width=5).grid(row=0, column=3, padx=5, pady=5)
        
        tk.Button(self.settings_frame, text="Új labirintus", command=self.create_new_maze).grid(row=0, column=4, padx=5, pady=5)
        
        # Típus választó gombok
        self.type_frame = tk.Frame(master)
        self.type_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        tk.Label(self.type_frame, text="Válassz típust:").grid(row=0, column=0, padx=5, pady=5)
        
        self.type_var = tk.IntVar(value=1)
        tk.Radiobutton(self.type_frame, text="Út", variable=self.type_var, value=0, 
                      command=self.update_selected_type).grid(row=0, column=1, padx=5, pady=5)
        tk.Radiobutton(self.type_frame, text="Fal", variable=self.type_var, value=1, 
                      command=self.update_selected_type).grid(row=0, column=2, padx=5, pady=5)
        tk.Radiobutton(self.type_frame, text="Cél", variable=self.type_var, value=2, 
                      command=self.update_selected_type).grid(row=0, column=3, padx=5, pady=5)
        tk.Radiobutton(self.type_frame, text="Kezdőpozíció", variable=self.type_var, value=3, 
                      command=self.update_selected_type).grid(row=0, column=4, padx=5, pady=5)
        
        # Fájl műveletek
        self.file_frame = tk.Frame(master)
        self.file_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        tk.Button(self.file_frame, text="Mentés", command=self.save_maze).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.file_frame, text="Betöltés", command=self.load_maze).grid(row=0, column=1, padx=5, pady=5)
        
        # Canvas a labirintus szerkesztéséhez
        self.canvas_frame = tk.Frame(master)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Egéresemények
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        
        # Létrehozzuk az alapértelmezett labirintust
        self.create_new_maze()
    
    def create_new_maze(self):
        """Új labirintus létrehozása"""
        try:
            self.width = int(self.width_var.get())
            self.height = int(self.height_var.get())
            
            # Korlátozzuk a méretet az észszerű értékekre
            if self.width < 5:
                self.width = 5
                self.width_var.set(str(self.width))
            if self.height < 5:
                self.height = 5
                self.height_var.set(str(self.height))
            
            if self.width > 50:
                self.width = 50
                self.width_var.set(str(self.width))
            if self.height > 50:
                self.height = 50
                self.height_var.set(str(self.height))
            
            # Alapértelmezett labirintus: minden fal
            self.maze = [[1 for _ in range(self.width)] for _ in range(self.height)]
            
            # Kezdőpozíció (alapértelmezetten 1,1)
            self.maze[1][1] = 3
            
            # Cél (alapértelmezetten jobbra lent)
            self.maze[self.height-2][self.width-2] = 2
            
            # Canvas méretének beállítása
            canvas_width = self.width * self.cell_size
            canvas_height = self.height * self.cell_size
            self.canvas.config(width=canvas_width, height=canvas_height)
            
            # Labirintus kirajzolása
            self.draw_maze()
        except ValueError:
            messagebox.showerror("Hiba", "Érvénytelen méret! Kérlek adj meg érvényes számokat.")
    
    def draw_maze(self):
        """Labirintus kirajzolása"""
        self.canvas.delete("all")
        for i in range(self.height):
            for j in range(self.width):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                
                # Négyzet rajzolása a megfelelő színnel
                if self.maze[i][j] == 0:  # Út
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.path_color, outline="gray")
                elif self.maze[i][j] == 1:  # Fal
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.wall_color, outline="gray")
                elif self.maze[i][j] == 2:  # Cél
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.goal_color, outline="gray")
                elif self.maze[i][j] == 3:  # Kezdőpozíció
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.start_color, outline="gray")
    
    def update_selected_type(self):
        """Frissíti a kiválasztott típust"""
        self.selected_type = self.type_var.get()
    
    def on_click(self, event):
        """Egér kattintás kezelése"""
        # Kiszámoljuk, hogy melyik cellára kattintott a felhasználó
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        # Ellenőrizzük, hogy érvényes-e a cella
        if 0 <= row < self.height and 0 <= col < self.width:
            # Ha kezdőpozíciót vagy célt választott, akkor ellenőrizzük, hogy van-e már másik
            if self.selected_type == 3:  # Kezdőpozíció
                # Töröljük a korábbi kezdőpozíciót, ha volt
                for i in range(self.height):
                    for j in range(self.width):
                        if self.maze[i][j] == 3 and (i != row or j != col):
                            self.maze[i][j] = 0
            
            # Beállítjuk a kiválasztott típust
            self.maze[row][col] = self.selected_type
            
            # Újrarajzoljuk a labirintust
            self.draw_maze()
    
    def on_drag(self, event):
        """Egér húzás kezelése"""
        # Ugyanaz, mint a kattintás
        self.on_click(event)
    
    def save_maze(self):
        """Labirintus mentése fájlba"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Szöveges fájlok", "*.txt"), ("Minden fájl", "*.*")],
            title="Labirintus mentése"
        )
        if not filename:
            return
            
        try:
            with open(filename, 'w') as f:
                # Írjunk egy fejlécet, ami elmagyarázza a számok jelentését
                f.write("# Labirintus fájl formátum:\n")
                f.write("# 0 = üres út\n")
                f.write("# 1 = fal\n")
                f.write("# 2 = cél\n")
                f.write("# 3 = kezdőpozíció\n\n")
                
                for row in self.maze:
                    f.write(''.join(str(cell) for cell in row) + '\n')
            messagebox.showinfo("Siker", "Labirintus sikeresen elmentve!")
        except Exception as e:
            messagebox.showerror("Hiba", f"Nem sikerült a mentés: {e}")
            
    def load_maze(self):
        """Labirintus betöltése fájlból"""
        filename = filedialog.askopenfilename(
            filetypes=[("Szöveges fájlok", "*.txt"), ("Minden fájl", "*.*")],
            title="Labirintus betöltése"
        )
        if not filename:
            return
            
        try:
            maze = []
            with open(filename, 'r') as f:
                for line in f:
                    # Figyelmen kívül hagyjuk a kommenteket és az üres sorokat
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    row = [int(cell) for cell in line.strip()]
                    maze.append(row)
            
            # Ellenőrizzük, hogy érvényes-e a labirintus
            if not maze:
                messagebox.showerror("Hiba", "A fájl nem tartalmaz érvényes labirintust!")
                return
                
            # Ellenőrizzük, hogy van-e kezdőpozíció
            has_start = any(3 in row for row in maze)
            if not has_start:
                if messagebox.askyesno("Figyelmeztetés", "A labirintusban nincs kezdőpozíció. Hozzáadjunk egyet?"):
                    # Az első szabad helyre tesszük a kezdőpozíciót
                    for i in range(len(maze)):
                        for j in range(len(maze[i])):
                            if maze[i][j] == 0:
                                maze[i][j] = 3
                                break
                        if any(3 in row for row in maze):
                            break
            
            # Beállítjuk az új méretet
            self.height = len(maze)
            self.width = len(maze[0])
            self.height_var.set(str(self.height))
            self.width_var.set(str(self.width))
            
            # Beállítjuk az új labirintust
            self.maze = maze
            
            # Canvas méretének beállítása
            canvas_width = self.width * self.cell_size
            canvas_height = self.height * self.cell_size
            self.canvas.config(width=canvas_width, height=canvas_height)
            
            # Újrarajzoljuk a labirintust
            self.draw_maze()
            
            messagebox.showinfo("Siker", "Labirintus sikeresen betöltve!")
        except Exception as e:
            messagebox.showerror("Hiba", f"Nem sikerült a betöltés: {e}")


def main():
    root = tk.Tk()
    app = MazeEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()