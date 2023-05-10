import pygame
import os
import random
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Settings
FPS = 60
VEL = 5
MAIN_FONT = pygame.font.SysFont('comicsans', 30)
OUTCOME_FONT = pygame.font.SysFont('comicsans', 70)
BLOCK_SIZE = 40
BLOCK_NUMBER = 20

# Loading Assets
APPLE_MODEL = pygame.transform.scale(
    pygame.image.load(os.path.join('Assets', 'Apple.png')), (40, 40)
)
SNAKE_BLOCK_MODEL = pygame.image.load(os.path.join('Assets', 'Block.png'))
EATING_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Munch-Sound.mp3'))
EATING_SOUND.set_volume(0.2)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (175, 215, 70)
DARK_GREEN = (167, 210, 61)

# Events
SNAKE_GROWTH = pygame.USEREVENT + 1
SNAKE_MOVE = pygame.USEREVENT + 2
SNAKE_RESPAWN = pygame.USEREVENT + 3
pygame.time.set_timer(SNAKE_MOVE, 150)


class Snake():
    def __init__(self):
        self.snake_body = [
            pygame.Vector2(5, 10),
            pygame.Vector2(4, 10),
            pygame.Vector2(3, 10)
        ]
        self.direction = pygame.Vector2(1, 0)
        self.growth = False

    def draw(self):
        for block in self.snake_body:
            pos_x = int(block.x * BLOCK_SIZE)
            pos_y = int(block.y * BLOCK_SIZE)
            snake_block = pygame.Rect(pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE)
            WIN.blit(SNAKE_BLOCK_MODEL, snake_block)

    def movement(self):
        if self.growth:
            snake_copy = self.snake_body[:]
            snake_copy.insert(0, snake_copy[0] + self.direction)
            self.snake_body = snake_copy[:]
            self.growth = False
        else:
            snake_copy = self.snake_body[:-1]
            snake_copy.insert(0, snake_copy[0] + self.direction)
            self.snake_body = snake_copy[:]

    def collision(self, apple):
        if apple.apple_pos == self.snake_body[0]:
            pygame.event.post(pygame.event.Event(SNAKE_GROWTH))
            apple.reposition()

        for block in self.snake_body[1:]:
            if apple.apple_pos == block:
                apple.reposition()

    def respawn(self):
        self.snake_body = [
            pygame.Vector2(5, 10),
            pygame.Vector2(4, 10),
            pygame.Vector2(3, 10)
        ]
        self.direction = pygame.Vector2(1, 0)


class Fruit():
    def __init__(self):
        self.reposition()

    def reposition(self):
        self.x = random.randrange(0, BLOCK_NUMBER)
        self.y = random.randrange(0, BLOCK_NUMBER)
        self.apple_pos = pygame.Vector2(self.x, self.y)

    def draw(self):
        apple_rect = pygame.Rect(int(self.apple_pos.x * BLOCK_SIZE), int(self.apple_pos.y * BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE)
        WIN.blit(APPLE_MODEL, apple_rect)


def game_over():
    result_label = OUTCOME_FONT.render("Game Over", 1, RED)
    WIN.blit(result_label, (WIDTH // 2 - result_label.get_width() // 2, HEIGHT // 2 - result_label.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(500)


def handle_movement(snake, keys):
    up = keys[pygame.K_UP]
    down = keys[pygame.K_DOWN]
    left = keys[pygame.K_LEFT]
    right = keys[pygame.K_RIGHT]

    if up and not (left or right or down) and snake.direction.y != 1:  # Moving Up
        snake.direction = pygame.Vector2(0, -1)
    if down and not (right or left or up) and snake.direction.y != -1:  # Moving Down
        snake.direction = pygame.Vector2(0, 1)
    if left and not (down or right or up) and snake.direction.x != 1:  # Moving Left
        snake.direction = pygame.Vector2(-1, 0)
    if right and not (up or left or down) and snake.direction.x != -1:  # Moving Right
        snake.direction = pygame.Vector2(1, 0)

    if not (0 <= snake.snake_body[0].x < BLOCK_NUMBER) or not (0 <= snake.snake_body[0].y < BLOCK_NUMBER):
        pygame.event.post(pygame.event.Event(SNAKE_RESPAWN))
        
    for block in snake.snake_body[1:]:
        if block == snake.snake_body[0]:
            pygame.event.post(pygame.event.Event(SNAKE_RESPAWN))


def draw_window(snake, apple, score):
    # Creating grass pattern
    WIN.fill(GREEN)
    for row in range(BLOCK_NUMBER):
        if row % 2 == 0:
            for col in range(BLOCK_NUMBER):
                if col % 2 == 0:
                    grass_rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(WIN, DARK_GREEN, grass_rect)
        else:
            for col in range(BLOCK_NUMBER):
                if col % 2 != 0:
                    grass_rect = pygame.Rect(col * BLOCK_SIZE, row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(WIN, DARK_GREEN, grass_rect)

    score_label = MAIN_FONT.render(f"Score: {score}", 1, WHITE)
    WIN.blit(score_label, (10, 10))

    apple.draw()
    snake.draw()
    pygame.display.update()


def main():
    snake = Snake()
    apple = Fruit()
    score = 0

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == SNAKE_MOVE:
                snake.movement()

            if event.type == SNAKE_GROWTH:
                snake.growth = True
                score = str(len(snake.snake_body) - 2)
                EATING_SOUND.play()

            if event.type == SNAKE_RESPAWN:
                game_over()
                snake.respawn()
                score = 0

        keys = pygame.key.get_pressed()
        handle_movement(snake, keys)
        snake.collision(apple)
        draw_window(snake, apple, score)
  
    quit()

main()