# initialization and constants
import sys
import random
import pygame
from pygame import *

# pygame.init()

vec = pygame.math.Vector2 # 2 for 2 dimensional
HEIGHT = 600
WIDTH = 600
acceleration = 0.5 #acceleration
friction = -0.12 #friction
frames_per_second = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

pygame.init()


# player and platform classes

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		
		self.surf = pygame.Surface((30,30))
		self.surf.fill((128,255,40))
		self.rect = self.surf.get_rect()
		
		self.pos = vec((10,HEIGHT-90))
		self.velocity = vec(0,0)
		self.acceleration = vec(0,0)		

	def move(self):
		self.acceleration = vec(0,0.5) #0.5 gives vertical acceleration i.e. gravity
		pressedkeys = pygame.key.get_pressed()
		if pressedkeys[K_LEFT]:
			self.acceleration.x = -acceleration
		if pressedkeys[K_RIGHT]:
			self.acceleration.x = acceleration

		self.acceleration.x += self.velocity.x * friction
		self.velocity += self.acceleration
		self.pos += self.velocity + 0.5*self.acceleration

		if self.pos.x > WIDTH:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = WIDTH

#		if self.pos.y > HEIGHT:
#			self.pos.y = 0
#		if self.pos.y < 0:
#			self.pos.y = HEIGHT

		self.rect.midbottom = self.pos

	def jump(self):
		hits = pygame.sprite.spritecollide(self, platforms, dokill=False)
		# only allows jumping if the player is already on a platform
		self.velocity.y = -15 if hits else self.velocity.y 

	def update(self):
		hits = pygame.sprite.spritecollide(self, platforms, dokill=False)
		if hits and self.velocity.y>0:
			self.pos.y = hits[0].rect.top +1 # relocates the player to the top of first platform hit
			self.velocity.y = 0

class Platform(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.surf = pygame.Surface((random.randint(80,150), 12))
		self.surf.fill((255,0,0))
		self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH-10),
											random.randint(0, HEIGHT-30)))



def platform_generator():
	while len(platforms) <20:
		p = platform()
		p.rect.center = (random.randrange(0, WIDTH - (random.randrange(50,100))),
						random.randrange(-50,0)
						)
		platforms.add(p)
		all_sprites.add(p)


# sprites group
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

# create player sprite
player_1 = Player()
all_sprites.add(player_1)

# create base/1st platform sprite
platform_1 = Platform()
platform_1.surf = pygame.Surface((WIDTH,20))
platform_1.surf.fill((127,127,0))
platform_1.rect = platform_1.surf.get_rect(center = (WIDTH/2, HEIGHT-10))

platforms.add(platform_1)
all_sprites.add(platform_1)

# randomly generate 6-9 platforms
for _ in range(random.randint(6,9)):
	new_platform = Platform()
	platforms.add(new_platform)
	all_sprites.add(new_platform)





# game loop

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player_1.jump() 

	# scrolling loop
	if player_1.rect.top < HEIGHT/3:
		player_1.pos.y += abs(player_1.velocity.y)	
		
		# as the player goes up, the platforms go down, giving the impression of scrolling
		for plat in platforms:
			plat.rect.y += abs(player_1.velocity.y)
			if plat.rect.y > HEIGHT:
				plat.kill()
				new_plat = Platform()
				platforms.add(new_plat)
				all_sprites.add(new_plat)

		# generating a new platform if an old one is killed
	


	screen.fill((0,0,0))

	for entity in all_sprites:
		screen.blit(entity.surf, entity.rect)

	pygame.display.update()

	frames_per_second.tick(60)
	player_1.move()
	player_1.update()
