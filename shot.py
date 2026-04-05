from circleshape import CircleShape
from constants import (
    SHOT_RADIUS,
    LINE_WIDTH,
    PLAYER_SHOOT_SPEED,
    SPREAD_SHOT_ANGLE_DEGREES,
    BURST_SHOT_ANGLE_DEGREES,
    SHOT_LIFETIME_SECONDS,
)
import pygame


class Shot(CircleShape):
    def __init__(self, position, velocity):
        super().__init__(position.x, position.y, SHOT_RADIUS)
        self.velocity = velocity
        self.lifetime = SHOT_LIFETIME_SECONDS

    @classmethod
    def _spawn_at_angle(cls, position, rotation, angle_offset):
        direction = pygame.Vector2(0, 1).rotate(rotation + angle_offset)
        velocity = direction * PLAYER_SHOOT_SPEED
        cls(position, velocity)

    @classmethod
    def fire_weapon(cls, weapon_type, position, rotation):
        if weapon_type == "spread":
            cls._spawn_at_angle(position, rotation, -SPREAD_SHOT_ANGLE_DEGREES)
            cls._spawn_at_angle(position, rotation, 0)
            cls._spawn_at_angle(position, rotation, SPREAD_SHOT_ANGLE_DEGREES)
            return
        if weapon_type == "burst":
            cls._spawn_at_angle(position, rotation, -BURST_SHOT_ANGLE_DEGREES * 2)
            cls._spawn_at_angle(position, rotation, -BURST_SHOT_ANGLE_DEGREES)
            cls._spawn_at_angle(position, rotation, 0)
            cls._spawn_at_angle(position, rotation, BURST_SHOT_ANGLE_DEGREES)
            cls._spawn_at_angle(position, rotation, BURST_SHOT_ANGLE_DEGREES * 2)
            return
        cls._spawn_at_angle(position, rotation, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
            return
        super().update(dt)