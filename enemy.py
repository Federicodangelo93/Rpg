import random
import time
import math

class Enemy:
    def __init__(self, x, y, enemy_type="goblin"):
        self.x = x
        self.y = y
        self.tile_size = 32
        self.enemy_type = enemy_type
        
        self.setup_stats()
        
        self.last_move_time = 0
        self.move_delay = 0.3
        self.vision_range = 5
        self.last_attack_time = 0
        self.attack_delay = 1.5
        
        self.target = None
        self.state = "idle"
        self.spawn_x = x
        self.spawn_y = y
        self.max_distance_from_spawn = 8
        
    def setup_stats(self):
        enemy_stats = {
            "goblin": {
                "max_hp": 30, "attack_damage": 8, "defense": 2,
                "experience_reward": 15, "color": "#228B22"
            },
            "orc": {
                "max_hp": 60, "attack_damage": 15, "defense": 5,
                "experience_reward": 35, "color": "#8B4513"
            },
            "skeleton": {
                "max_hp": 40, "attack_damage": 12, "defense": 3,
                "experience_reward": 25, "color": "#F5F5DC"
            },
            "dragon": {
                "max_hp": 200, "attack_damage": 35, "defense": 15,
                "experience_reward": 150, "color": "#DC143C"
            }
        }
        
        stats = enemy_stats.get(self.enemy_type, enemy_stats["goblin"])
        self.max_hp = stats["max_hp"]
        self.hp = self.max_hp
        self.attack_damage = stats["attack_damage"]
        self.defense = stats["defense"]
        self.experience_reward = stats["experience_reward"]
        self.color = stats["color"]
    
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
    
    def distance_to(self, target):
        return math.sqrt((self.x - target.x)**2 + (self.y - target.y)**2)
    
    def can_see_target(self, target):
        distance = self.distance_to(target)
        return distance <= self.vision_range and target.hp > 0
    
    def is_adjacent_to(self, target):
        return (abs(self.x - target.x) <= 1 and 
                abs(self.y - target.y) <= 1 and
                (self.x != target.x or self.y != target.y))
    
    def get_direction_to_target(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        
        if dx > 0:
            dx = 1
        elif dx < 0:
            dx = -1
        
        if dy > 0:
            dy = 1
        elif dy < 0:
            dy = -1
            
        return dx, dy
    
    def move_towards_target(self, target, game_map):
        if not self.can_move():
            return False
            
        dx, dy = self.get_direction_to_target(target)
        new_x = self.x + dx
        new_y = self.y + dy
        
        if (0 <= new_x < len(game_map[0]) and 
            0 <= new_y < len(game_map) and
            game_map[new_y][new_x] != 1):
            
            new_distance_to_spawn = math.sqrt((new_x - self.spawn_x)**2 + (new_y - self.spawn_y)**2)
            if new_distance_to_spawn <= self.max_distance_from_spawn:
                self.x = new_x
                self.y = new_y
                return True
        
        return False
    
    def random_move(self, game_map):
        if not self.can_move():
            return False
            
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy
            
            if (0 <= new_x < len(game_map[0]) and 
                0 <= new_y < len(game_map) and
                game_map[new_y][new_x] != 1):
                
                new_distance_to_spawn = math.sqrt((new_x - self.spawn_x)**2 + (new_y - self.spawn_y)**2)
                if new_distance_to_spawn <= self.max_distance_from_spawn:
                    self.x = new_x
                    self.y = new_y
                    return True
        
        return False
    
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        return self.hp <= 0
    
    def update_ai(self, player, game_map):
        if self.hp <= 0:
            self.state = "dead"
            return
        
        if self.can_see_target(player):
            self.target = player
            self.state = "chasing"
        elif self.state == "chasing" and self.target:
            if self.distance_to(self.target) > self.vision_range * 1.5:
                self.target = None
                self.state = "idle"
        
        if self.state == "idle":
            if random.random() < 0.1:
                self.random_move(game_map)
                
        elif self.state == "chasing" and self.target:
            if not self.is_adjacent_to(self.target):
                self.move_towards_target(self.target, game_map)
    
    def get_pixel_pos(self):
        return (self.x * self.tile_size + self.tile_size // 2,
                self.y * self.tile_size + self.tile_size // 2)