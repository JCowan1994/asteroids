import pygame

from systems.background_system import draw_starfield
from systems.effects_system import draw_effects, update_effects


def render_frame(screen, starfield, drawable, player, hud, state, effects, dt):
    screen.fill("black")
    draw_starfield(screen, starfield)

    if state.game_started and not state.game_over:
        # Blink player while invulnerable after respawn.
        if state.invulnerability_timer <= 0 or int(state.invulnerability_timer * 10) % 2 == 0:
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

        current_time = pygame.time.get_ticks() / 1000.0
        effects = update_effects(effects, current_time)
        draw_effects(screen, effects, current_time)

        hud.draw_gameplay(screen, state.score, state.high_score, state.lives, player)
        state.invulnerability_timer -= dt
    elif not state.game_started:
        hud.draw_start_screen(screen, state.high_score)
    else:
        hud.draw_game_over(screen, state.score, state.high_score)

    pygame.display.flip()
    return effects
