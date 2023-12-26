import pygame
from random import choice, randint
 
pygame.init()
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 786
 
screen_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Pierwsza Gra')
 
clock = pygame.time.Clock()
POINTS_FONT = pygame.font.SysFont("verdana", 20)
 
bonus_images = [
    'b1.png',
    'b2.png',
    'b3.png'
]
 
FRAMES_PER_SECOND = 60
frames_cnt = 0
 
player_points = 0
 
def load_image(img_path: str, position):
    image = pygame.image.load(img_path)
    surface = image.convert()
    transparent_color = (0, 0, 0)
    surface.set_colorkey(transparent_color)
    rect = surface.get_rect(center=position)
    return [image, surface, rect]
 
def print_image(img_list) -> None:
    image, surface, rect = img_list
    screen_surface.blit(surface, rect)
    pass
 
def set_position_image(img_list, position):
    image, surface, rect = img_list
    rect = surface.get_rect(center=position)
    return [image, surface, rect]
 
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
    bonus_objects.append(new_obj)
    pass
 
def print_bonus_objects():
    for obj in bonus_objects:
        print_image(obj)
        pass
    pass
 
def check_collisions():
    global player_points
    rect_player = player[2]
 
    for index in range(len(bonus_objects) - 1, -1, -1):
        obj = bonus_objects[index]
        rect = obj[2]
        if rect.colliderect(rect_player):
            bonus_objects.pop(index)
            player_points += 1
            pass
        pass
    pass
 
def print_points(points: int) -> None:
    text = f"Points: {points}"
    color = [255, 255, 255]
    position = [0, 0]
    label = POINTS_FONT.render(text, False, color)
    screen_surface.blit(label, position)
    pass
 
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
player = load_image('amongus.png', player_pos)
background_color = [9, 42, 121]
bonus_objects = []
 
game_status = True
while game_status:
    events = pygame.event.get()
 
    for event in events:
        if event.type == pygame.QUIT:
            game_status = False
        pass  # for event
 
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
        pass
 
    check_collisions()
 
    print_bonus_objects()
    
    print_points(player_points)
    
    pygame.display.update()
 
    frames_cnt += 1
 
    clock.tick(FRAMES_PER_SECOND)
    pass
 
print("Zamykanie aplikacji")
pygame.quit()
quit()
