import math

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


class OrbitingKnives:
    """Facas que giram à volta do jogador e ferem tudo o que tocam."""

    def __init__(self):
        self.count = 0           # começa sem facas; ganha-se ao subir de nível
        self.radius = 90         # distância ao jogador
        self.spin_speed = 3.0    # radianos por segundo
        self.damage = 6
        self.knife_radius = 8
        self.hit_delay = 0.4     # segundos até a mesma faca ferir o mesmo inimigo outra vez
        self.angle = 0.0
        self._last_hit = {}      # inimigo -> tempo restante até poder ser ferido outra vez

    def positions(self, player):
        """Posição de cada faca, espalhadas em partes iguais do círculo (tau = 2*pi)."""
        result = []
        for i in range(self.count):
            a = self.angle + i * math.tau / self.count
            offset = pygame.Vector2(math.cos(a), math.sin(a)) * self.radius
            result.append(player.pos + offset)
        return result

    def update(self, dt, player, enemies):
        self.angle += self.spin_speed * dt
        # reduz os temporizadores e esquece os que já acabaram
        self._last_hit = {e: t - dt for e, t in self._last_hit.items() if t - dt > 0}
        for knife_pos in self.positions(player):
            for e in enemies:
                if e in self._last_hit:
                    continue
                if knife_pos.distance_to(e.pos) < self.knife_radius + e.radius:
                    e.hp -= self.damage
                    self._last_hit[e] = self.hit_delay

    def draw(self, screen, camera, player):
        for pos in self.positions(player):
            pygame.draw.circle(screen, S.YELLOW, pos - camera, self.knife_radius)
            pygame.draw.circle(screen, S.WHITE, pos - camera, self.knife_radius, 2)
