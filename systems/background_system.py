import random

import pygame

from constants import SCREEN_HEIGHT, SCREEN_WIDTH


def create_starfield():
    # Create animated parallax starfield (far, mid, near layers)
    star_layers = [
        {"count": 80, "speed_min": 0.2, "speed_max": 0.8, "size": 1, "brightness_min": 80, "brightness_max": 150},
        {"count": 50, "speed_min": 0.8, "speed_max": 1.6, "size": 1, "brightness_min": 140, "brightness_max": 210},
        {"count": 30, "speed_min": 1.6, "speed_max": 3.0, "size": 2, "brightness_min": 200, "brightness_max": 255},
    ]

    starfield = []
    for layer in star_layers:
        layer_stars = []
        for _ in range(layer["count"]):
            layer_stars.append(
                {
                    "x": random.randint(0, SCREEN_WIDTH),
                    "y": random.randint(0, SCREEN_HEIGHT),
                    "speed": random.uniform(layer["speed_min"], layer["speed_max"]),
                    "size": layer["size"],
                    "brightness": random.randint(layer["brightness_min"], layer["brightness_max"]),
                }
            )
        starfield.append(layer_stars)

    return starfield


def reset_starfield_positions(starfield):
    for layer_stars in starfield:
        for star in layer_stars:
            star["x"] = random.randint(0, SCREEN_WIDTH)
            star["y"] = random.randint(0, SCREEN_HEIGHT)


def draw_starfield(screen, starfield):
    for layer_stars in starfield:
        for star in layer_stars:
            star["y"] += star["speed"]
            if star["y"] > SCREEN_HEIGHT:
                star["y"] = 0
                star["x"] = random.randint(0, SCREEN_WIDTH)
            pygame.draw.circle(
                screen,
                (star["brightness"], star["brightness"], star["brightness"]),
                (int(star["x"]), int(star["y"])),
                star["size"],
            )
