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

# Game state
font_path = "test/turok.ttf"
font_path_ch = "test/lansui.ttf"
font = pygame.font.Font(font_path, 36)
title_font = pygame.font.Font(font_path, 72)
small_font_ch = pygame.font.Font(font_path_ch, 24)  #font for chinese

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

# define and def start game background
start_bg_image = pygame.image.load("test/start_background/background.png").convert_alpha()
#function for drawing background
def draw_start_bg():
  scaled_bg = pygame.transform.scale(start_bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

def draw_start_screen():
    # screen.fill(BLACK)
    draw_start_bg()
    # draw_text("WARRIORS", title_font, WHITE, SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100)
    # draw_text("Game Start", font, WHITE, SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()

# Define character positions and sizes
CHARACTER_SIZE = (100, 100)
CHARACTER_GAP = 20

# Calculate the starting X position to center the characters
total_width = len(character_images) * CHARACTER_SIZE[0] + (len(character_images) - 1) * CHARACTER_GAP
CHARACTER_START_X = (SCREEN_WIDTH - total_width) // 2
CHARACTER_START_Y = (SCREEN_HEIGHT - CHARACTER_SIZE[1]) // 2 + 100

# Define fonts
font_path = "test/turok.ttf"
font = pygame.font.Font(font_path, 36)
small_font = pygame.font.Font(font_path, 24)  # Smaller font for the "Press Enter to continue" message

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
    screen.fill(BLACK)
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

    # "Press Enter to continue" message
    if selected_character is not None:
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
                start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 50, 160, 40)
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
        if selected_character == 3: # set the 4th character slower animation
            animation_speed = 0.01
        animation_counter += animation_speed
        current_frame_index = int(animation_counter) % len(current_animation_frames)

# print selections
print(f"Player 1 selected character {player1_character}")
print(f"Player 2 selected character {player2_character}")



from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init() #這行能刪？

#create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

#set framerate
clock = pygame.time.Clock()
FPS = 60

#define colours
RED = (172, 31, 44)
GREEN = (69, 187, 137)
BLUE = (70, 130, 180)
GRAY = (105, 105, 105)
DARKER_GRAY = (79, 79, 79)
LIGHT_YELLOW = (255, 255, 204)
SKY_BLUE = (168, 223, 241)
DEEP_BLUE = (4, 37, 90)
BLACK_GRAY = (35, 35, 35)


#define game variables
intro_count = 5
last_count_update = pygame.time.get_ticks()
score = [0, 0]#player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

#define fighter variables
MARTIAL_HERO_SIZE = 126
MARTIAL_HERO_SIZE_y = 396/7
MARTIAL_HERO_SCALE = [3.5, 3.5]
MARTIAL_HERO_OFFSET = [45,30]
MARTIAL_HERO_DATA = [MARTIAL_HERO_SIZE, MARTIAL_HERO_SIZE_y, MARTIAL_HERO_SCALE, MARTIAL_HERO_OFFSET]

HERO_KNIGHT_SIZE = 180
HERO_KNIGHT_SIZE_y = 396/7
HERO_KNIGHT_SCALE = [3.3, 3.3]
HERO_KNIGHT_OFFSET = [75,59]
HERO_KNIGHT_DATA = [HERO_KNIGHT_SIZE, HERO_KNIGHT_SIZE_y, HERO_KNIGHT_SCALE, HERO_KNIGHT_OFFSET]

EVIL_WIZARD_SIZE = 250
EVIL_WIZARD_SIZE_y = 518/7
EVIL_WIZARD_SCALE = [3.4, 3.4]
EVIL_WIZARD_OFFSET = [107,114]
EVIL_WIZARD_DATA = [EVIL_WIZARD_SIZE, EVIL_WIZARD_SIZE_y, EVIL_WIZARD_SCALE, EVIL_WIZARD_OFFSET]

MEDIEVAL_KING_SIZE = 111
MEDIEVAL_KING_SIZE_y = 366/7
MEDIEVAL_KING_SCALE = [4.9, 3.5]
MEDIEVAL_KING_OFFSET = [47,53]
MEDIEVAL_KING_DATA = [MEDIEVAL_KING_SIZE, MEDIEVAL_KING_SIZE_y, MEDIEVAL_KING_SCALE, MEDIEVAL_KING_OFFSET]

MEDIEVAL_WARRIOR_SIZE = 135
MEDIEVAL_WARRIOR_SIZE_y = 530/7
MEDIEVAL_WARRIOR_SCALE = [4.5, 4.5]
MEDIEVAL_WARRIOR_OFFSET = [57,45]
MEDIEVAL_WARRIOR_DATA = [MEDIEVAL_WARRIOR_SIZE,  MEDIEVAL_WARRIOR_SIZE_y, MEDIEVAL_WARRIOR_SCALE, MEDIEVAL_WARRIOR_OFFSET]

DATA = [EVIL_WIZARD_DATA, HERO_KNIGHT_DATA, MARTIAL_HERO_DATA, MEDIEVAL_KING_DATA, MEDIEVAL_WARRIOR_DATA]

#load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

#load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

#load spritesheets
martial_hero_idle = pygame.image.load("assets/images/warriors/Martial Hero/Sprite/Idle.png").convert_alpha()
martial_hero_run = pygame.image.load("assets/images/warriors/Martial Hero/Sprite/Run.png").convert_alpha()
martial_hero_jump = pygame.image.load("assets/images/warriors/Martial Hero/Sprite/Going up.png").convert_alpha()
martial_hero_attack = pygame.image.load("assets/images/warriors/Martial Hero/Sprite/Attack1.png").convert_alpha()
martial_hero_skill = pygame.image.load("assets/images/warriors/Martial Hero/Sprite/Attack3.png").convert_alpha()
martial_hero_hit = pygame.image.load("assets/images/warriors/Martial Hero/Sprite/Take hit.png").convert_alpha()
martial_hero_death = pygame.image.load("assets/images/warriors/Martial Hero/Sprite/Death.png").convert_alpha()
martial_hero_sheet = [martial_hero_idle, martial_hero_run, martial_hero_jump, martial_hero_attack, martial_hero_skill, martial_hero_hit, martial_hero_death]

hero_knight_idle = pygame.image.load("assets/images/warriors/Hero Knight/Sprites/Idle.png").convert_alpha()
hero_knight_run = pygame.image.load("assets/images/warriors/Hero Knight/Sprites/Run.png").convert_alpha()
hero_knight_jump = pygame.image.load("assets/images/warriors/Hero Knight/Sprites/Jump.png").convert_alpha()
hero_knight_attack = pygame.image.load("assets/images/warriors/Hero Knight/Sprites/Attack1.png").convert_alpha()
hero_knight_skill = pygame.image.load("assets/images/warriors/Hero Knight/Sprites/Attack2.png").convert_alpha()
hero_knight_hit = pygame.image.load("assets/images/warriors/Hero Knight/Sprites/Take hit.png").convert_alpha()
hero_knight_death = pygame.image.load("assets/images/warriors/Hero Knight/Sprites/Death.png").convert_alpha()
hero_knight_sheet = [hero_knight_idle, hero_knight_run, hero_knight_jump, hero_knight_attack, hero_knight_skill, hero_knight_hit, hero_knight_death]

evil_wizard_idle = pygame.image.load("assets/images/warriors/EVil Wizard/Sprites/Idle.png").convert_alpha()
evil_wizard_run = pygame.image.load("assets/images/warriors/EVil Wizard/Sprites/Run.png").convert_alpha()
evil_wizard_jump = pygame.image.load("assets/images/warriors/EVil Wizard/Sprites/Jump.png").convert_alpha()
evil_wizard_attack = pygame.image.load("assets/images/warriors/EVil Wizard/Sprites/Attack1.png").convert_alpha()
evil_wizard_skill = pygame.image.load("assets/images/warriors/EVil Wizard/Sprites/Attack2.png").convert_alpha()
evil_wizard_hit = pygame.image.load("assets/images/warriors/EVil Wizard/Sprites/Take hit.png").convert_alpha()
evil_wizard_death = pygame.image.load("assets/images/warriors/EVil Wizard/Sprites/Death.png").convert_alpha()
evil_wizard_sheet = [evil_wizard_idle, evil_wizard_run, evil_wizard_jump, evil_wizard_attack, evil_wizard_skill, evil_wizard_hit, evil_wizard_death]

medieval_king_idle = pygame.image.load("assets/images/warriors/Medieval King Pack/Sprites/Idle.png").convert_alpha()
medieval_king_run = pygame.image.load("assets/images/warriors/Medieval King Pack/Sprites/Run.png").convert_alpha()
medieval_king_jump = pygame.image.load("assets/images/warriors/Medieval King Pack/Sprites/Jump.png").convert_alpha()
medieval_king_attack = pygame.image.load("assets/images/warriors/Medieval King Pack/Sprites/Attack1.png").convert_alpha()
medieval_king_skill = pygame.image.load("assets/images/warriors/Medieval King Pack/Sprites/Attack3.png").convert_alpha()
medieval_king_hit = pygame.image.load("assets/images/warriors/Medieval King Pack/Sprites/Take hit.png").convert_alpha()
medieval_king_death = pygame.image.load("assets/images/warriors/Medieval King Pack/Sprites/Death.png").convert_alpha()
medieval_king_sheet = [medieval_king_idle, medieval_king_run, medieval_king_jump, medieval_king_attack, medieval_king_skill, medieval_king_hit, medieval_king_death]

medieval_warrior_idle = pygame.image.load("assets/images/warriors/Medieval Warrior Pack/Sprites/Idle.png").convert_alpha()
medieval_warrior_run = pygame.image.load("assets/images/warriors/Medieval Warrior Pack/Sprites/Run.png").convert_alpha()
medieval_warrior_jump = pygame.image.load("assets/images/warriors/Medieval Warrior Pack/Sprites/Jump.png").convert_alpha()
medieval_warrior_attack = pygame.image.load("assets/images/warriors/Medieval Warrior Pack/Sprites/Attack2.png").convert_alpha()
medieval_warrior_skill = pygame.image.load("assets/images/warriors/Medieval Warrior Pack/Sprites/Attack3.png").convert_alpha()
medieval_warrior_hit = pygame.image.load("assets/images/warriors/Medieval Warrior Pack/Sprites/Get hit.png").convert_alpha()
medieval_warrior_death = pygame.image.load("assets/images/warriors/Medieval Warrior Pack/Sprites/Death.png").convert_alpha()
medieval_warrior_sheet = [medieval_warrior_idle, medieval_warrior_run, medieval_warrior_jump, medieval_warrior_attack, medieval_warrior_skill, medieval_warrior_hit, medieval_warrior_death]

sheet = [evil_wizard_sheet, hero_knight_sheet, martial_hero_sheet, medieval_king_sheet, medieval_warrior_sheet]

#define number of steps in each animation
MARTIAL_HERO_ANIMATION_STEPS = [10, 8, 3, 7, 7, 3, 11]
HERO_KNIGHT_ANIMATION_STEP = [11, 8, 3, 7, 7, 4, 11]
EVIL_WIZARD_ANIMATION_STEP = [8, 8, 2, 8, 7, 3, 7]
MEDIEVAL_KING_ANIMATION_STEP = [8, 8, 2, 4, 4, 4, 6]
MEDIEVAL_WARRIOR_ANIMATION_STEP = [10, 6, 2, 4, 4, 3, 9]
STEPS = [EVIL_WIZARD_ANIMATION_STEP, HERO_KNIGHT_ANIMATION_STEP, MARTIAL_HERO_ANIMATION_STEPS, MEDIEVAL_KING_ANIMATION_STEP, MEDIEVAL_WARRIOR_ANIMATION_STEP]

#define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
backcount_font = pygame.font.Font("assets/fonts/turok.ttf", 88)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)


#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
  scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
  screen.blit(scaled_bg, (0, 0))

#function for drawing fighter health bars
def draw_health_bar(health, fullhealth, x, y):
  ratio = health / fullhealth
  pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, RED, (x, y, 400, 30))
  pygame.draw.rect(screen, GREEN, (x, y, 400 * ratio, 30))

def draw_magic_bar(magic, x, y):
  ratio =  magic / 100
  pygame.draw.rect(screen, WHITE, (x - 1, y - 1, 202, 17))
  pygame.draw.rect(screen, DEEP_BLUE, (x, y, 200 * ratio, 15))
  if ratio == 1:
     pygame.draw.rect(screen, SKY_BLUE, (x, y, 200 * ratio, 15))
     
def draw_ques():
  ques_font = pygame.font.Font("assets/fonts/turok.ttf", 40)
  again_leave_font = pygame.font.Font("assets/fonts/turok.ttf", 25)
  pygame.draw.rect(screen, WHITE, (350, 125, 300, 225))
  pygame.draw.rect(screen, DARKER_GRAY, (350, 125, 300, 25))
  pygame.draw.rect(screen, GRAY, (375, 300, 100, 35))
  again_button = pygame.Rect(375, 300, 100, 35)
  pygame.draw.rect(screen, GRAY, (525, 300, 100, 35))
  leave_button = pygame.Rect(525, 300, 100, 35)
  draw_text('Play Again?', ques_font, BLACK, 405, 215)
  draw_text('Again!', again_leave_font, WHITE, 395, 302.5)
  draw_text('Leave', again_leave_font, WHITE, 545, 302.5)
  result_font = pygame.font.Font("assets/fonts/turok.ttf", 40)
  if fighter_1.alive == False:
      draw_text('Player 2 wins!', result_font, BLACK, 385, 175)
  elif fighter_2.alive == False:
      draw_text('Player 1 wins!', result_font, BLACK, 385, 175)

# 幫我檢查
#create two instances of fighters
DATA[player1_character - 1].append([72, 56])
DATA[player2_character - 1].append([112, 107])
fighter_1 = Fighter(player1_character, 'player1_character', 200, 310, False, DATA[player1_character - 1], sheet[player1_character - 1], STEPS[player1_character - 1], sword_fx)
fighter_2 = Fighter(player2_character, 'player2_character', 700, 310, True, DATA[player2_character - 1], sheet[player2_character - 1], STEPS[player2_character - 1], magic_fx)

#game loop
run = True
while run:

  clock.tick(FPS)

  #draw background
  draw_bg()

  #show player stats
  draw_health_bar(fighter_1.health, fighter_1.fullhealth, 20, 20)
  draw_health_bar(fighter_2.health, fighter_2.fullhealth, 580, 20)
  draw_magic_bar(fighter_1.magic, 20, 20)
  draw_magic_bar(fighter_2.magic, 580, 20)
  draw_text("P1: " + str(score[0]), score_font, LIGHT_YELLOW, 21, 60)
  draw_text("P2: " + str(score[1]), score_font, LIGHT_YELLOW, 925, 60)

  #update countdown
  if intro_count <= 0:
    #move fighters
    fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
    fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
  else:
    #display count timer
    draw_text(str(intro_count), backcount_font, BLACK_GRAY, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    draw_text(str(intro_count), count_font, LIGHT_YELLOW, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
    #update count timer
    if (pygame.time.get_ticks() - last_count_update) >= 1000:
      intro_count -= 1
      last_count_update = pygame.time.get_ticks()

  #update fighters
  fighter_1.update()
  fighter_2.update()

  #draw fighters
  fighter_1.draw(screen)
  fighter_2.draw(screen)

  #check for player defeat
  if round_over == False:
    if fighter_1.alive == False:
      score[1] += 1
      round_over = True
      # round_over_time = pygame.time.get_ticks()
    elif fighter_2.alive == False:
      score[0] += 1
      round_over = True

  else:
    # again or leave
    show_ques = True
    if show_ques:
        draw_ques()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                again_button = pygame.Rect(250, 300, 200, 75)
                leave_button = pygame.Rect(582, 300, 200, 75)
                if again_button.collidepoint(mouse_pos):
                    fighter_1 = Fighter(player1_character, 'player1_character', 200, 310, False, DATA[player1_character - 1], sheet[player1_character - 1], STEPS[player1_character - 1], sword_fx)
                    fighter_2 = Fighter(player2_character, 'player2_character', 700, 310, True, DATA[player2_character - 1], sheet[player2_character - 1], STEPS[player2_character - 1], magic_fx)
                    round_over = False
                    intro_count = 5
                    show_ques = False
                elif leave_button.collidepoint(mouse_pos):
                    run = False
                    pygame.quit()

                #update display
        pygame.display.update()

        # fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
        # fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.update()

#exit pygame
pygame.quit()