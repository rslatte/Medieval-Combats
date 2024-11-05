import pygame
import sys
import os

pygame.init()

# Set up the screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Character Select")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Define character images
character_images = []
character_paths = [
    "test/ch1.png",
    "test/ch2.png",
    "test/ch3.png",
    "test/ch4.png",
    "test/ch5.png"
]

for path in character_paths:
    if os.path.exists(path):
        character_images.append(pygame.image.load(path).convert_alpha())
    else:
        print(f"Error: File {path} does not exist.")
        sys.exit()

# Define character animations and their frame counts
character_animations = []
animation_paths = [
    "test/ch1_animation.png",
    "test/ch2_animation.png",
    "test/ch3_animation.png",
    "test/ch4_animation.png",
    "test/ch5_animation.png"
]

frame_counts = [8, 11, 10, 8, 10]  # Specify the number of frames for each character

for idx, path in enumerate(animation_paths):
    animation_frames = []
    sprite_sheet = pygame.image.load(path).convert_alpha()
    frame_count = frame_counts[idx]
    frame_height = sprite_sheet.get_height()
    frame_width = sprite_sheet.get_width() // frame_count

    for i in range(frame_count):
        frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
        animation_frames.append(frame)
    character_animations.append(animation_frames)

# Load small images for characters
small_images = []
small_image_paths = [
    "test/n1.png",
    "test/n2.png",
    "test/n3.png",
    "test/n4.png",
    "test/n5.png"
]

for path in small_image_paths:
    if os.path.exists(path):
        small_images.append(pygame.image.load(path).convert_alpha())
    else:
        print(f"Error: File {path} does not exist.")
        sys.exit()

# Game state
font_path = "test/turok.ttf"
font_path_ch = "test/lansui.ttf"
font = pygame.font.Font(font_path, 36)
title_font = pygame.font.Font(font_path, 72)
small_font_ch = pygame.font.Font(font_path_ch, 24)  # font for chinese
small_font = pygame.font.Font(font_path, 24)  # Smaller font for the "Press Enter to continue" message

state = "start_screen"

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def draw_text_with_colored_word(text, font, color, colored_word, colored_word_color, x, y):
    words = text.split(' ')
    text_surface = pygame.Surface((0, 0), pygame.SRCALPHA, 32).convert_alpha()
    cursor_x = 0

    for word in words:
        if word == colored_word:
            word_surface = font.render(word, True, colored_word_color)
        else:
            word_surface = font.render(word, True, color)
        text_surface.blit(word_surface, (cursor_x, 0))
        cursor_x += word_surface.get_width() + font.size(' ')[0]

    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

# Define and load start game background
start_bg_image = pygame.image.load("test/start_background/background.png").convert_alpha()
# Function for drawing start screen background
def draw_start_bg():
    scaled_bg = pygame.transform.scale(start_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

def draw_start_screen():
    draw_start_bg()
    pygame.display.flip()

# Load character select background
character_select_bg_image = pygame.image.load("test/select.png").convert_alpha()
# Function for drawing character select background
def draw_character_select_bg():
    scaled_bg = pygame.transform.scale(character_select_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# Define character positions and sizes
CHARACTER_SIZE = (100, 100)
CHARACTER_GAP = 20

# Calculate the starting X position to center the characters
total_width = len(character_images) * CHARACTER_SIZE[0] + (len(character_images) - 1) * CHARACTER_GAP
CHARACTER_START_X = (SCREEN_WIDTH - total_width) // 2
CHARACTER_START_Y = (SCREEN_HEIGHT - CHARACTER_SIZE[1]) // 2 + 100

# Define player variables
player1_selected = False
player2_selected = False
player1_character = None
player2_character = None

# Animation variables
selected_character = None
current_animation_frames = None
current_frame_index = 0
animation_counter = 0

# Define vertical offset for character animations
ANIMATION_VERTICAL_OFFSET = [50, 10, -30, -100, 10]

def draw_centered_text(text, font, color, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y))
    screen.blit(text_surface, text_rect)

def draw_highlighted_text(text, font, highlight_color, normal_color, highlight_word, y):
    words = text.split()
    x = SCREEN_WIDTH // 2
    total_width = sum(font.size(word)[0] for word in words) + (len(words) - 1) * font.size(' ')[0]
    start_x = x - total_width // 2

    for word in words:
        color = highlight_color if word == highlight_word else normal_color
        word_surface = font.render(word, True, color)
        word_rect = word_surface.get_rect(topleft=(start_x, y))
        screen.blit(word_surface, word_rect)
        start_x += word_surface.get_width() + font.size(' ')[0]

def draw_character_select():
    draw_character_select_bg()
    if not player1_selected:
        draw_text("Player 1: Select Your Warrior", font, WHITE, 20, 20)
    elif not player2_selected:
        draw_text("Player 2: Select Your Warrior", font, WHITE, 20, 20)

    # Display character images in a single row centered on the screen
    for i, character_image in enumerate(character_images):
        x = CHARACTER_START_X + i * (CHARACTER_SIZE[0] + CHARACTER_GAP)
        y = CHARACTER_START_Y

        if player1_selected and not player2_selected and i == player1_character - 1:
            continue  # Skip the character already selected by player 1

        # Scale
        character_image_scaled = pygame.transform.scale(character_image, CHARACTER_SIZE)
        screen.blit(character_image_scaled, (x, y))
        draw_text(f"{i + 1}", font, WHITE, x, y + CHARACTER_SIZE[1] + 5)

    # Display selected character animation
    if current_animation_frames is not None:
        frame = current_animation_frames[current_frame_index]
        # Scale the frame to make it larger
        scale_factor = 2.5 if selected_character == 4 else 2  # Make the 5th character's animation larger
        scaled_frame = pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
        x = (SCREEN_WIDTH - scaled_frame.get_width()) // 2
        y = CHARACTER_START_Y - scaled_frame.get_height() + 50

        y += ANIMATION_VERTICAL_OFFSET[selected_character]
        screen.blit(scaled_frame, (x, y))

        # Display the corresponding small image in the top-right corner
        if selected_character is not None:  # Check if a character is selected
            small_image = small_images[selected_character]
            small_image_pos = (SCREEN_WIDTH - small_image.get_width() - 10, 10)
            screen.blit(small_image, small_image_pos)

        # "Press Enter to continue" message
        draw_highlighted_text("Press Enter to continue", small_font, YELLOW, WHITE, "Enter", SCREEN_HEIGHT - 80) 

    pygame.display.flip()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if state == "start_screen":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 160, SCREEN_HEIGHT // 2 + 50, 320, 80)  # Increased size
                if start_button_rect.collidepoint(mouse_x, mouse_y):
                    state = "character_select"
                    animation_counter = 0  # Initialize animation counter when entering character select
                    current_frame_index = 0  # Initialize frame index when entering character select
        elif state == "character_select":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Check if a character is clicked
                for i in range(len(character_images)):
                    x = CHARACTER_START_X + i * (CHARACTER_SIZE[0] + CHARACTER_GAP)
                    y = CHARACTER_START_Y
                    if x < mouse_x < x + CHARACTER_SIZE[0] and y < mouse_y < y + CHARACTER_SIZE[1]:
                        selected_character = i
                        current_animation_frames = character_animations[selected_character]
                        current_frame_index = 0
                        animation_counter = 0
                        break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and selected_character is not None:
                    if not player1_selected:
                        player1_selected = True
                        player1_character = selected_character + 1
                        selected_character = None
                        current_animation_frames = None
                    elif not player2_selected:
                        player2_selected = True
                        player2_character = selected_character + 1
                        running = False

    # Update and draw the appropriate screen
    if state == "start_screen":
        draw_start_screen()
    elif state == "character_select":
        draw_character_select()

    # Update animation frame
    if current_animation_frames is not None:
        animation_speed = 0.02
        if selected_character == 3:  # set the 4th character slower animation
            animation_speed = 0.01
        animation_counter += animation_speed
        current_frame_index = int(animation_counter) % len(current_animation_frames)

# print selections
# print(f"Player 1 selected character {player1_character}")
# print(f"Player 2 selected character {player2_character}")
