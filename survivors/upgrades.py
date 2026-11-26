"""Melhorias disponíveis ao subir de nível. Cada uma é (nome, função que aplica).

Cada função recebe o `game` e mexe no que precisar (game.player, game.weapon, game.knives).
"""
import random


def _damage(game):
    game.weapon.damage *= 1.25


def _speed_fire(game):
    game.weapon.cooldown = max(0.15, game.weapon.cooldown * 0.85)


def _multishot(game):
    game.weapon.count += 1


def _hp(game):
    game.player.max_hp += 25
    game.player.hp = min(game.player.max_hp, game.player.hp + 40)


def _move(game):
    game.player.speed *= 1.1


def _magnet(game):
    game.player.pickup_radius *= 1.4


def _knife(game):
    game.knives.count += 1


UPGRADES = [
    
    ("+25% dano", _damage),
    ("+15% cadência de tiro", _speed_fire),
    ("+1 projétil", _multishot),
    ("+25 vida máx. (e cura)", _hp),
    ("+10% velocidade", _move),
    ("+40% alcance do íman", _magnet),
    ("+1 faca orbital", _knife),
]


def random_choices(n=3):
    return random.sample(UPGRADES, n)
