import tkinter as tk
from tkinter import Canvas, Frame, Label
import random

# Importar nuestros módulos
from player import Player
from enemy import Enemy
from combat_system import CombatSystem
from game_map import GameMap

class AOGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("AO Style Game - Sistema de Combate")
        self.root.resizable(False, False)
        
        # Inicializar sistemas del juego
        self.game_map = GameMap()
        self.player = Player(3, 3)
        self.combat_system = CombatSystem()
        self.enemies = []
        
        # Crear enemigos
        self.spawn_enemies()
        
        # Configurar interfaz
        self.setup_ui()
        
        # Eventos de teclado
        self.keys_pressed = set()
        self.root.bind("<KeyPress>", self.on_key_down)
        self.root.bind("<KeyRelease>", self.on_key_up)
        self.root.focus_set()
        
        self.selected_enemy = None
        self.update_display()
        self.game_loop()
    
    def setup_ui(self):
        # Canvas principal
        map_width = len(self.game_map.map_data[0]) * 32
        map_height = len(self.game_map.map_data) * 32
        
        self.canvas = Canvas(self.root, width=map_width, height=map_height, bg="#000000")
        self.canvas.pack()
        
        # Panel de información
        info_frame = Frame(self.root)
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Stats del jugador
        stats_frame = Frame(info_frame)
        stats_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        self.hp_label = Label(stats_frame, text="HP: 100/100", fg="red")
        self.hp_label.pack(anchor=tk.W)
        
        self.mana_label = Label(stats_frame, text="Maná: 50/50", fg="blue")
        self.mana_label.pack(anchor=tk.W)
        
        self.level_label = Label(stats_frame, text="Nivel: 1")
        self.level_label.pack(anchor=tk.W)
        
        self.exp_label = Label(stats_frame, text="EXP: 0/100")
        self.exp_label.pack(anchor=tk.W)
        
        # Controles
        controls_frame = Frame(info_frame)
        controls_frame.pack(side=tk.RIGHT)
        
        Label(controls_frame, text="WASD: Mover").pack(anchor=tk.E)
        Label(controls_frame, text="ESPACIO: Atacar").pack(anchor=tk.E)
        Label(controls_frame, text="TAB: Seleccionar enemigo").pack(anchor=tk.E)
        
        # Log de combate
        log_frame = Frame(self.root)
        log_frame.pack(fill=tk.X, padx=5)
        
        Label(log_frame, text="Log de Combate:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.log_text = tk.Text(log_frame, height=6, width=80, bg="#F0F0F0", state=tk.DISABLED)
        self.log_text.pack(fill=tk.X)
    
    def spawn_enemies(self):
        enemy_spawns = [
            (10, 3, "goblin"), (15, 5, "orc"), (8, 8, "skeleton"),
            (12, 10, "goblin"), (16, 8, "goblin"), (6, 6, "skeleton"),
            (14, 3, "orc"), (18, 10, "dragon")
        ]
        
        for x, y, enemy_type in enemy_spawns:
            if self.game_map.map_data[y][x] == 0:
                enemy = Enemy(x, y, enemy_type)
                self.enemies.append(enemy)
    
    def on_key_down(self, event):
        self.keys_pressed.add(event.keysym.lower())
    
    def on_key_up(self, event):
        self.keys_pressed.discard(event.keysym.lower())
    
    def handle_input(self):
        # Movimiento
        moves = {
            'w': (0, -1), 'up': (0, -1),
            's': (0, 1), 'down': (0, 1),
            'a': (-1, 0), 'left': (-1, 0),
            'd': (1, 0), 'right': (1, 0)
        }
        
        for key in self.keys_pressed:
            if key in moves:
                dx, dy = moves[key]
                if self.player.move(dx, dy, self.game_map.map_data):
                    self.update_display()
                break
        
        # Ataque
        if 'space' in self.keys_pressed:
            self.keys_pressed.discard('space')
            self.handle_attack()
        
        # Seleccionar enemigo
        if 'tab' in self.keys_pressed:
            self.keys_pressed.discard('tab')
            self.select_next_enemy()
    
    def handle_attack(self):
        adjacent_enemies = []
        for enemy in self.enemies:
            if enemy.hp > 0 and self.player.is_adjacent_to(enemy):
                adjacent_enemies.append(enemy)
        
        if not adjacent_enemies:
            self.combat_system.add_to_log("No hay enemigos cerca para atacar")
            return
        
        target = None
        if self.selected_enemy and self.selected_enemy in adjacent_enemies:
            target = self.selected_enemy
        else:
            target = adjacent_enemies[0]
        
        success, message = self.combat_system.player_attack_enemy(self.player, target)
        
        if target.hp <= 0:
            self.selected_enemy = None
    
    def select_next_enemy(self):
        alive_enemies = [e for e in self.enemies if e.hp > 0]
        if not alive_enemies:
            self.selected_enemy = None
            return
        
        if self.selected_enemy not in alive_enemies:
            self.selected_enemy = alive_enemies[0]
        else:
            current_index = alive_enemies.index(self.selected_enemy)
            next_index = (current_index + 1) % len(alive_enemies)
            self.selected_enemy = alive_enemies[next_index]
    
    def update_enemies(self):
        for enemy in self.enemies:
            if enemy.hp > 0:
                enemy.update_ai(self.player, self.game_map.map_data)
                
                if enemy.is_adjacent_to(self.player):
                    self.combat_system.enemy_attack_player(enemy, self.player)
    
    def update_display(self):
        self.canvas.delete("all")
        
        # Dibujar mapa
        self.game_map.draw(self.canvas)
        
        # Dibujar enemigos
        for enemy in self.enemies:
            if enemy.hp > 0:
                px, py = enemy.get_pixel_pos()
                
                # Destacar enemigo seleccionado
                if enemy == self.selected_enemy:
                    self.canvas.create_oval(px-16, py-16, px+16, py+16, 
                                          fill="yellow", outline="orange", 
                                          width=3, tags="enemy_select")
                
                # Dibujar enemigo
                self.canvas.create_rectangle(px-10, py-10, px+10, py+10, 
                                           fill=enemy.color, outline="black", 
                                           width=2, tags="enemy")
                
                # Barra de vida
                hp_ratio = enemy.hp / enemy.max_hp
                bar_width = 20
                bar_height = 4
                
                self.canvas.create_rectangle(px-bar_width//2, py-18, 
                                           px+bar_width//2, py-14, 
                                           fill="red", outline="black", 
                                           tags="enemy_hp_bg")
                
                self.canvas.create_rectangle(px-bar_width//2, py-18, 
                                           px-bar_width//2 + int(bar_width * hp_ratio), py-14, 
                                           fill="green", tags="enemy_hp")
        
        # Dibujar jugador
        px, py = self.player.get_pixel_pos()
        self.canvas.create_oval(px-12, py-12, px+12, py+12, 
                               fill=self.player.color, outline="#000080", 
                               width=2, tags="player")
        
        self.update_ui()
    
    def update_ui(self):
        self.hp_label.config(text=f"HP: {self.player.hp}/{self.player.max_hp}")
        self.mana_label.config(text=f"Maná: {self.player.mana}/{self.player.max_mana}")
        self.level_label.config(text=f"Nivel: {self.player.level}")
        self.exp_label.config(text=f"EXP: {self.player.experience}/{self.player.experience_to_next_level}")
        
        # Log de combate
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        for message in self.combat_system.get_combat_log():
            self.log_text.insert(tk.END, message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.see(tk.END)
    
    def game_loop(self):
        if self.player.hp > 0:
            self.handle_input()
            self.update_enemies()
            self.update_display()
        else:
            self.canvas.create_text(320, 200, text="GAME OVER", 
                                  fill="red", font=("Arial", 24, "bold"))
        
        self.root.after(50, self.game_loop)
    
    def run(self):
        self.root.mainloop()

# Ejecutar el juego
if __name__ == "__main__":
    game = AOGame()
    game.run()


#hola

