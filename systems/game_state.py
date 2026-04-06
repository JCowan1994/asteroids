from dataclasses import dataclass


@dataclass
class GameState:
    score: int = 0
    high_score: int = 0
    lives: int = 0
    invulnerability_timer: float = 0.0
    game_over: bool = False
    game_started: bool = False
    powerup_spawn_timer: float = 0.0

    def reset_for_restart(self, starting_lives):
        self.score = 0
        self.lives = starting_lives
        self.invulnerability_timer = 0.0
        self.game_over = False
        self.game_started = False
        self.powerup_spawn_timer = 0.0
