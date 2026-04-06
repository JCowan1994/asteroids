import random

import pygame

from .circleshape import CircleShape
from constants import POWERUP_RADIUS, POWERUP_DRIFT_SPEED, LINE_WIDTH


class PowerUp(CircleShape):
    def __init__(self, x, y, kind):
        super().__init__(x, y, POWERUP_RADIUS)
        self.kind = kind
        self.velocity = pygame.Vector2(
            random.uniform(-1, 1), random.uniform(-1, 1)
        )
        if self.velocity.length_squared() == 0:
            self.velocity = pygame.Vector2(0, 1)
        self.velocity = self.velocity.normalize() * POWERUP_DRIFT_SPEED

    @classmethod
    def spawn_random(cls, x, y):
        kind = random.choice(["shield", "speed", "bomb"])
        return cls(x, y, kind)

    def draw(self, screen):
        if self.kind == "shield":
            color = "deepskyblue"
        elif self.kind == "speed":
            color = "limegreen"
        else:
            color = "orange"
        pygame.draw.circle(screen, color, self.position, self.radius, LINE_WIDTH)

        if self.kind == "shield":
            # Shield icon: inner ring + small badge triangle.
            pygame.draw.circle(
                screen,
                color,
                self.position,
                int(self.radius * 0.55),
                2,
            )
            tip = self.position + pygame.Vector2(0, self.radius * 0.45)
            left = self.position + pygame.Vector2(-self.radius * 0.3, self.radius * 0.05)
            right = self.position + pygame.Vector2(self.radius * 0.3, self.radius * 0.05)
            pygame.draw.polygon(screen, color, [tip, right, left], 0)
        elif self.kind == "speed":
            # Speed icon: lightning bolt.
            s = self.radius * 0.6
            p1 = self.position + pygame.Vector2(-0.15 * s, -1.0 * s)
            p2 = self.position + pygame.Vector2(0.5 * s, -0.2 * s)
            p3 = self.position + pygame.Vector2(0.05 * s, -0.2 * s)
            p4 = self.position + pygame.Vector2(0.35 * s, 1.0 * s)
            p5 = self.position + pygame.Vector2(-0.45 * s, 0.05 * s)
            p6 = self.position + pygame.Vector2(-0.05 * s, 0.05 * s)
            pygame.draw.polygon(screen, color, [p1, p2, p3, p4, p5, p6], 0)
        else:
            # Bomb icon: core + short fuse.
            pygame.draw.circle(screen, color, self.position, int(self.radius * 0.45), 0)
            fuse_start = self.position + pygame.Vector2(self.radius * 0.1, -self.radius * 0.45)
            fuse_end = fuse_start + pygame.Vector2(self.radius * 0.45, -self.radius * 0.3)
            pygame.draw.line(screen, color, fuse_start, fuse_end, 2)
            pygame.draw.circle(screen, "yellow", fuse_end, 2, 0)
