import math
import random
import sys

import pygame

from . import settings as S
from .enemy import Enemy, XPGem
from .player import Player
from .upgrades import random_choices
from .weapons import OrbitingKnives, Weapon


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Survivors")
        self.screen = pygame.display.set_mode((S.WIDTH, S.HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 64)
        self.reset()

    def reset(self):
        self.player = Player()
        self.weapon = Weapon()
        self.knives = OrbitingKnives()
        self.enemies = []
        self.projectiles = []
        self.gems = []
        self.spawn_timer = 0.0
        self.time = 0.0
        self.kills = 0
        self.state = "playing"  # playing | levelup | gameover
        self.choices = []

    # ---------- loop principal ----------
    def run(self):
        while True:
            dt = min(self.clock.tick(S.FPS) / 1000, 0.05)  # limita dt para evitar saltos
            self.handle_events()
            if self.state == "playing":
                self.update(dt)
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.state == "levelup" and event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    _, apply = self.choices[event.key - pygame.K_1]
                    apply(self)
                    self.state = "playing"
                elif self.state == "gameover" and event.key == pygame.K_r:
                    self.reset()

    # ---------- lógica ----------
    def update(self, dt):
        self.time += dt
        self.player.update(dt, pygame.key.get_pressed())
        self.spawn_enemies(dt)

        for e in self.enemies:
            e.update(dt, self.player.pos)
        self.weapon.update(dt, self.player, self.enemies, self.projectiles)
        self.knives.update(dt, self.player, self.enemies)
        for p in self.projectiles:
            p.update(dt)
        for g in self.gems:
            g.update(dt, self.player)

        self.handle_collisions()
        self.projectiles = [p for p in self.projectiles if p.life > 0]

        if not self.player.alive:
            self.state = "gameover"

    def spawn_enemies(self, dt):
        self.spawn_timer -= dt
        if self.spawn_timer > 0:
            return
        # quanto mais tempo passa, mais rápido nascem inimigos
        interval = max(S.SPAWN_INTERVAL_MIN, S.SPAWN_INTERVAL_START - self.time / 120)
        self.spawn_timer = interval
        angle = random.uniform(0, math.tau)
        distance = max(S.WIDTH, S.HEIGHT) * 0.65  # fora do ecrã
        pos = self.player.pos + pygame.Vector2(math.cos(angle), math.sin(angle)) * distance
        kind = "zombie" if random.random() < min(0.4, self.time / 300) else "bat"
        hp_scale = 1 + self.time / 90
        self.enemies.append(Enemy(kind, pos, hp_scale))

    def handle_collisions(self):
        # projéteis vs inimigos
        for p in self.projectiles:
            for e in self.enemies:
                if p.pos.distance_to(e.pos) < p.radius + e.radius:
                    e.hp -= p.damage
                    p.life = 0
                    break

        # inimigos mortos largam gemas
        survivors = []
        for e in self.enemies:
            if e.hp <= 0:
                self.kills += 1
                self.gems.append(XPGem(e.pos, e.xp))
            else:
                survivors.append(e)
        self.enemies = survivors

        # inimigos vs jogador
        for e in self.enemies:
            if e.pos.distance_to(self.player.pos) < e.radius + self.player.radius:
                self.player.take_damage(e.damage)

        # jogador apanha gemas
        remaining = []
        for g in self.gems:
            if g.pos.distance_to(self.player.pos) < g.radius + self.player.radius:
                if self.player.add_xp(g.value):
                    self.choices = random_choices(3)
                    self.state = "levelup"
            else:
                remaining.append(g)
        self.gems = remaining

    # ---------- desenho ----------
    def draw(self):
        self.screen.fill(S.BG)
        camera = self.player.pos - pygame.Vector2(S.WIDTH / 2, S.HEIGHT / 2)
        self.draw_grid(camera)

        for g in self.gems:
            g.draw(self.screen, camera)
        for e in self.enemies:
            e.draw(self.screen, camera)
        for p in self.projectiles:
            p.draw(self.screen, camera)
        self.knives.draw(self.screen, camera, self.player)
        self.player.draw(self.screen, camera)

        self.draw_hud()
        if self.state == "levelup":
            self.draw_levelup()
        elif self.state == "gameover":
            self.draw_gameover()
        pygame.display.flip()

    def draw_grid(self, camera, size=64):
        """Grelha que se move com a câmara para dar sensação de mundo infinito."""
        ox, oy = -camera.x % size, -camera.y % size
        for x in range(int(ox), S.WIDTH, size):
            pygame.draw.line(self.screen, S.GRID, (x, 0), (x, S.HEIGHT))
        for y in range(int(oy), S.HEIGHT, size):
            pygame.draw.line(self.screen, S.GRID, (0, y), (S.WIDTH, y))

    def draw_hud(self):
        # barra de XP no topo
        pygame.draw.rect(self.screen, (50, 50, 60), (0, 0, S.WIDTH, 14))
        fill = S.WIDTH * self.player.xp / self.player.xp_needed
        pygame.draw.rect(self.screen, S.YELLOW, (0, 0, fill, 14))
        # barra de vida
        pygame.draw.rect(self.screen, (60, 30, 30), (20, 30, 200, 18))
        hp_w = 200 * max(0, self.player.hp) / self.player.max_hp
        pygame.draw.rect(self.screen, S.RED, (20, 30, hp_w, 18))
        minutes, seconds = divmod(int(self.time), 60)
        text = f"Nível {self.player.level}   Kills {self.kills}   {minutes:02d}:{seconds:02d}"
        self.screen.blit(self.font.render(text, True, S.WHITE), (20, 56))

    def overlay(self):
        shade = pygame.Surface((S.WIDTH, S.HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 170))
        self.screen.blit(shade, (0, 0))

    def center_text(self, text, y, font=None, color=S.WHITE):
        surf = (font or self.font).render(text, True, color)
        self.screen.blit(surf, surf.get_rect(center=(S.WIDTH // 2, y)))

    def draw_levelup(self):
        self.overlay()
        self.center_text("SUBISTE DE NÍVEL!", 200, self.big_font, S.YELLOW)
        for i, (name, _) in enumerate(self.choices):
            self.center_text(f"[{i + 1}]  {name}", 320 + i * 60)

    def draw_gameover(self):
        self.overlay()
        self.center_text("GAME OVER", 260, self.big_font, S.RED)
        self.center_text(f"Sobreviveste {int(self.time)}s  |  {self.kills} kills", 330)
        self.center_text("R para recomeçar  |  ESC para sair", 390)
