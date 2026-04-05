import pygame
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    STARTING_LIVES,
)
from logger import log_state, log_event
from input_handler import InputHandler
from hud import HudRenderer
from systems.background_system import (
    create_starfield,
    reset_starfield_positions,
)
from systems.collision_system import process_collisions
from systems.game_session import (
    create_groups,
    create_world,
    load_high_score,
    reset_world,
    save_high_score,
)
from systems.game_state import GameState
from systems.render_system import render_frame
from systems.spawn_system import update_powerup_spawns

HIGH_SCORE_FILE = "highscore.json"

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}, Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    starfield = create_starfield()
    
    clock = pygame.time.Clock()
    dt = 0

    updatable, drawable, asteroids, shots, powerups, bombs = create_groups()
    explosions = []

    player, asteroid_field = create_world(
        updatable, drawable, asteroids, shots, powerups, bombs
    )

    state = GameState(
        high_score=load_high_score(HIGH_SCORE_FILE),
        lives=STARTING_LIVES,
    )
    
    input_handler = InputHandler()
    hud = HudRenderer()

    while True:
        log_state()
        for event in pygame.event.get():
            actions = input_handler.handle_event(
                event,
                state.game_started,
                state.game_over,
                player,
            )

            if actions["quit"]:
                return

            if actions["start"]:
                state.game_started = True
                log_event("game_started")

            if actions["bomb_dropped"]:
                log_event("bomb_dropped")

            if actions["restart"]:
                # Restart game
                state.reset_for_restart(STARTING_LIVES)
                reset_world(
                    updatable,
                    drawable,
                    asteroids,
                    shots,
                    powerups,
                    bombs,
                    explosions,
                )
                reset_starfield_positions(starfield)
                player, asteroid_field = create_world(
                    updatable, drawable, asteroids, shots, powerups, bombs
                )

        is_playing = state.game_started and not state.game_over

        if is_playing:
            updatable.update(dt)
            update_powerup_spawns(dt, state)

        if is_playing:
            was_game_over = state.game_over
            process_collisions(
                asteroids,
                shots,
                powerups,
                bombs,
                player,
                explosions,
                state,
            )

            if not was_game_over and state.game_over and state.score > state.high_score:
                state.high_score = state.score
                save_high_score(HIGH_SCORE_FILE, state.high_score)
        explosions = render_frame(
            screen,
            starfield,
            drawable,
            player,
            hud,
            state,
            explosions,
            dt,
        )
        dt = clock.tick(60) / 1000  # Limit to 60 FPS and convert to seconds
        

if __name__ == "__main__":
    main()
