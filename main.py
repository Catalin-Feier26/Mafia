import pygame
import random
import display
from display import draw_characters
from display import draw_button

def start_pygame_interface():
    pygame.init()
    screen = pygame.display.set_mode((1340, 960))  
    pygame.display.set_caption("Mafia Game")
    
    background_color = (50, 50, 100)
    button_color = (100, 200, 100)
    text_color = (255, 255, 255)
    button_hover_color = (80, 180, 80)
    
    title_font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 50)
    
    roles = ["Civilian"] * 5 + ["Doctor", "Police", "Killer"]
    statuses = ["alive"] * len(roles)
    random.shuffle(roles)
    rect_width, rect_height = 120, 150
    images = load_scaled_images(rect_width, rect_height)
    
    running = True
    while running:
        screen.fill(background_color)
        screen_width, screen_height = screen.get_size()
        
        title_text = title_font.render("Mafia Game", True, text_color)
        screen.blit(title_text, ((screen_width - title_text.get_width()) // 2, screen_height // 4))
        
        button_width, button_height = 200, 80
        button_x = (screen_width - button_width) // 2
        button_y = screen_height // 2
        
        # Call the draw_button function
        is_hovering = draw_button(screen, "Start", button_font, button_color, button_hover_color, text_color, button_x, button_y, button_width, button_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and is_hovering:
                display_night_falls_window(screen, roles, statuses, images)
        
        pygame.display.flip()

def display_night_falls_window(screen, roles, statuses, images):
    font = pygame.font.Font(None, 80)
    small_font = pygame.font.Font(None, 36)
    running = True

    while running:
        screen.fill((50, 50, 100))
        screen_width, screen_height = screen.get_size()

        button_width, button_height = 300, 100
        button_x = (screen_width - button_width) // 2
        button_y = int(screen_height * 0.7)

        # Call the draw_button function
        is_hovering = draw_button(screen, "Night Falls", font, (100, 200, 100), (80, 180, 80), (255, 255, 255), button_x, button_y, button_width, button_height)

        draw_characters(screen, roles, statuses, images)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and is_hovering:
                start_game_window(screen, roles, statuses, images)
        
        pygame.display.flip()

def load_scaled_images(rect_width, rect_height):
    roles = ["Civilian", "Doctor", "Police", "Killer"]
    images = {}
    for role in roles:
        img = pygame.image.load(f"{role.lower()}.png")
        scaled_img = pygame.transform.scale(img, (rect_width - 20, rect_height - 50))
        images[role] = scaled_img
    images["grave"] = pygame.transform.scale(pygame.image.load("grave.png"), (rect_width - 20, rect_height - 50))
    return images

def start_game_window(screen, roles, statuses, images):
    font = pygame.font.Font(None, 40)

    while True:
        # Check for game win conditions before starting the next round
        if "Killer" not in [roles[i] for i, status in enumerate(statuses) if status == "alive"]:
            display_game_over_screen(screen, "Civilians Win")
            return
        if len([status for status in statuses if status == "alive"]) <= 1:
            display_game_over_screen(screen, "Killer Wins")
            return

        messages = [] 

        doctor_choice = game_stage_prompt(screen, roles, images, "Doctor: Who do you want to save?", font)
        messages.append(f"Doctor chose to save: Player {doctor_choice + 1}")
        saved_player = doctor_choice

        # Police's turn
        if police_officer_prompt(screen, roles, images, font):
            police_choice = game_stage_prompt(screen, roles, images, "Police: Who do you want to shoot?", font)
            messages.append(f"Police chose to shoot: Player {police_choice + 1}")

            if police_choice == saved_player:
                messages.append(f"Police's shot had no effect because Player {police_choice + 1} was saved.")
            elif roles[police_choice] == "Killer":
                statuses[police_choice] = "dead"
                messages.append(f"Police successfully shot the Killer (Player {police_choice + 1}).")
            else:
                statuses[police_choice] = "dead"
                statuses[roles.index("Police")] = "dead"
                messages.append(f"Police and Player {police_choice + 1} both died.")
        else:
            messages.append("Police chose not to shoot anyone.")

        killer_choice = game_stage_prompt(screen, roles, images, "Killer: Who do you want to kill?", font)
        messages.append(f"Killer chose to kill: Player {killer_choice + 1}")

        if killer_choice == saved_player:
            messages.append(f"Killer's attack had no effect because Player {killer_choice + 1} was saved.")
        else:
            statuses[killer_choice] = "dead"
            messages.append(f"Killer successfully killed Player {killer_choice + 1}.")

        display_night_summary(screen, roles, statuses, images, messages)

        game_over = voting_stage(screen, roles, statuses, images)
        if game_over:  
            return

def display_night_summary(screen, roles, statuses, images, messages):
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 36)

    while True:
        screen.fill((50, 50, 100))
        screen_width, screen_height = screen.get_size()

        
        summary_text = font.render("Night Summary", True, (255, 255, 255))
        screen.blit(summary_text, ((screen_width - summary_text.get_width()) // 2, int(screen_height * 0.05)))

        adjusted_y_offset = int(screen_height * 0.2)

        draw_characters(screen, roles, statuses, images, adjusted_y_offset)

        message_start_y = adjusted_y_offset + 200  
        for i, message in enumerate(messages):
            message_text = small_font.render(message, True, (255, 255, 255))
            screen.blit(message_text, (50, message_start_y + i * 30))  

        # Draw "Continue" button
        button_width, button_height = 200, 80
        button_x = (screen_width - button_width) // 2
        button_y = int(screen_height * 0.85)
        pygame.draw.rect(screen, (100, 200, 100), (button_x, button_y, button_width, button_height))
        continue_text = font.render("Continue", True, (255, 255, 255))
        screen.blit(continue_text, (button_x + (button_width - continue_text.get_width()) // 2, button_y + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    return  
        pygame.display.flip()

def game_stage_prompt(screen, roles, images, prompt, font):
    screen_width, screen_height = screen.get_size()
    positions = [(i * 100 + 50, int(screen_height * 0.5) + 50) for i in range(8)]
    labels = [str(i + 1) for i in range(8)]
    selected = None

    while True:
        screen.fill((50, 50, 100))
        draw_characters(screen, roles, ["alive"] * len(roles), images)
        draw_prompt_with_checkboxes(screen, prompt, labels, selected, font, positions)

        # Draw Next button
        next_x, next_y = (screen_width - 200) // 2, int(screen_height * 0.85)
        pygame.draw.rect(screen, (100, 200, 100), (next_x, next_y, 200, 50))
        next_text = font.render("Next", True, (255, 255, 255))
        screen.blit(next_text, (next_x + (200 - next_text.get_width()) // 2, next_y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i, pos in enumerate(positions):
                    if pos[0] <= mouse_x <= pos[0] + 30 and pos[1] <= mouse_y <= pos[1] + 30:
                        selected = i
                if next_x <= mouse_x <= next_x + 200 and next_y <= mouse_y <= next_y + 50:
                    return selected

        pygame.display.flip()


def draw_prompt_with_checkboxes(screen, prompt, labels, selected, font, positions):
    screen_width, screen_height = screen.get_size()
    prompt_text = font.render(prompt, True, (255, 255, 255))
    screen.blit(prompt_text, ((screen_width - prompt_text.get_width()) // 2, int(screen_height * 0.4)))

    for i, (label, pos) in enumerate(zip(labels, positions)):
        pygame.draw.rect(screen, (255, 255, 255), (*pos, 30, 30), 2)
        if i == selected:
            pygame.draw.rect(screen, (255, 255, 255), (pos[0] + 5, pos[1] + 5, 20, 20))
        checkbox_text = font.render(label, True, (255, 255, 255))
        screen.blit(checkbox_text, (pos[0] + 40, pos[1]))


def police_officer_prompt(screen, roles, images, font):
    screen_width, screen_height = screen.get_size()

    button_width, button_height = 200, 50
    yes_x, yes_y = (screen_width // 4) - (button_width // 2), int(screen_height * 0.7)
    no_x, no_y = (3 * screen_width // 4) - (button_width // 2), int(screen_height * 0.7)

    while True:
        screen.fill((50, 50, 100))
        
        draw_characters(screen, roles, ["alive"] * len(roles), images)

        # Draw prompt above the characters
        prompt_text = font.render("Police: Do you want to shoot someone?", True, (255, 255, 255))
        prompt_x = (screen_width - prompt_text.get_width()) // 2
        prompt_y = int(screen_height * 0.3)  # Position the prompt above the characters
        screen.blit(prompt_text, (prompt_x, prompt_y))

        # Draw Yes button
        pygame.draw.rect(screen, (100, 200, 100), (yes_x, yes_y, button_width, button_height))
        yes_text = font.render("Yes", True, (255, 255, 255))
        yes_text_x = yes_x + (button_width - yes_text.get_width()) // 2
        yes_text_y = yes_y + (button_height - yes_text.get_height()) // 2
        screen.blit(yes_text, (yes_text_x, yes_text_y))

        # Draw No button
        pygame.draw.rect(screen, (200, 100, 100), (no_x, no_y, button_width, button_height))
        no_text = font.render("No", True, (255, 255, 255))
        no_text_x = no_x + (button_width - no_text.get_width()) // 2
        no_text_y = no_y + (button_height - no_text.get_height()) // 2
        screen.blit(no_text, (no_text_x, no_text_y))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if yes_x <= mouse_x <= yes_x + button_width and yes_y <= mouse_y <= yes_y + button_height:
                    return True
                elif no_x <= mouse_x <= no_x + button_width and no_y <= mouse_y <= no_y + button_height:
                    return False

        pygame.display.flip()

def voting_stage(screen, roles, statuses, images):
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 36)

    alive_players = [i for i, status in enumerate(statuses) if status == "alive"]

    votes = {player: None for player in alive_players}
    dropdown_open = {player: False for player in alive_players}

    running = True

    while running:
        screen.fill((50, 50, 100))
        screen_width, screen_height = screen.get_size()

        title_text = font.render("Voting Stage", True, (255, 255, 255))
        screen.blit(title_text, ((screen_width - title_text.get_width()) // 2, int(screen_height * 0.05)))

        rect_width, rect_height = 120, 150
        margin = (screen_width - len(alive_players) * rect_width) // (len(alive_players) + 1)
        y = int(screen_height * 0.2)

        for i, player_index in enumerate(alive_players):
            x = margin + i * (rect_width + margin)
            # Draw player rectangle
            pygame.draw.rect(screen, (255, 255, 255), (x, y, rect_width, rect_height))
            screen.blit(images[roles[player_index]], (x + 10, y + 10))

            index_text = small_font.render(f"{player_index + 1}", True, (255, 255, 255))
            screen.blit(index_text, (x + (rect_width - index_text.get_width()) // 2, y - 30))


            dropdown_x = x
            dropdown_y = y + rect_height + 20
            dropdown_width = 120
            dropdown_height = 30

            if dropdown_open[player_index]:
                pygame.draw.rect(screen, (200, 200, 200), (dropdown_x, dropdown_y, dropdown_width, dropdown_height * len(alive_players)))
                for j, target_player in enumerate(alive_players):
                    option_y = dropdown_y + j * dropdown_height
                    option_text = small_font.render(f"Player {target_player + 1}", True, (0, 0, 0))
                    screen.blit(option_text, (dropdown_x + 5, option_y + 5))
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if dropdown_x <= mouse_x <= dropdown_x + dropdown_width and option_y <= mouse_y <= option_y + dropdown_height:
                        pygame.draw.rect(screen, (180, 180, 180), (dropdown_x, option_y, dropdown_width, dropdown_height))
                        if pygame.mouse.get_pressed()[0]:  
                            votes[player_index] = target_player
                            dropdown_open[player_index] = False  
            else:
                selected_text = small_font.render(
                    f"Player {votes[player_index] + 1}" if votes[player_index] is not None else "Vote",
                    True,
                    (0, 0, 0),
                )
                pygame.draw.rect(screen, (255, 255, 255), (dropdown_x, dropdown_y, dropdown_width, dropdown_height))
                screen.blit(selected_text, (dropdown_x + 5, dropdown_y + 5))

        button_width, button_height = 200, 80
        button_x = (screen_width - button_width) // 2
        button_y = int(screen_height * 0.85)
        pygame.draw.rect(screen, (100, 200, 100), (button_x, button_y, button_width, button_height))
        continue_text = font.render("Continue", True, (255, 255, 255))
        screen.blit(continue_text, (button_x + (button_width - continue_text.get_width()) // 2, button_y + 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    running = False  
                
                for player_index in alive_players:
                    dropdown_x = margin + alive_players.index(player_index) * (rect_width + margin)
                    dropdown_y = y + rect_height + 20
                    if dropdown_x <= mouse_x <= dropdown_x + dropdown_width and dropdown_y <= mouse_y <= dropdown_y + dropdown_height:
                        dropdown_open[player_index] = not dropdown_open[player_index]  

        pygame.display.flip()

    print("Votes:", votes)
    return process_votes(screen, roles, statuses, votes, images)

def process_votes(screen, roles, statuses, votes, images):
    # Tally votes
    vote_count = {}
    for vote in votes.values():
        if vote is not None:
            vote_count[vote] = vote_count.get(vote, 0) + 1

    most_votes = max(vote_count.values(), default=0)
    potential_killers = [player for player, count in vote_count.items() if count == most_votes]

    if len(potential_killers) == 1:
        eliminated_player = potential_killers[0]
        statuses[eliminated_player] = "dead"
        print(f"Player {eliminated_player + 1} eliminated as the suspected killer.")
        if roles[eliminated_player] == "Killer":
            display_game_over_screen(screen, "Civilians Win")
            return True  # Game over
    else:
        print("No majority vote. No one is eliminated.")

    if "Killer" in [roles[i] for i, status in enumerate(statuses) if status == "alive"]:
        return False 
    else:
        display_game_over_screen(screen, "Civilians Win")
        return True


def display_game_over_screen(screen, message):
    font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 50)
    screen.fill((50, 50, 100))
    text = font.render(message, True, (255, 255, 255))
    screen_width, screen_height = screen.get_size()
    screen.blit(text, ((screen_width - text.get_width()) // 2, screen_height // 3))

    # Draw "Continue" button
    button_width, button_height = 200, 80
    button_x = (screen_width - button_width) // 2
    button_y = int(screen_height * 0.7)
    pygame.draw.rect(screen, (100, 200, 100), (button_x, button_y, button_width, button_height))
    continue_text = button_font.render("Continue", True, (255, 255, 255))
    screen.blit(continue_text, (button_x + (button_width - continue_text.get_width()) // 2, button_y + (button_height - continue_text.get_height()) // 2))

    pygame.display.flip()

    # Wait for the player to click the continue button
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if button_x <= mouse_x <= button_x + button_width and button_y <= mouse_y <= button_y + button_height:
                    pygame.quit()
                    return  # Exit the game


if __name__ == "__main__":
    start_pygame_interface()