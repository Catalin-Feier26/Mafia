import pygame

def draw_button(screen, text, font, button_color, button_hover_color, text_color, x, y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    is_hovering = x <= mouse_x <= x + width and y <= mouse_y <= y + height
    color = button_hover_color if is_hovering else button_color
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=15)
    button_text = font.render(text, True, text_color)
    screen.blit(button_text, (x + (width - button_text.get_width()) // 2, y + (height - button_text.get_height()) // 2))
    return is_hovering

def draw_characters(screen, roles, statuses, images, y_offset=None):
    screen_width, screen_height = screen.get_size()
    rect_width, rect_height = 120, 150
    margin = (screen_width - (8 * rect_width)) // 9
    start_x = margin
    y = y_offset if y_offset else int(screen_height * 0.05)

    font = pygame.font.Font(None, 36)
    name_font = pygame.font.Font(None, 24)
    for i, role in enumerate(roles):
        x = start_x + i * (rect_width + margin)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, rect_width, rect_height))
        if statuses[i] == "alive":
            screen.blit(images[role], (x + 10, y + 10))
        else:
            screen.blit(images["grave"], (x + 10, y + 10))
        
        player_name_text = name_font.render(f"Player {i + 1}", True, (255, 255, 255))
        screen.blit(player_name_text, (x + (rect_width - player_name_text.get_width()) // 2, y - 30))

        index_text = font.render(f"{i + 1}", True, (255, 255, 255))
        screen.blit(index_text, (x + (rect_width - index_text.get_width()) // 2, y - 30 - index_text.get_height()))
