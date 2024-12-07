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
    horizontal_spacing = 9
    margin = (screen_width - (8 * rect_width)) // horizontal_spacing
    start_x = margin
    y = y_offset if y_offset else int(screen_height * 0.05)

    font = pygame.font.Font(None, 36)
    name_font = pygame.font.Font(None, 24)
    
    for i, role in enumerate(roles):
        x = start_x + i * (rect_width + margin)
        image_key = role if statuses[i] == "alive" else "grave"
        screen.blit(images[image_key], (x + 10, y + 10))
        
        # Render player name
        player_name_text = name_font.render(f"Player {i + 1}", True, (255, 255, 255))
        name_x = x + (rect_width - player_name_text.get_width()) // 2
        screen.blit(player_name_text, (name_x, y - 30))
        
        # Render player index
        index_text = font.render(f"{i + 1}", True, (255, 255, 255))
        index_x = x + (rect_width - index_text.get_width()) // 2
        screen.blit(index_text, (index_x, y - 30 - index_text.get_height()))
        
        # Optionally add player role
        role_text = name_font.render(role, True, (255, 255, 255))
        role_x = x + (rect_width - role_text.get_width()) // 2
        screen.blit(role_text, (role_x, y + rect_height - 20))


def display_elimination_summary(screen, roles, statuses, votes, images):
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 36)

    while True:
        screen.fill((50, 50, 100))  # Clear the screen with the background color
        screen_width, screen_height = screen.get_size()

        summary_text = font.render("Elimination Summary", True, (255, 255, 255))
        screen.blit(summary_text, ((screen_width - summary_text.get_width()) // 2, int(screen_height * 0.05)))

        # Adjust the Y offset for the characters and the elimination message
        adjusted_y_offset = int(screen_height * 0.2)

        if len(votes) > 0:
            # Tally votes
            vote_count = {}
            for vote in votes.values():
                if vote is not None:
                    vote_count[vote] = vote_count.get(vote, 0) + 1

            most_votes = max(vote_count.values(), default=0)
            potential_killers = [player for player, count in vote_count.items() if count == most_votes]

            if len(potential_killers) == 1:
                eliminated_player = potential_killers[0]
                eliminated_name = f"Player {eliminated_player + 1}"
                elimination_message = f"{eliminated_name} was eliminated with {most_votes} votes."
                statuses[eliminated_player] = "dead"
            else:
                elimination_message = "No one was eliminated."

            # Display the elimination message
            elimination_text = small_font.render(elimination_message, True, (255, 255, 255))
            screen.blit(elimination_text, ((screen_width - elimination_text.get_width()) // 2, adjusted_y_offset))

        # Draw characters with updated statuses
        draw_characters(screen, roles, statuses, images, adjusted_y_offset + 80)

        # Continue button
        button_width, button_height = 200, 80
        button_x = (screen_width - button_width) // 2
        button_y = int(screen_height * 0.85)
        is_hovering = draw_button(screen, "Continue", font, (100, 200, 100), (80, 180, 80), (255, 255, 255), button_x, button_y, button_width, button_height)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and is_hovering:
                return  # Exit the function when the button is clicked

        pygame.display.flip()  # Update the display

def display_game_over_screen(screen, message):
    font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 50)
    screen.fill((50, 50, 100))
    
    # Display game over message
    text = font.render(message, True, (255, 255, 255))
    screen_width, screen_height = screen.get_size()
    screen.blit(text, ((screen_width - text.get_width()) // 2, screen_height // 3))

    # Button properties
    button_width, button_height = 200, 80
    button_x = (screen_width - button_width) // 2
    button_y = int(screen_height * 0.7)

    pygame.display.flip()

    # Wait for the player to click the continue button
    while True:
        screen.fill((50, 50, 100))  # Redraw background
        screen.blit(text, ((screen_width - text.get_width()) // 2, screen_height // 3))  # Redraw message
        
        # Draw the button using draw_button
        button_hovering = draw_button(
            screen,
            "Continue",
            button_font,
            (100, 200, 100),   # Button color
            (120, 220, 120),   # Hover color
            (255, 255, 255),   # Text color
            button_x,
            button_y,
            button_width,
            button_height
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_hovering:
                    pygame.quit;
                    exit();
                    return 