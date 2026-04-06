import pygame

from constants import (
    ASTEROID_POINTS,
    BOMB_BLAST_RADIUS,
    BOMB_PICKUP_AMOUNT,
    BOMB_SHOCKWAVE_DURATION,
    RESPAWN_INVULNERABILITY_TIME,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from explosion import Explosion, Shockwave
from logger import log_event


def process_collisions(
    asteroids,
    shots,
    powerups,
    bombs,
    player,
    explosions,
    state,
):
    # Shot -> asteroid collisions.
    for asteroid in list(asteroids):
        if not asteroid.alive():
            continue
        for shot in list(shots):
            if not shot.alive():
                continue
            if asteroid.collides_with(shot):
                log_event("asteroid_shot")
                state.score += ASTEROID_POINTS
                explosions.append(Explosion(asteroid.position.copy()))
                asteroid.split()
                shot.kill()
                break

    # Power-up pickups.
    for powerup in list(powerups):
        if not player.collides_with(powerup):
            continue

        if powerup.kind == "shield":
            player.activate_shield()
            log_event("powerup_shield")
        elif powerup.kind == "speed":
            player.activate_speed_boost()
            log_event("powerup_speed")
        else:
            player.bombs += BOMB_PICKUP_AMOUNT
            log_event("powerup_bomb", amount=BOMB_PICKUP_AMOUNT)
        powerup.kill()

    # Bomb explosion handling.
    for bomb in list(bombs):
        if not bomb.ready_to_explode():
            continue

        destroyed = 0
        for asteroid in list(asteroids):
            if (asteroid.position - bomb.position).length() <= BOMB_BLAST_RADIUS + asteroid.radius:
                explosions.append(Explosion(asteroid.position.copy()))
                asteroid.kill()
                state.score += ASTEROID_POINTS
                destroyed += 1

        explosions.append(Explosion(bomb.position.copy()))
        explosions.append(
            Shockwave(
                bomb.position.copy(),
                BOMB_BLAST_RADIUS,
                BOMB_SHOCKWAVE_DURATION,
                color=(255, 180, 80),
                width=2,
            )
        )
        bomb.kill()
        log_event("bomb_exploded", destroyed=destroyed)

    # Asteroid -> player collisions.
    for asteroid in asteroids:
        if not asteroid.collides_with(player) or state.invulnerability_timer > 0:
            continue

        if player.has_shield():
            player.consume_shield()
            explosions.append(Explosion(asteroid.position.copy()))
            asteroid.kill()
            log_event("shield_block")
            continue

        log_event("player_hit")
        state.lives -= 1
        if state.lives <= 0:
            state.game_over = True
        else:
            player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            player.velocity = pygame.Vector2(0, 0)
            state.invulnerability_timer = RESPAWN_INVULNERABILITY_TIME
