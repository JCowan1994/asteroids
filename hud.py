import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class HudRenderer:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)

    def draw_gameplay(self, screen, score, high_score, lives, player):
        score_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        high_score_text = self.font.render(f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(high_score_text, (SCREEN_WIDTH - 300, 10))

        lives_text = self.font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(lives_text, (10, SCREEN_HEIGHT - 40))

        weapon_text = self.font.render(
            f"Weapon: {player.get_weapon_name()} (1/2/3)",
            True,
            (255, 255, 255),
        )
        screen.blit(weapon_text, (SCREEN_WIDTH - 380, SCREEN_HEIGHT - 40))

        bomb_text = self.font.render(f"Bombs: {player.bombs} (B)", True, (255, 255, 255))
        screen.blit(bomb_text, (10, SCREEN_HEIGHT - 75))

        if player.has_shield():
            shield_text = self.font.render(
                f"Shield: {max(0.0, player.shield_timer):.1f}s",
                True,
                (70, 200, 255),
            )
            screen.blit(shield_text, (SCREEN_WIDTH - 280, 45))

        if player.has_speed_boost():
            speed_text = self.font.render(
                f"Speed Boost: {max(0.0, player.speed_boost_timer):.1f}s",
                True,
                (120, 255, 120),
            )
            screen.blit(speed_text, (SCREEN_WIDTH - 330, 75))

    def draw_start_screen(self, screen, high_score):
        title_text = self.large_font.render("Asteroids", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140))
        screen.blit(title_text, title_rect)

        prompt_text = self.font.render("Press ENTER to Start", True, (255, 255, 0))
        prompt_rect = prompt_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 55))
        screen.blit(prompt_text, prompt_rect)

        controls_1 = self.font.render("Move: W/S  Rotate: A/D  Shoot: SPACE", True, (220, 220, 220))
        controls_1_rect = controls_1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        screen.blit(controls_1, controls_1_rect)

        controls_2 = self.font.render("Weapons: 1/2/3  Drop Bomb: B", True, (220, 220, 220))
        controls_2_rect = controls_2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 45))
        screen.blit(controls_2, controls_2_rect)

        high_score_text = self.font.render(f"High Score: {high_score}", True, (180, 255, 180))
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 95))
        screen.blit(high_score_text, high_score_rect)

    def draw_game_over(self, screen, score, high_score):
        game_over_text = self.large_font.render("Game Over!", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        screen.blit(game_over_text, game_over_rect)

        score_display_text = self.font.render(f"Score: {score}", True, (255, 255, 255))
        score_display_rect = score_display_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(score_display_text, score_display_rect)

        high_score_display_text = self.font.render(f"High Score: {high_score}", True, (255, 255, 255))
        high_score_display_rect = high_score_display_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(high_score_display_text, high_score_display_rect)

        restart_text = self.font.render("Press SPACE to Play Again", True, (255, 255, 0))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        screen.blit(restart_text, restart_rect)
