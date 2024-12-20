import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Avoid the Cars")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Road dimensions
ROAD_WIDTH = 600
LANE_WIDTH = ROAD_WIDTH // 4
road_x = (SCREEN_WIDTH - ROAD_WIDTH) // 2

# Load car images
player_car_image = pygame.image.load("CAR.png")
player_car_image = pygame.transform.scale(player_car_image, (96, 100))
player_car_width = 96
player_car_height = 100

# Enemy car images
enemy_car_images = [
    pygame.image.load("ENEMY CAR1.png"),
    pygame.image.load("ENEMY CAR2.png"),
    pygame.image.load("ENEMY CAR3.png")
]
enemy_car_images[0] = pygame.transform.scale(enemy_car_images[0], (130, 100))
enemy_car_images[1] = pygame.transform.scale(enemy_car_images[1], (70, 100))
enemy_car_images[2] = pygame.transform.scale(enemy_car_images[2], (70, 100))

# Player car
player_car = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, player_car_width, player_car_height)
player_speed = 10

# Enemy cars
enemy_car_width = 70
enemy_car_height = 100
enemy_cars = []
enemy_speed = 5

# Lane divider animation variables
divider_offset = 0

# Function to add a new enemy car
def add_enemy_car():
    lane = random.randint(0, 3)
    x_pos = road_x + lane * LANE_WIDTH + (LANE_WIDTH - enemy_car_width) // 2
    y_pos = -enemy_car_height

    for enemy in enemy_cars:
        if abs(enemy["rect"].x - x_pos) < enemy_car_width and abs(enemy["rect"].y - y_pos) < enemy_car_height:
            return

    enemy_image = random.choice(enemy_car_images)
    rect_width = int(enemy_car_width * 0.7)
    rect_height = int(enemy_car_height * 0.7)
    rect_x = x_pos + (enemy_car_width - rect_width) // 2
    rect_y = y_pos + (enemy_car_height - rect_height) // 2
    enemy_cars.append({"rect": pygame.Rect(rect_x, rect_y, rect_width, rect_height), "image": enemy_image, "image_x": x_pos, "image_y": y_pos})

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Function to increase enemy speed based on score
def increase_enemy_speed():
    global enemy_speed
    if score % 50 == 0 and score != 0:
        enemy_speed += enemy_speed * 0.15

# Main game loop
running = True
while running:
    screen.fill(GRAY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.rect(screen, BLACK, (road_x, 0, ROAD_WIDTH, SCREEN_HEIGHT))

    divider_offset += enemy_speed // 2
    if divider_offset >= 40:
        divider_offset = 0

    for i in range(4):
        lane_center = road_x + i * LANE_WIDTH + LANE_WIDTH // 2
        for y in range(-40, SCREEN_HEIGHT, 40):
            pygame.draw.line(screen, WHITE, (lane_center, y + divider_offset), (lane_center, y + 20 + divider_offset), 2)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_car.left > road_x:
        player_car.x -= player_speed
    if keys[pygame.K_RIGHT] and player_car.right < road_x + ROAD_WIDTH:
        player_car.x += player_speed

    if random.randint(1, 30) == 1:
        add_enemy_car()

    for enemy in enemy_cars[:]:
        enemy["rect"].y += enemy_speed
        enemy["image_y"] += enemy_speed
        if enemy["rect"].top > SCREEN_HEIGHT:
            enemy_cars.remove(enemy)
            score += 1
            increase_enemy_speed()

    for enemy in enemy_cars:
        if player_car.colliderect(enemy["rect"]):
            screen.fill(BLACK)
            game_over_text = font.render("GAME OVER", True, RED)
            final_score_text = font.render(f"Final Score: {score}", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

    screen.blit(player_car_image, (player_car.x, player_car.y))

    for enemy in enemy_cars:
        screen.blit(enemy["image"], (enemy["image_x"], enemy["image_y"]))

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
