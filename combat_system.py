import random

class CombatSystem:
    def __init__(self):
        self.combat_log = []
        self.max_log_entries = 10
    
    def add_to_log(self, message):
        self.combat_log.append(message)
        if len(self.combat_log) > self.max_log_entries:
            self.combat_log.pop(0)
    
    def player_attack_enemy(self, player, enemy):
        if not player.can_attack():
            return False, "Debes esperar para atacar de nuevo"
        
        if not player.is_adjacent_to(enemy):
            return False, "El enemigo está muy lejos"
        
        if enemy.hp <= 0:
            return False, "El enemigo ya está muerto"
        
        base_damage = player.attack_damage
        critical_chance = 0.1
        
        is_critical = random.random() < critical_chance
        if is_critical:
            damage = int(base_damage * 1.5)
        else:
            damage = base_damage
        
        final_damage = max(1, damage - enemy.defense)
        enemy_died = enemy.take_damage(final_damage)
        
        if is_critical:
            message = f"¡CRÍTICO! Hiciste {final_damage} de daño al {enemy.enemy_type}"
        else:
            message = f"Hiciste {final_damage} de daño al {enemy.enemy_type}"
        
        self.add_to_log(message)
        
        if enemy_died:
            exp_gained = enemy.experience_reward
            player.gain_experience(exp_gained)
            self.add_to_log(f"¡Derrotaste al {enemy.enemy_type}! (+{exp_gained} EXP)")
        
        return True, message
    
    def enemy_attack_player(self, enemy, player):
        if not enemy.can_attack():
            return False
        
        if not enemy.is_adjacent_to(player):
            return False
        
        if player.hp <= 0:
            return False
        
        damage = max(1, enemy.attack_damage - player.defense)
        player_died = player.take_damage(damage)
        
        message = f"El {enemy.enemy_type} te hizo {damage} de daño"
        self.add_to_log(message)
        
        if player_died:
            self.add_to_log("¡Has muerto!")
        
        return True
    
    def get_combat_log(self):
        return self.combat_log.copy()