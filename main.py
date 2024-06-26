import pygame
from pygame.locals import *
import time
import random

# global variables for size and background
SIZE = 36
BACKGROUND_COLOR = (26, 88, 25)

class Apple:
    # initializes apple
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("apple.png").convert()
        self.x = 144
        self.y = 144
    # puts apple on screen
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()
    # moves apple to next random position
    def move(self):
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,19)*SIZE
    
class Heart:
    # initializes heart
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("apple.png").convert()
        self.x = 216
        self.y = 216
    # puts heart on screen
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()
    # moves heart to next random position
    def move(self):
        self.x = random.randint(1,24)*SIZE
        self.y = random.randint(1,19)*SIZE
        
class Snake:
    # initializes snake
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = 4
        self.block = pygame.image.load("block.png").convert()
        self.x = [SIZE]*length
        self.y = [SIZE]*length
        self.direction = 'down'
    # puts snake on screen    
    def draw(self):
        self.parent_screen.fill((26, 88, 25))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()
    # moves snake different directions
    def move_left(self):
        self.direction = 'left'
    def move_right(self):
        self.direction = 'right'
    def move_up(self):
        self.direction = 'up'
    def move_down(self):
        self.direction = 'down'
        
    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
            
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        self.draw()
        
    # makes snake bigger
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
        
class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Elliot's Snake Game")
        # initializes background music
        pygame.mixer.init()
        self.play_background_music()
        
        self.surface = pygame.display.set_mode((1000,800))
        self.surface.fill((26,88,25))
        self.snake = Snake(self.surface, 4)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.heart = Heart(self.surface)
        self.heart.draw()
    
    def play_background_music(self):
        pygame.mixer.music.load('background.mp3')
        pygame.mixer.music.play(-1,0)
     
    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("crash.wav")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("ding.wav")
        elif sound_name == 'wah':
            sound = pygame.mixer.Sound("wahwah.wav")

        pygame.mixer.Sound.play(sound)
        
    def reset(self):
        self.snake = Snake(self.surface, 4)
        self.apple = Apple(self.surface)
        self.heart = Heart(self.surface)
        
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(850,10))
        
    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.heart.draw()
        self.display_score()
        pygame.display.flip()
        
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.heart.x, self.heart.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.heart.move()
            
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"
            
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundry error"
            
    def show_game_over(self):
        self.surface.fill(BACKGROUND_COLOR)
        font = pygame.font.SysFont('arial',30)
        line1 = font.render(f"Score: {self.snake.length}",True,(255,255,255))
        self.surface.blit(line1, (325,325))
        line2 = font.render("To play again press Enter!", True, (255, 255, 255))
        self.surface.blit(line2, (325,375))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False
        
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                            running = False
                            pygame.mixer.music.pause()
                            
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False
                        
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()                        
                elif event.type == QUIT:
                    running = False
                    
            try:
                if not pause:
                    self.play()
                    
            except Exception as e:
                self.show_game_over()
                self.play_sound('wah')
                pause = True
                self.reset()
                
            time.sleep(0.25)
            

if __name__ == "__main__":
    game = Game()
    game.run()
