def update_effects(effects, current_time):
    return [effect for effect in effects if effect.is_alive(current_time)]


def draw_effects(screen, effects, current_time):
    for effect in effects:
        effect.draw(screen, current_time)
