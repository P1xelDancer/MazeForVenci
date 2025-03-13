import tkinter as tk
from tkinter import messagebox, filedialog
import random
import pygame.mixer

class MazeGame:
    def __init__(self, master, maze=None, sound_file=None):
        self.master = master
        self.master.title("Labirintus Játék")
        
        # Hang inicializálása
        try:
            pygame.mixer.init()
            self.sound_enabled = True
        except:
            self.sound_enabled = False
            print("Figyelmeztetés: A pygame.mixer nem inicializálható. A hanglejátszás nem fog működni.")
        
        self.victory_sound = sound_file
        
        # Alapértelmezett színek
        self.wall_color = "black"
        self.path_color = "white"
        self.player_color = "blue"
        self.goal_color = "green"
        self.start_color = "orange"
        
        # Ha nincs megadva labirintus, használjunk egy alapértelmezett mintát
        if maze is None:
            self.maze = [
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                [1, 3, 0, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
                [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
                [1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
                [1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
                [1, 0, 1, 1, 0, 0, 0, 1, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            ]
        else:
            self.maze = maze
            
        # Játékos és kezdő pozíció keresése
        self.start_pos = None
        self.player_pos = None
        
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == 3:  # 3-as a kezdőpozíció
                    self.start_pos = [i, j]
                    # Ha megtaláltuk a kezdőpozíciót, állítsuk be a játékos helyét is
                    if self.player_pos is None:
                        self.player_pos = [i, j]
        
        # Ha nincs kezdőpozíció, alapértelmezetten az [1,1]
        if self.player_pos is None:
            self.player_pos = [1, 1]
            self.start_pos = [1, 1]
        
        # Cél keresése (ha van a pályán 2-es, különben nem lesz cél)
        self.goal_pos = None
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == 2:
                    self.goal_pos = [i, j]
        
        # Egység mérete pixelekben
        self.cell_size = 40
        
        # Canvas létrehozása a megfelelő méretben
        width = len(self.maze[0]) * self.cell_size
        height = len(self.maze) * self.cell_size
        self.canvas = tk.Canvas(master, width=width, height=height, bg="white")
        self.canvas.pack(padx=10, pady=10)
        
        # Labirintus kirajzolása
        self.draw_maze()
        
        # Játékos kirajzolása
        self.player = self.canvas.create_rectangle(
            self.player_pos[1] * self.cell_size + 5,
            self.player_pos[0] * self.cell_size + 5,
            (self.player_pos[1] + 1) * self.cell_size - 5,
            (self.player_pos[0] + 1) * self.cell_size - 5,
            fill=self.player_color
        )
        
        # Billentyűzetkötések
        self.master.bind("<Up>", lambda event: self.move("up"))
        self.master.bind("<Down>", lambda event: self.move("down"))
        self.master.bind("<Left>", lambda event: self.move("left"))
        self.master.bind("<Right>", lambda event: self.move("right"))
        
        # Új játék gomb
        self.new_game_button = tk.Button(master, text="Új Játék", command=self.new_game)
        self.new_game_button.pack(pady=5)
        
    def draw_maze(self):
        """Labirintus kirajzolása"""
        self.canvas.delete("maze")
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                x1, y1 = j * self.cell_size, i * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                
                if self.maze[i][j] == 1:  # Fal
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.wall_color, tags="maze")
                elif self.maze[i][j] == 2:  # Cél
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.goal_color, tags="maze")
                elif self.maze[i][j] == 3:  # Kezdőpozíció
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.start_color, tags="maze")
    
    def move(self, direction):
        """Játékos mozgatása"""
        new_pos = self.player_pos.copy()
        
        if direction == "up":
            new_pos[0] -= 1
        elif direction == "down":
            new_pos[0] += 1
        elif direction == "left":
            new_pos[1] -= 1
        elif direction == "right":
            new_pos[1] += 1
            
        # Ellenőrizzük, hogy az új pozíció nem fal-e
        if 0 <= new_pos[0] < len(self.maze) and 0 <= new_pos[1] < len(self.maze[0]):
            if self.maze[new_pos[0]][new_pos[1]] != 1:  # Nem fal
                self.player_pos = new_pos
                
                # Játékos újrarajzolása
                self.canvas.coords(
                    self.player,
                    self.player_pos[1] * self.cell_size + 5,
                    self.player_pos[0] * self.cell_size + 5,
                    (self.player_pos[1] + 1) * self.cell_size - 5,
                    (self.player_pos[0] + 1) * self.cell_size - 5
                )
                
                # Ellenőrizzük, hogy elértük-e a célt
                if self.goal_pos and self.player_pos[0] == self.goal_pos[0] and self.player_pos[1] == self.goal_pos[1]:
                    # Hanglejátszás, ha van beállítva
                    if self.sound_enabled and self.victory_sound:
                        try:
                            sound = pygame.mixer.Sound(self.victory_sound)
                            sound.play()
                        except Exception as e:
                            print(f"Hiba a hang lejátszása közben: {e}")
                    
                    messagebox.showinfo("Gratulálok!", "Elérted a célt!")
                    self.new_game()
    
    def new_game(self):
        """Új játék indítása"""
        # Játékos visszahelyezése a kezdőpozícióra
        if self.start_pos:
            self.player_pos = self.start_pos.copy()
        else:
            self.player_pos = [1, 1]
        
        # Játékos újrarajzolása
        self.canvas.coords(
            self.player,
            self.player_pos[1] * self.cell_size + 5,
            self.player_pos[0] * self.cell_size + 5,
            (self.player_pos[1] + 1) * self.cell_size - 5,
            (self.player_pos[0] + 1) * self.cell_size - 5
        )