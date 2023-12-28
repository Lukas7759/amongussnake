import pygame
from random import choice, randint
import os

pygame.init()

SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 786

screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('amongus snake')

clock = pygame.time.Clock()
POINTS_FONT = pygame.font.SysFont("verdana", 20)

bonus_images = ['b1.png', 'b2.png', 'b3.png']

SOUND_PATH = "sounds"
SOUNDS = {
    50: "50.wav",
    100: "100.wav",
    200: "200.wav",
    400: "400.wav",
    500: "500.wav",
    "point": "point.wav",
    "end": "end.mp4"
}

FRAMES_PER_SECOND = 60
frames_cnt = 0

player_points = 0

def load_sound(sound_path: str):
    try:
        return pygame.mixer.Sound(os.path.join(SOUND_PATH, sound_path))
    except pygame.error:
        print(f"Error loading sound: {sound_path}")
        return None

def load_image(img_path: str, position):
    try:
        image = pygame.image.load(os.path.join("images", img_path))
        surface = image.convert()
        transparent_color = (0, 0, 0)
        surface.set_colorkey(transparent_color)
        rect = surface.get_rect(center=position)
        return [image, surface, rect]
    except pygame.error:
        print(f"Error loading image: {img_path}")
        return None

def print_image(img_list) -> None:
    if img_list:
        image, surface, rect = img_list
        screen_surface.blit(surface, rect)

def set_position_image(img_list, position):
    if img_list:
        image, surface, rect = img_list
        rect = surface.get_rect(center=position)
        return [image, surface, rect]
    return None

def calculate_player_movement(keys):
    speed = 40
    delta_x = 0
    delta_y = 0

    if keys[pygame.K_i]:
        delta_y -= speed
    if keys[pygame.K_k]:
        delta_y += speed
    if keys[pygame.K_l]:
        delta_x += speed
    if keys[pygame.K_j]:
        delta_x -= speed

    return [delta_x, delta_y]

def limit_position(position):
    x, y = position
    x = max(0, min(x, SCREEN_WIDTH))
    y = max(0, min(y, SCREEN_HEIGHT))
    return [x, y]

def generate_bonus_object():
    image_name = choice(bonus_images)
    x = randint(0, SCREEN_WIDTH)
    y = randint(0, SCREEN_HEIGHT)
    position = [x, y]
    new_obj = load_image(image_name, position)
    if new_obj:
        bonus_objects.append(new_obj)

def print_bonus_objects():
    for obj in bonus_objects:
        print_image(obj)

def check_collisions():
    global player_points
    rect_player = player[2]

    for index in range(len(bonus_objects) - 1, -1, -1):
        obj = bonus_objects[index]
        if obj:
            rect = obj[2]
            if rect.colliderect(rect_player):
                bonus_objects.pop(index)
                player_points += 1
                check_point_sound(player_points)

def check_point_sound(points):
    if points in {50, 100, 200, 400, 500}:
        play_sound(points)

def play_sound(sound_key):
    sound_path = SOUNDS.get(sound_key)
    if sound_path:
        try:
            if sound_key == "end":
                pygame.mixer.music.load(os.path.join(SOUND_PATH, sound_path))
                pygame.mixer.music.play()
            else:
                sound = load_sound(sound_path)
                if sound:
                    sound.play()
        except pygame.error:
            print(f"Error playing sound: {sound_key}")

def print_points(points: int) -> None:
    text = f"Points: {points}"
    color = [255, 255, 255]
    position = [0, 0]
    label = POINTS_FONT.render(text, False, color)
    screen_surface.blit(label, position)

player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player = load_image('amongus.png', player_pos)
background_color = [9, 42, 121]
bonus_objects = []

game_status = "playing"
while game_status == "playing":
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            game_status = "quit"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                generate_bonus_object()

    pressed_keys = pygame.key.get_pressed()
    delta_x, delta_y = calculate_player_movement(pressed_keys)

    player_pos[0] += delta_x
    player_pos[1] += delta_y
    player_pos = limit_position(player_pos)

    player = set_position_image(player, player_pos)

    screen_surface.fill(background_color)
    print_image(player)

    if frames_cnt % (FRAMES_PER_SECOND * 1) == 0:
        generate_bonus_object()

    check_collisions()

    print_bonus_objects()

    print_points(player_points)

    if player_points >= 600:
        play_sound("end")
        game_status = "quit"

    pygame.display.update()

    frames_cnt += 1

    clock.tick(FRAMES_PER_SECOND)

print("Zamykanie aplikacji")
pygame.quit()
quit()
