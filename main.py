import pygame, sys
import json
import os
import random
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    ASTEROID_POINTS,
    STARTING_LIVES,
    RESPAWN_INVULNERABILITY_TIME,
    POWERUP_SPAWN_RATE_SECONDS,
    BOMB_BLAST_RADIUS,
    BOMB_SHOCKWAVE_DURATION,
    BOMB_PICKUP_AMOUNT,
)
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from explosion import Explosion, Shockwave
from powerup import PowerUp
from bomb import Bomb

HIGH_SCORE_FILE = "highscore.json"

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}, Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Create animated parallax starfield (far, mid, near layers)
    star_layers = [
        {"count": 80, "speed_min": 0.2, "speed_max": 0.8, "size": 1, "brightness_min": 80, "brightness_max": 150},
        {"count": 50, "speed_min": 0.8, "speed_max": 1.6, "size": 1, "brightness_min": 140, "brightness_max": 210},
        {"count": 30, "speed_min": 1.6, "speed_max": 3.0, "size": 2, "brightness_min": 200, "brightness_max": 255},
    ]
    starfield = []
    for layer in star_layers:
        layer_stars = []
        for _ in range(layer["count"]):
            layer_stars.append(
                {
                    "x": random.randint(0, SCREEN_WIDTH),
                    "y": random.randint(0, SCREEN_HEIGHT),
                    "speed": random.uniform(layer["speed_min"], layer["speed_max"]),
                    "size": layer["size"],
                    "brightness": random.randint(layer["brightness_min"], layer["brightness_max"]),
                }
            )
        starfield.append(layer_stars)
    
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    explosions = []

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    Bomb.containers = (bombs, updatable, drawable)

    # Instantiate player at center of screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    # Scoring
    score = 0
    
    # Load high score from file
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, "r") as f:
            data = json.load(f)
            high_score = data.get("high_score", 0)
    else:
        high_score = 0
    
    # Lives
    lives = STARTING_LIVES
    invulnerability_timer = 0
    game_over = False
    powerup_spawn_timer = 0
    
    font = pygame.font.Font(None, 36)
    large_font = pygame.font.Font(None, 72)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player.set_weapon("single")
                elif event.key == pygame.K_2:
                    player.set_weapon("spread")
                elif event.key == pygame.K_3:
                    player.set_weapon("burst")
                elif event.key == pygame.K_b:
                    bomb = player.drop_bomb()
                    if bomb:
                        log_event("bomb_dropped")
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Restart game
                    score = 0
                    lives = STARTING_LIVES
                    invulnerability_timer = 0
                    game_over = False
                    # Clear all sprites and explosions
                    updatable.empty()
                    drawable.empty()
                    asteroids.empty()
                    shots.empty()
                    powerups.empty()
                    bombs.empty()
                    explosions.clear()
                    # Reset starfield positions
                    for layer_stars in starfield:
                        for star in layer_stars:
                            star["x"] = random.randint(0, SCREEN_WIDTH)
                            star["y"] = random.randint(0, SCREEN_HEIGHT)
                    
                    # Recreate game objects
                    Player.containers = (updatable, drawable)
                    Asteroid.containers = (asteroids, updatable, drawable)
                    AsteroidField.containers = (updatable,)
                    Shot.containers = (shots, updatable, drawable)
                    PowerUp.containers = (powerups, updatable, drawable)
                    Bomb.containers = (bombs, updatable, drawable)
                    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    asteroid_field = AsteroidField()
                    powerup_spawn_timer = 0
        
        if not game_over:
            updatable.update(dt)
            powerup_spawn_timer += dt
            if powerup_spawn_timer >= POWERUP_SPAWN_RATE_SECONDS:
                powerup_spawn_timer = 0
                PowerUp.spawn_random(
                    random.uniform(60, SCREEN_WIDTH - 60),
                    random.uniform(60, SCREEN_HEIGHT - 60),
                )
        if not game_over:
            # Iterate over snapshots to avoid re-processing newly spawned asteroids in the same frame.
            for asteroid in list(asteroids):
                if not asteroid.alive():
                    continue
                for shot in list(shots):
                    if not shot.alive():
                        continue
                    if asteroid.collides_with(shot):
                        log_event("asteroid_shot")
                        score += ASTEROID_POINTS
                        # Create explosion at asteroid position
                        explosions.append(Explosion(asteroid.position.copy()))
                        asteroid.split()
                        shot.kill()
                        # One shot can only hit one asteroid per frame.
                        break

            # Power-up pickup handling.
            for powerup in list(powerups):
                if player.collides_with(powerup):
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
                        score += ASTEROID_POINTS
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

            for object in asteroids:
                if object.collides_with(player) and invulnerability_timer <= 0:
                    if player.has_shield():
                        player.consume_shield()
                        explosions.append(Explosion(object.position.copy()))
                        object.kill()
                        log_event("shield_block")
                        continue
                    log_event("player_hit")
                    lives -= 1
                    if lives <= 0:
                        if score > high_score:
                            high_score = score
                            # Save high score to file
                            with open(HIGH_SCORE_FILE, "w") as f:
                                json.dump({"high_score": high_score}, f)
                        game_over = True
                    else:
                        # Respawn player
                        player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                        player.velocity = pygame.Vector2(0, 0)
                        invulnerability_timer = RESPAWN_INVULNERABILITY_TIME
        else:
            # During game over, don't update game state
            pass
        screen.fill("black")
        
        # Draw animated starfield background
        for layer_stars in starfield:
            for star in layer_stars:
                star["y"] += star["speed"]
                if star["y"] > SCREEN_HEIGHT:
                    star["y"] = 0
                    star["x"] = random.randint(0, SCREEN_WIDTH)
                pygame.draw.circle(
                    screen,
                    (star["brightness"], star["brightness"], star["brightness"]),
                    (int(star["x"]), int(star["y"])),
                    star["size"],
                )
        
        if not game_over:
            # Blink player during invulnerability
            if invulnerability_timer <= 0 or int(invulnerability_timer * 10) % 2 == 0:
                player.draw(screen)
                if player.has_shield():
                    pygame.draw.circle(
                        screen,
                        "deepskyblue",
                        player.position,
                        int(player.radius * 1.55),
                        2,
                    )
            for sprite in drawable:
                if sprite != player:
                    sprite.draw(screen)
            
            # Update and draw explosions
            current_time = pygame.time.get_ticks() / 1000.0
            explosions = [exp for exp in explosions if exp.is_alive(current_time)]
            for explosion in explosions:
                explosion.draw(screen, current_time)
            
            # Display score, high score, and lives
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))
            high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
            screen.blit(high_score_text, (SCREEN_WIDTH - 300, 10))
            lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
            screen.blit(lives_text, (10, SCREEN_HEIGHT - 40))
            weapon_text = font.render(
                f"Weapon: {player.get_weapon_name()} (1/2/3)",
                True,
                (255, 255, 255),
            )
            screen.blit(weapon_text, (SCREEN_WIDTH - 380, SCREEN_HEIGHT - 40))
            bomb_text = font.render(f"Bombs: {player.bombs} (B)", True, (255, 255, 255))
            screen.blit(bomb_text, (10, SCREEN_HEIGHT - 75))

            if player.has_shield():
                shield_text = font.render(
                    f"Shield: {max(0.0, player.shield_timer):.1f}s",
                    True,
                    (70, 200, 255),
                )
                screen.blit(shield_text, (SCREEN_WIDTH - 280, 45))

            if player.has_speed_boost():
                speed_text = font.render(
                    f"Speed Boost: {max(0.0, player.speed_boost_timer):.1f}s",
                    True,
                    (120, 255, 120),
                )
                screen.blit(speed_text, (SCREEN_WIDTH - 330, 75))
            
            # Decrease invulnerability timer
            invulnerability_timer -= dt
        else:
            # Display game over screen
            game_over_text = large_font.render("Game Over!", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            screen.blit(game_over_text, game_over_rect)
            
            score_display_text = font.render(f"Score: {score}", True, (255, 255, 255))
            score_display_rect = score_display_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(score_display_text, score_display_rect)
            
            high_score_display_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
            high_score_display_rect = high_score_display_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            screen.blit(high_score_display_text, high_score_display_rect)
            
            restart_text = font.render("Press SPACE to Play Again", True, (255, 255, 0))
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
            screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Limit to 60 FPS and convert to seconds
        

if __name__ == "__main__":
    main()
