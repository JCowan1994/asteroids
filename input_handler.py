import pygame


class InputHandler:
    def handle_event(self, event, game_started, game_over, player):
        actions = {
            "quit": False,
            "start": False,
            "restart": False,
            "bomb_dropped": False,
        }

        if event.type == pygame.QUIT:
            actions["quit"] = True
            return actions

        if event.type != pygame.KEYDOWN:
            return actions

        if not game_started and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            actions["start"] = True
            return actions

        if game_over and event.key == pygame.K_SPACE:
            actions["restart"] = True
            return actions

        if game_started and not game_over:
            if event.key == pygame.K_1:
                player.set_weapon("single")
            elif event.key == pygame.K_2:
                player.set_weapon("spread")
            elif event.key == pygame.K_3:
                player.set_weapon("burst")
            elif event.key == pygame.K_b:
                bomb = player.drop_bomb()
                if bomb:
                    actions["bomb_dropped"] = True

        return actions
