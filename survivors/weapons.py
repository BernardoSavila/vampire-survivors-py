import pygame
from . import settings as S


class Projectile:
    def __init__(self, pos, direction, damage):
        self.pos = pygame.Vector2(pos)
        self.vel = direction * S.PROJECTILE_SPEED
        self.damage = damage
        self.radius = 5
        self.life = S.PROJECTILE_LIFETIME

    def update(self, dt):
        self.pos += self.vel * dt
        self.life -= dt

    def draw(self, screen, camera):
        pygame.draw.circle(screen, S.WHITE, self.pos - camera, self.radius)


class Weapon:
    """Dispara automaticamente no inimigo mais próximo (como no Vampire Survivors)."""

    def __init__(self):
        self.cooldown = S.WEAPON_COOLDOWN
        self.damage = S.PROJECTILE_DAMAGE
        self.count = 1  # projéteis por disparo
        self.timer = 0.0

    def update(self, dt, player, enemies, projectiles):
        self.timer -= dt
        if self.timer > 0 or not enemies:
            return
        self.timer = self.cooldown
        # min com key= devolve o inimigo com menor distância
        target = min(enemies, key=lambda e: player.pos.distance_squared_to(e.pos))
        base = (target.pos - player.pos)
        if base.length_squared() == 0:
            return
        base = base.normalize()
        # espalha os projéteis em leque
        spread = 12
        start = -spread * (self.count - 1) / 2
        for i in range(self.count):
            direction = base.rotate(start + i * spread)
            projectiles.append(Projectile(player.pos, direction, self.damage))
