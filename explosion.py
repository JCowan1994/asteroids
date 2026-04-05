import pygame
from constants import EXPLOSION_DURATION, EXPLOSION_MAX_RADIUS

class Explosion:
    def __init__(self, position):
        self.position = position
        self.creation_time = pygame.time.get_ticks() / 1000.0
    
    def is_alive(self, current_time):
        return current_time - self.creation_time < EXPLOSION_DURATION
    
    def draw(self, screen, current_time):
        elapsed = current_time - self.creation_time
        progress = elapsed / EXPLOSION_DURATION
        
        # Calculate expanding ring radius
        radius = int(progress * EXPLOSION_MAX_RADIUS)
        
        # Calculate opacity (fades out over time)
        opacity = int(255 * (1 - progress))
        
        # Create a surface for the ring
        ring_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        
        # Draw the ring (circle outline)
        if radius > 0:
            pygame.draw.circle(ring_surface, (255, 255, 255, opacity), (radius, radius), radius, 3)
        
        # Blit to screen
        top_left = (self.position.x - radius, self.position.y - radius)
        screen.blit(ring_surface, top_left)
