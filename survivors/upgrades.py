"""Melhorias disponíveis ao subir de nível. Cada uma é (nome, função que aplica)."""
import random


def _damage(player, weapon):
    weapon.damage *= 1.25


def _speed_fire(player, weapon):
    weapon.cooldown = max(0.15, weapon.cooldown * 0.85)


def _multishot(player, weapon):
    weapon.count += 1


def _hp(player, weapon):
    player.max_hp += 25
    player.hp = min(player.max_hp, player.hp + 40)


def _move(player, weapon):
    player.speed *= 1.1


def _magnet(player, weapon):
    player.pickup_radius *= 1.4


UPGRADES = [
    ("+25% dano", _damage),
    ("+15% cadência de tiro", _speed_fire),
    ("+1 projétil", _multishot),
    ("+25 vida máx. (e cura)", _hp),
    ("+10% velocidade", _move),
    ("+40% alcance do íman", _magnet),
]


def random_choices(n=3):
    return random.sample(UPGRADES, n)
