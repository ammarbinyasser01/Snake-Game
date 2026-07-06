import pygame
import random
import sys

from settings import *
from snake import Snake
from food import Food
from obstacle import Obstacles
from powerup import SpeedPowerUp
from ai_coach import AICoach

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Innovative Snake Game")

clock = pygame.time.Clock()

font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 40)

# -------------------------
# Themes (Multiple Environments)
# -------------------------

themes = [
    {
        "name": "Classic",
        "bg": (30, 30, 30)
    },
    {
        "name": "Forest",
        "bg": (20, 70, 20)
    }
]

theme_index = 0

# -------------------------
# Snake Colors
# -------------------------

colors = [
    GREEN,
    BLUE,
    YELLOW,
    (255, 120, 0),
    (180, 0, 255)
]

color_index = 0

# -------------------------
# Create Game Objects
# -------------------------

snake1 = Snake(10, 10, colors[color_index])
snake2 = Snake(30, 20, BLUE)

food = Food()
obstacles = Obstacles()

powerup = SpeedPowerUp()

coach = AICoach()

score1 = 0
score2 = 0

speed_timer1 = 0
speed_timer2 = 0

fps1 = FPS
fps2 = FPS

game_started = False
game_over = False

occupied = (
    snake1.body +
    snake2.body +
    obstacles.positions
)

food.respawn(occupied)

if random.randint(0, 1):
    powerup.spawn(occupied)

def reset_game():
    global snake1
    global snake2
    global food
    global obstacles
    global powerup
    global score1
    global score2
    global fps1
    global fps2
    global speed_timer1
    global speed_timer2
    global game_over

    snake1 = Snake(10, 10, colors[color_index])
    snake2 = Snake(30, 20, BLUE)

    food = Food()

    obstacles = Obstacles()

    powerup = SpeedPowerUp()

    occupied = (
        snake1.body +
        snake2.body +
        obstacles.positions
    )

    food.respawn(occupied)

    if random.randint(0, 1):
        powerup.spawn(occupied)

    score1 = 0
    score2 = 0

    fps1 = FPS
    fps2 = FPS

    speed_timer1 = 0
    speed_timer2 = 0

    game_over = False

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_game():
    screen.fill(themes[theme_index]["bg"])

    food.draw(screen)
    obstacles.draw(screen)
    powerup.draw(screen)

    snake1.draw(screen)
    snake2.draw(screen)

    draw_text(f"P1 Score: {score1}", font, WHITE, 10, 10)
    draw_text(f"P2 Score: {score2}", font, WHITE, 10, 40)

    draw_text(
        coach.get_tip(snake1, food, obstacles),
        font,
        WHITE,
        10,
        HEIGHT - 35
    )

    pygame.display.flip()

def draw_menu():
    screen.fill((25, 25, 25))

    draw_text("INNOVATIVE SNAKE GAME", big_font, WHITE, 170, 80)

    draw_text("ENTER - Start Game", font, WHITE, 270, 180)

    draw_text("T - Change Theme", font, WHITE, 270, 220)
    draw_text(f"Current Theme: {themes[theme_index]['name']}", font, YELLOW, 270, 250)

    draw_text("C - Change Snake Color", font, WHITE, 270, 310)
    pygame.draw.rect(screen, colors[color_index], (520, 307, 30, 30))

    draw_text("Player 1", font, GREEN, 40, 430)
    draw_text("W A S D", font, WHITE, 40, 460)

    draw_text("Player 2", font, BLUE, 560, 430)
    draw_text("Arrow Keys", font, WHITE, 560, 460)

    pygame.display.flip()

running = True

while running:

    if not game_started:

        draw_menu()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    game_started = True

                elif event.key == pygame.K_t:
                    theme_index = (theme_index + 1) % len(themes)

                elif event.key == pygame.K_c:
                    color_index = (color_index + 1) % len(colors)
                    snake1.color = colors[color_index]

        clock.tick(60)
        continue

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:

            # Player 1

            if event.key == pygame.K_w:
                snake1.change_direction(0, -1)

            elif event.key == pygame.K_s:
                snake1.change_direction(0, 1)

            elif event.key == pygame.K_a:
                snake1.change_direction(-1, 0)

            elif event.key == pygame.K_d:
                snake1.change_direction(1, 0)

            # Player 2

            elif event.key == pygame.K_UP:
                snake2.change_direction(0, -1)

            elif event.key == pygame.K_DOWN:
                snake2.change_direction(0, 1)

            elif event.key == pygame.K_LEFT:
                snake2.change_direction(-1, 0)

            elif event.key == pygame.K_RIGHT:
                snake2.change_direction(1, 0)

    snake1.move()
    snake2.move()

    snake1.check_wall_collision()
    snake2.check_wall_collision()

    snake1.check_self_collision()
    snake2.check_self_collision()

    obstacles.collision(snake1)
    obstacles.collision(snake2)

    occupied = (
        snake1.body +
        snake2.body +
        obstacles.positions
    )

    if snake1.eat_food(food.position):
        score1 += 1
        food.respawn(occupied)

    if snake2.eat_food(food.position):
        score2 += 1
        food.respawn(occupied)

    if powerup.check_collect(snake1):
        fps1 = FPS + 5
        speed_timer1 = pygame.time.get_ticks()

    if powerup.check_collect(snake2):
        fps2 = FPS + 5
        speed_timer2 = pygame.time.get_ticks()

    now = pygame.time.get_ticks()

    if now - speed_timer1 > 5000:
        fps1 = FPS

    if now - speed_timer2 > 5000:
        fps2 = FPS

    if not snake1.alive or not snake2.alive:

        screen.fill(BLACK)

        draw_text("GAME OVER", big_font, RED, 250, 180)

        draw_text(
            f"Player 1 Score : {score1}",
            font,
            WHITE,
            260,
            270
        )

        draw_text(
            f"Player 2 Score : {score2}",
            font,
            WHITE,
            260,
            310
        )

        draw_text(
            "Press R to Restart",
            font,
            GREEN,
            250,
            380
        )

        pygame.display.flip()

        waiting = True

        while waiting:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r:
                        reset_game()
                        waiting = False

        continue

    draw_game()

    clock.tick(max(fps1, fps2))

pygame.quit()