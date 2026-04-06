import random

from constants import POWERUP_SPAWN_RATE_SECONDS, SCREEN_HEIGHT, SCREEN_WIDTH
from objects.powerup import PowerUp


def update_powerup_spawns(dt, state):
    state.powerup_spawn_timer += dt
    if state.powerup_spawn_timer < POWERUP_SPAWN_RATE_SECONDS:
        return

    state.powerup_spawn_timer = 0.0
    PowerUp.spawn_random(
        random.uniform(60, SCREEN_WIDTH - 60),
        random.uniform(60, SCREEN_HEIGHT - 60),
    )
