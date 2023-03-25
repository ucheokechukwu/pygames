# imports
import pygame
from pygame.locals import *
import sys
import random 
import time

# initializing
pygame.init()

# setting up frame per second
FPS = pygame.time.Clock()

# Predefine some colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (127,127, 0)

# other constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
speed = 5
score = 0

# setting up fonts
font = pygame.font.SysFont('Menlo', 60)
font_small = pygame.font.SysFont('Menlo', 20)
game_over = font.render("GAME OVER", True, BLACK)
background = pygame.image.load("AnimatedStreet.png")

# create a white screen
SCREEN = pygame.display.set_mode((400,600))
SCREEN.fill(WHITE)
pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("Enemy.png")
		self.rect = self.image.get_rect()
		self.rect.center = (random.randint(40, SCREEN_WIDTH-40),0)
 
	def move(self):
		global score
		self.rect.move_ip(0,speed)
		if (self.rect.bottom > SCREEN_HEIGHT):
			score += 1
			self.rect.top = 0
			self.rect.center = (random.randint(30, 370),0)

	def draw(self, surface):
		surface.blit(self.image, self.rect)

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("Player.png")
		self.rect = self.image.get_rect()
		self.rect.center = (160, 520)

	def move(self):
		pressed_keys = pygame.key.get_pressed()
		
		if self.rect.left > 0:
			if pressed_keys[K_LEFT]:
				self.rect.move_ip(-5,0)
		if self.rect.right < SCREEN_WIDTH:
			if pressed_keys[K_RIGHT]:
				self.rect.move_ip(5,0)

	def draw(self, surface):
		surface.blit(self.image, self.rect)

# setting up sprites

P1 = Player()
E1 = Enemy()

enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(E1)
all_sprites.add(P1)


# Adding a user event
inc_speed = pygame.USEREVENT + 1
pygame.time.set_timer(inc_speed, 1000)


# Game loop

while True:

	# cycle through all the events
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

		if event.type == inc_speed:
			speed += 0.5


	# Rendering
	SCREEN.blit(background, (0,0))
	scores = font_small.render(str(score), True, BLACK)
	SCREEN.blit(scores, (10,10))

	# moves and redraws sprites
	for entity in all_sprites:
		entity.draw(SCREEN)
		entity.move()

	# collision control
	if pygame.sprite.spritecollideany(P1, enemies):
		pygame.mixer.Sound('crash.wav').play()
		time.sleep(0.5)

		SCREEN.fill(RED)
		SCREEN.blit(game_over,(30,250))

		pygame.display.update()
		for entity in all_sprites:
			entity.kill()
		time.sleep(2)
		pygame.quit()
		sys.exit()

	pygame.display.update()
	FPS.tick(60)

