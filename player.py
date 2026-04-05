import circleshape
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_ACCELERATION, PLAYER_MAX_SPEED, PLAYER_FRICTION, LINE_WIDTH, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
import pygame
from shot import Shot

class Player(circleshape.CircleShape):
    def __init__ (self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_cooldown = 0

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

    def accelerate(self, dt):
        # Get forward direction based on rotation
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # Apply acceleration in forward direction
        self.velocity += forward * PLAYER_ACCELERATION * dt
        # Cap the speed
        if self.velocity.length() > PLAYER_MAX_SPEED:
            self.velocity = self.velocity.normalize() * PLAYER_MAX_SPEED
    
    def apply_friction(self, dt):
        # Apply friction (gradual slowdown when not accelerating)
        self.velocity *= PLAYER_FRICTION
    
    def shoot(self):
        unit_vector = pygame.Vector2(0,1)
        rotated_vector = unit_vector.rotate(self.rotation)
        velocity = rotated_vector * PLAYER_SHOOT_SPEED
        return Shot(self.position, velocity)

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.accelerate(dt)

        if keys[pygame.K_s]:
            # Accelerate backward
            forward = pygame.Vector2(0, 1).rotate(self.rotation)
            self.velocity -= forward * PLAYER_ACCELERATION * dt
            if self.velocity.length() > PLAYER_MAX_SPEED:
                self.velocity = self.velocity.normalize() * PLAYER_MAX_SPEED

        # Apply friction every frame
        self.apply_friction(dt)

        if keys[pygame.K_SPACE]:
            if self.shoot_cooldown <= 0:
                self.shoot()
                self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

        self.shoot_cooldown -= dt
        
        # Apply movement based on velocity
        super().update(dt)
