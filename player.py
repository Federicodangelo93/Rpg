import time

class Player:
    def __init__(self, x=5, y=5):
        self.x = x
        self.y = y
        self.tile_size = 32
        self.color = "#4169E1"
        self.last_move_time = 0
        self.move_delay = 0.15
        
        # Estadísticas de combate
        self.max_hp = 100
        self.hp = self.max_hp
        self.max_mana = 50
        self.mana = self.max_mana
        self.attack_damage = 15
        self.defense = 5
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        
        # Estado de combate
        self.in_combat = False
        self.target = None
        self.last_attack_time = 0
        self.attack_delay = 1.0
        
    def can_move(self):
        current_time = time.time()
        if current_time - self.last_move_time >= self.move_delay:
            self.last_move_time = current_time
            return True
        return False
    
    def can_attack(self):
        current_time = time.time()
        if current_time - self.last_attack_time >= self.attack_delay:
            self.last_attack_time = current_time
            return True
        return False
    
    def move(self, dx, dy, game_map):
        if not self.can_move():
            return False
            
        new_x = self.x + dx
        new_y = self.y + dy
        
        if (0 <= new_x < len(game_map[0]) and 
            0 <= new_y < len(game_map) and
            game_map[new_y][new_x] != 1):
            
            self.x = new_x
            self.y = new_y
            return True
        return False
    
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        return self.hp <= 0
    
    def gain_experience(self, exp):
        self.experience += exp
        while self.experience >= self.experience_to_next_level:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.experience -= self.experience_to_next_level
        self.experience_to_next_level = int(self.experience_to_next_level * 1.2)
        
        old_max_hp = self.max_hp
        self.max_hp += 20
        self.hp += (self.max_hp - old_max_hp)
        
        self.max_mana += 10
        self.mana = self.max_mana
        self.attack_damage += 3
        self.defense += 1
        
        return True
    
    def is_adjacent_to(self, target):
        return (abs(self.x - target.x) <= 1 and 
                abs(self.y - target.y) <= 1 and
                (self.x != target.x or self.y != target.y))
    
    def get_pixel_pos(self):
        return (self.x * self.tile_size + self.tile_size // 2,
                self.y * self.tile_size + self.tile_size // 2)