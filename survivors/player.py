import pygame
from . import settings as S


class Player:
    def __init__(self):
        self.pos = pygame.Vector2(0, 0)
        self.hp = S.PLAYER_MAX_HP
        self.max_hp = S.PLAYER_MAX_HP
        self.speed = S.PLAYER_SPEED
        self.radius = S.PLAYER_RADIUS
        self.invuln = 0.0
        self.pickup_radius = S.PICKUP_RADIUS
        self.level = 1
        self.xp = 0
        self.xp_needed = S.XP_BASE

    def update(self, dt, keys):
        direction = pygame.Vector2(
            keys[pygame.K_d] - keys[pygame.K_a] + keys[pygame.K_RIGHT] - keys[pygame.K_LEFT],
            keys[pygame.K_s] - keys[pygame.K_w] + keys[pygame.K_DOWN] - keys[pygame.K_UP],
        )
        if direction.length_squared() > 0:
            # normalize evita andar mais rápido na diagonal
            self.pos += direction.normalize() * self.speed * dt
        self.invuln = max(0.0, self.invuln - dt)

    def take_damage(self, amount):
        if self.invuln > 0:
            return
        self.hp -= amount
        self.invuln = S.INVULN_TIME

    def add_xp(self, amount):
        """Devolve True se subiu de nível."""
        self.xp += amount
        if self.xp >= self.xp_needed:
            self.xp -= self.xp_needed
            self.level += 1
            self.xp_needed = int(self.xp_needed * S.XP_GROWTH) + 1
            return True
        return False

    @property
    def alive(self):
        return self.hp > 0

    def draw(self, screen, camera):
        center = self.pos - camera
        # pisca enquanto invulnerável
        if self.invuln > 0 and int(self.invuln * 20) % 2 == 0:
            return
        pygame.draw.circle(screen, S.BLUE, center, self.radius)
        pygame.draw.circle(screen, S.WHITE, center, self.radius, 2)
