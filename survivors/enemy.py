import pygame
from . import settings as S


class Enemy:
    def __init__(self, kind, pos, hp_scale=1.0):
        stats = S.ENEMY_TYPES[kind]
        self.pos = pygame.Vector2(pos)
        self.hp = stats["hp"] * hp_scale
        self.speed = stats["speed"]
        self.damage = stats["damage"]
        self.radius = stats["radius"]
        self.color = stats["color"]
        self.xp = stats["xp"]

    def update(self, dt, target_pos):
        direction = target_pos - self.pos
        if direction.length_squared() > 0:
            self.pos += direction.normalize() * self.speed * dt

    def draw(self, screen, camera):
        pygame.draw.circle(screen, self.color, self.pos - camera, self.radius)


class XPGem:
    def __init__(self, pos, value):
        self.pos = pygame.Vector2(pos)
        self.value = value
        self.radius = 5

    def update(self, dt, player):
        """Gemas perto do jogador são atraídas por ele (efeito íman)."""
        to_player = player.pos - self.pos
        if to_player.length() < player.pickup_radius:
            self.pos += to_player.normalize() * 350 * dt if to_player.length_squared() else 0

    def draw(self, screen, camera):
        pygame.draw.circle(screen, S.YELLOW, self.pos - camera, self.radius)
