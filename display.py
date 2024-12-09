import pygame

prover_message=""

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
        
        player_name_text = name_font.render(f"Player {i + 1}", True, (255, 255, 255))
        name_x = x + (rect_width - player_name_text.get_width()) // 2
        screen.blit(player_name_text, (name_x, y - 30))
        
        index_text = font.render(f"{i + 1}", True, (255, 255, 255))
        index_x = x + (rect_width - index_text.get_width()) // 2
        screen.blit(index_text, (index_x, y - 30 - index_text.get_height()))
        
        role_text = name_font.render(role, True, (255, 255, 255))
        role_x = x + (rect_width - role_text.get_width()) // 2
        screen.blit(role_text, (role_x, y + rect_height - 20))


def display_elimination_summary(screen, roles, statuses, votes, images):
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 36)

    while True:
        screen.fill((50, 50, 100))  
        screen_width, screen_height = screen.get_size()

        summary_text = font.render("Elimination Summary", True, (255, 255, 255))
        screen.blit(summary_text, ((screen_width - summary_text.get_width()) // 2, int(screen_height * 0.05)))

        adjusted_y_offset = int(screen_height * 0.2)

        if len(votes) > 0:
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

            elimination_text = small_font.render(elimination_message, True, (255, 255, 255))
            screen.blit(elimination_text, ((screen_width - elimination_text.get_width()) // 2, adjusted_y_offset))

        draw_characters(screen, roles, statuses, images, adjusted_y_offset + 80)

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
                return 

        pygame.display.flip()  

def display_game_over_screen(screen, message):
    font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 50)
    screen.fill((50, 50, 100))
    
    text = font.render(message, True, (255, 255, 255))
    screen_width, screen_height = screen.get_size()
    screen.blit(text, ((screen_width - text.get_width()) // 2, screen_height // 3))

    # Button properties
    button_width, button_height = 200, 80
    button_x = (screen_width - button_width) // 2
    button_y = int(screen_height * 0.7)

    pygame.display.flip()

    while True:
        screen.fill((50, 50, 100))  
        screen.blit(text, ((screen_width - text.get_width()) // 2, screen_height // 3))  # Redraw message
        
        button_hovering = draw_button(
            screen,
            "Continue",
            button_font,
            (100, 200, 100),   
            (120, 220, 120),   
            (255, 255, 255),   
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
                    run_prover9_and_extract_output()
                    display_prover_window(screen)
                    exit()
                    return 
                
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        rendered_line = font.render(" ".join(current_line), True, (0, 0, 0))
        if rendered_line.get_width() > max_width:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]
    if current_line:
        lines.append(" ".join(current_line))
    return lines


def draw_button_update(screen, text, font, color, hover_color, text_color, x, y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hovering = x <= mouse_x <= x + width and y <= mouse_y <= y + height

    button_color = hover_color if hovering else color

    pygame.draw.rect(screen, button_color, (x, y, width, height), border_radius=10)
    pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 3, border_radius=10)

    rendered_text = font.render(text, True, text_color)
    text_x = x + (width - rendered_text.get_width()) // 2
    text_y = y + (height - rendered_text.get_height()) // 2
    screen.blit(rendered_text, (text_x, text_y))

    return hovering
import subprocess

def run_prover9_and_extract_output(input_file="night.in", output_file="night.out"):

    global prover_message
    command = f"/home/cata/LADR-2009-11A/bin/prover9 -f {input_file} > {output_file}"
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running prover9: {e}")
        return None
    try:
        with open(output_file, "r") as file:
            lines = file.readlines()
        
        separator = "============================== end of search =========================\n"
        if separator in lines:
            separator_index = lines.index(separator)
            prover_message="".join(lines[separator_index + 1:])
            return "".join(lines[separator_index + 1:])
        else:
            print(f"Separator line not found in {output_file}")
            return None
    except FileNotFoundError:
        print(f"Output file {output_file} not found.")
        return None


def display_prover_window(screen):
    global prover_message
    pygame.init()
    font = pygame.font.Font(None, 36)
    button_font = pygame.font.Font(None, 50)  
    screen.fill((30, 30, 60)) 

    message = (
        "The prover9 file 'night.in' has been generated. "
        "To verify the current ending, run the following commands in the terminal:\n\n"
        "    prover9 -f night.in > night.out\n\n"
        "Check the terminal output:\n"
        "    - 'Search Failed' means the prover9 couldn't prove the ending is valid.\n"
        "    - 'Theorem Proved' means prover9 deduced the ending is correct. \n"
        "   RESULT FROM THE PROVER!!!!!!!!!!\n"
        + prover_message
    )
    screen_width, screen_height = screen.get_size()
    wrapped_message = wrap_text(message, font, screen_width - 80)

    y_offset = 100 
    for line in wrapped_message:
        rendered_text = font.render(line, True, (255, 255, 255))
        screen.blit(rendered_text, ((screen_width - rendered_text.get_width()) // 2, y_offset))
        y_offset += 40 

    button_width, button_height = 250, 80
    button_x = (screen_width - button_width) // 2
    button_y = screen_height - 150

    pygame.display.flip()

    while True:
        screen.fill((30, 30, 60)) 

        y_offset = 100
        for line in wrapped_message:
            rendered_text = font.render(line, True, (255, 255, 255))
            screen.blit(rendered_text, ((screen_width - rendered_text.get_width()) // 2, y_offset))
            y_offset += 40

        button_hovering = draw_button_update(
            screen,
            "Continue",
            button_font,
            (50, 150, 50),   
            (70, 180, 70),  
            (255, 255, 255), 
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
                    return
