"""Constantes do jogo. Mexe aqui para balancear a dificuldade!"""

WIDTH, HEIGHT = 1000, 700
FPS = 60

# Cores (R, G, B)
BG = (24, 26, 33)
GRID = (34, 37, 46)
WHITE = (240, 240, 240)
RED = (220, 70, 70)
GREEN = (80, 200, 120)
BLUE = (80, 140, 255)
YELLOW = (250, 210, 70)
PURPLE = (170, 90, 220)

# Jogador
PLAYER_SPEED = 230
PLAYER_MAX_HP = 100
PLAYER_RADIUS = 14
INVULN_TIME = 0.5  # segundos de invencibilidade após levar dano

# Inimigos
SPAWN_INTERVAL_START = 1.0
SPAWN_INTERVAL_MIN = 0.15
ENEMY_TYPES = {
    "bat":   {"hp": 10, "speed": 90,  "damage": 8,  "radius": 10, "color": PURPLE, "xp": 1},
    "zombie": {"hp": 30, "speed": 55, "damage": 15, "radius": 16, "color": GREEN,  "xp": 3},
}

# Arma
WEAPON_COOLDOWN = 0.8
PROJECTILE_SPEED = 450
PROJECTILE_DAMAGE = 10
PROJECTILE_LIFETIME = 1.5

# XP
XP_BASE = 5
XP_GROWTH = 1.4
PICKUP_RADIUS = 80
