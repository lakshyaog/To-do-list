import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Load images
BIRD_IMG = pygame.Surface((34, 24))
BIRD_IMG.fill((255, 255, 0))  # Yellow color for the bird
PIPE_IMG = pygame.Surface((52, 320))
PIPE_IMG.fill((0, 255, 0))  # Green color for the pipes

# Game settings
GRAVITY = 0.5
BIRD_JUMP = -10
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # Milliseconds

# Bird class
class Bird:
    def __init__(self):
        self.image = BIRD_IMG
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.velocity = 0

    def jump(self):
        self.velocity = BIRD_JUMP  # Reset velocity on jump

    def update(self):
        self.velocity += GRAVITY
        self.rect.centery += self.velocity
        if self.rect.bottom > SCREEN_HEIGHT:  # Prevent falling below the screen
            self.rect.bottom = SCREEN_HEIGHT

# Pipe class
class Pipe:
    def __init__(self):
        self.height = random.randint(150, 450)  # Random height for the top pipe
        self.top_pipe = PIPE_IMG.get_rect(topleft=(SCREEN_WIDTH, self.height - PIPE_IMG.get_height()))
        self.bottom_pipe = PIPE_IMG.get_rect(topleft=(SCREEN_WIDTH, self.height + PIPE_GAP))

    def update(self):
        self.top_pipe.x -= 3
        self.bottom_pipe.x -= 3

# Main game function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()

    bird = Bird()
    pipes = [Pipe()]
    score = 0
    game_over = False

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()
                if event.key == pygame.K_r and game_over:
                    main()

        if not game_over:
            bird.update()

            # Add new pipes
            if len(pipes) == 0 or pipes[-1].top_pipe.x < SCREEN_WIDTH - 200:
                pipes.append(Pipe())

            # Update pipes
            for pipe in pipes:
                pipe.update()
                if pipe.top_pipe.x < -PIPE_IMG.get_width():
                    pipes.remove(pipe)
                    score += 1

                # Collision detection
                if bird.rect.colliderect(pipe.top_pipe) or bird.rect.colliderect(pipe.bottom_pipe):
                    game_over = True

            # Check if bird is on the ground or above the screen
            if bird.rect.bottom >= SCREEN_HEIGHT or bird.rect.top <= 0:
                game_over = True

        # Drawing
        screen.fill(WHITE)
        screen.blit(bird.image, bird.rect)

        for pipe in pipes:
            screen.blit(PIPE_IMG, pipe.top_pipe)
            screen.blit(PIPE_IMG, pipe.bottom_pipe)

        # Display score
        font = pygame.font.SysFont(None, 36)
        score_surface = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_surface, (10, 10))

        # Game Over screen
        if game_over:
            over_font = pygame.font.SysFont(None, 48)
            over_surface = over_font.render('Game Over! Press R to Restart', True, BLACK)
            screen.blit(over_surface, (SCREEN_WIDTH // 2 - over_surface.get_width() // 2, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

