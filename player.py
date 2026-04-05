from triangleshape import TriangleShape
from constants import (
    PLAYER_RADIUS,
    PLAYER_TURN_SPEED,
    PLAYER_ACCELERATION,
    PLAYER_MAX_SPEED,
    PLAYER_FRICTION,
    LINE_WIDTH,
    SINGLE_SHOT_COOLDOWN_SECONDS,
    SPREAD_SHOT_COOLDOWN_SECONDS,
    BURST_SHOT_COOLDOWN_SECONDS,
    SHIELD_DURATION_SECONDS,
    SPEED_BOOST_DURATION_SECONDS,
    SPEED_BOOST_MULTIPLIER,
    PLAYER_START_BOMBS,
    BOMB_DROP_COOLDOWN_SECONDS,
)
import pygame
from shot import Shot
from bomb import Bomb

class Player(TriangleShape):
    def __init__ (self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0
        self.weapon_type = "single"
        self.shield_timer = 0
        self.speed_boost_timer = 0
        self.bombs = PLAYER_START_BOMBS
        self.bomb_cooldown = 0

    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def has_shield(self):
        return self.shield_timer > 0

    def activate_shield(self):
        self.shield_timer = SHIELD_DURATION_SECONDS

    def consume_shield(self):
        self.shield_timer = 0

    def has_speed_boost(self):
        return self.speed_boost_timer > 0

    def activate_speed_boost(self):
        self.speed_boost_timer = SPEED_BOOST_DURATION_SECONDS

    def get_current_max_speed(self):
        if self.has_speed_boost():
            return PLAYER_MAX_SPEED * SPEED_BOOST_MULTIPLIER
        return PLAYER_MAX_SPEED

    def can_drop_bomb(self):
        return self.bombs > 0 and self.bomb_cooldown <= 0

    def drop_bomb(self):
        if not self.can_drop_bomb():
            return None
        self.bombs -= 1
        self.bomb_cooldown = BOMB_DROP_COOLDOWN_SECONDS
        return Bomb(self.position.copy(), self.velocity * 0.4)

    def accelerate(self, dt):
        # Get forward direction based on rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # Apply acceleration in forward direction
        self.velocity += forward * PLAYER_ACCELERATION * dt
        # Cap the speed
        max_speed = self.get_current_max_speed()
        if self.velocity.length() > max_speed:
            self.velocity = self.velocity.normalize() * max_speed
    
    def apply_friction(self, dt):
        # Frame-time damping so coasting slows consistently across frame rates.
        damping = max(0.0, 1.0 - PLAYER_FRICTION * dt)
        self.velocity *= damping

    def set_weapon(self, weapon_type):
        if weapon_type in ("single", "spread", "burst"):
            self.weapon_type = weapon_type

    def get_weapon_name(self):
        return self.weapon_type.capitalize()

    def get_weapon_cooldown(self):
        if self.weapon_type == "spread":
            return SPREAD_SHOT_COOLDOWN_SECONDS
        if self.weapon_type == "burst":
            return BURST_SHOT_COOLDOWN_SECONDS
        return SINGLE_SHOT_COOLDOWN_SECONDS
    
    def shoot(self):
        Shot.fire_weapon(self.weapon_type, self.position, self.rotation)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        thrusting = False

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.accelerate(dt)
            thrusting = True

        if keys[pygame.K_s]:
            # Accelerate backward
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            self.velocity -= forward * PLAYER_ACCELERATION * dt
            max_speed = self.get_current_max_speed()
            if self.velocity.length() > max_speed:
                self.velocity = self.velocity.normalize() * max_speed
            thrusting = True

        # Only apply friction while coasting so acceleration feels responsive.
        if not thrusting:
            self.apply_friction(dt)

        if keys[pygame.K_SPACE]:
            if self.shoot_cooldown <= 0:
                self.shoot()
                self.shoot_cooldown = self.get_weapon_cooldown()

        self.shoot_cooldown -= dt
        self.shield_timer -= dt
        self.speed_boost_timer -= dt
        self.bomb_cooldown -= dt
        
        # Apply movement based on velocity
        super().update(dt)
