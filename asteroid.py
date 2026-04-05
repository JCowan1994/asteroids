from circleshape import CircleShape
import pygame
from logger import log_event
import random
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        new_vel1 = self.velocity.rotate(angle)
        new_vel2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        if new_radius > 0:
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = new_vel1 * 1.2
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2.velocity = new_vel2 * 1.2
        

