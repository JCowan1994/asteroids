import pygame

from .circleshape import CircleShape
from constants import BOMB_RADIUS, BOMB_FUSE_SECONDS, LINE_WIDTH


class Bomb(CircleShape):
    def __init__(self, position, velocity):
        super().__init__(position.x, position.y, BOMB_RADIUS)
        self.velocity = velocity
        self.fuse_timer = BOMB_FUSE_SECONDS

    def update(self, dt):
        self.fuse_timer -= dt
        super().update(dt)

    def ready_to_explode(self):
        return self.fuse_timer <= 0

    def draw(self, screen):
        # Simple pulse as the fuse gets close to zero.
        color = "orange" if self.fuse_timer > 0.25 else "red"
        pygame.draw.circle(screen, color, self.position, self.radius, LINE_WIDTH)
