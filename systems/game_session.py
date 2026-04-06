import json
import os

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from objects.asteroid import Asteroid
from objects.asteroidfield import AsteroidField
from objects.bomb import Bomb
from objects.player import Player
from objects.powerup import PowerUp
from objects.shot import Shot


def load_high_score(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            return data.get("high_score", 0)
    return 0


def save_high_score(file_path, score):
    with open(file_path, "w") as f:
        json.dump({"high_score": score}, f)


def create_groups():
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    return updatable, drawable, asteroids, shots, powerups, bombs


def setup_containers(updatable, drawable, asteroids, shots, powerups, bombs):
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    Bomb.containers = (bombs, updatable, drawable)


def create_world(updatable, drawable, asteroids, shots, powerups, bombs):
    setup_containers(updatable, drawable, asteroids, shots, powerups, bombs)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    return player, asteroid_field


def reset_world(updatable, drawable, asteroids, shots, powerups, bombs, explosions):
    updatable.empty()
    drawable.empty()
    asteroids.empty()
    shots.empty()
    powerups.empty()
    bombs.empty()
    explosions.clear()
