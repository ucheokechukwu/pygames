# Initialization

import pygame
from pygame.locals import *
import sys
import random
from tkinter import *
from tkinter import filedialog


pygame.init()
vec = pygame.math.Vector2
frames_per_second = pygame.time.Clock()
HEIGHT = 350
WIDTH = 700

ACC = 0.3
FRICTION = -0.1

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


# Animations
# running animation
run_animation_R = [pygame.image.load("./rpg_images/Player_Sprite_R.png"), 
				pygame.image.load("./rpg_images/Player_Sprite2_R.png"),
				pygame.image.load("./rpg_images/Player_Sprite3_R.png"),
				pygame.image.load("./rpg_images/Player_Sprite4_R.png"),
				pygame.image.load("./rpg_images/Player_Sprite5_R.png"),
				pygame.image.load("./rpg_images/Player_Sprite6_R.png"),
				pygame.image.load("./rpg_images/Player_Sprite_R.png")]


run_animation_L = [pygame.image.load("./rpg_images/Player_Sprite_L.png"), 
				pygame.image.load("./rpg_images/Player_Sprite2_L.png"),
				pygame.image.load("./rpg_images/Player_Sprite3_L.png"),
				pygame.image.load("./rpg_images/Player_Sprite4_L.png"),
				pygame.image.load("./rpg_images/Player_Sprite5_L.png"),
				pygame.image.load("./rpg_images/Player_Sprite6_L.png"),
				pygame.image.load("./rpg_images/Player_Sprite_L.png")]

# attacking animation
attack_animation_R = [pygame.image.load("./rpg_images/Player_Sprite_R.png"), 
                pygame.image.load("./rpg_images/Player_Attack_R.png"),
                pygame.image.load("./rpg_images/Player_Attack2_R.png"),
                pygame.image.load("./rpg_images/Player_Attack2_R.png"),
                pygame.image.load("./rpg_images/Player_Attack3_R.png"),
                pygame.image.load("./rpg_images/Player_Attack3_R.png"),
                pygame.image.load("./rpg_images/Player_Attack4_R.png"),
                pygame.image.load("./rpg_images/Player_Attack4_R.png"),
                pygame.image.load("./rpg_images/Player_Attack5_R.png"),
                pygame.image.load("./rpg_images/Player_Attack5_R.png"),
                pygame.image.load("./rpg_images/Player_Sprite_R.png")]
 
# Attack animation for the LEFT
attack_animation_L = [pygame.image.load("./rpg_images/Player_Sprite_L.png"), 
                pygame.image.load("./rpg_images/Player_Attack_L.png"),
                pygame.image.load("./rpg_images/Player_Attack2_L.png"),
                pygame.image.load("./rpg_images/Player_Attack2_L.png"),
                pygame.image.load("./rpg_images/Player_Attack3_L.png"),
                pygame.image.load("./rpg_images/Player_Attack3_L.png"),
                pygame.image.load("./rpg_images/Player_Attack4_L.png"),
                pygame.image.load("./rpg_images/Player_Attack4_L.png"),
                pygame.image.load("./rpg_images/Player_Attack5_L.png"),
                pygame.image.load("./rpg_images/Player_Attack5_L.png"),
                pygame.image.load("./rpg_images/Player_Sprite_L.png")]

# Classes

class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("./rpg_images/Player_Sprite_R.png")
		self.rect = self.image.get_rect()
		# position and direction
		self.vx = 0
		self.pos = vec((340,240))
		self.velocity = vec((0,0))
		self.acceleration = vec((0,0))
		self.direction = 'RIGHT'
		self.jumping = False
		self.running = False
		self.attacking = False
		self.cooldown = False
		self.move_frame = 0
		self.attack_frame = 0


	def move(self):
		self.running = True if abs(self.velocity.x) > 0.3 else False
		self.acceleration = vec((0,0.5))		
		pressedkeys = pygame.key.get_pressed()
		if pressedkeys[K_LEFT]:
			self.acceleration.x = -ACC
		if pressedkeys[K_RIGHT]:
			self.acceleration.x = ACC	

		self.acceleration.x += self.velocity.x * FRICTION
		self.velocity += self.acceleration
		self.pos += self.velocity + 0.5*self.acceleration
		#warping

		if self.pos.x > WIDTH:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = WIDTH
		self.rect.midbottom = self.pos

	def update(self):	
		# controls the animation of the player
		# 1. moves to the next frame if the player is running
		if not self.jumping and self.running:
			self.move_frame += 1
			if self.velocity.x > 0:
				self.image = run_animation_R[self.move_frame]
				self.direction = 'RIGHT'
			else:
				self.image = run_animation_L[self.move_frame]
				self.direction = 'LEFT'
		# 2. return to base frame when it has cycled through the 7 frames
		if self.move_frame == 6:
			self.move_frame = 0
			return
		# 3. return to base frame if the player is almost stationary
		if abs(self.velocity.x) < 0.2 and self.move_frame != 0:
			self.move_frame = 0
			if self.direction == 'RIGHT':
				self.image = run_animation_R[self.move_frame]
			elif self.direction == 'LEFT':
				self.image = run_animation_L[self.move_frame]
				 

	def jump(self):	
		self.rect.x += 1
		# check if in contact with the ground
		hits = pygame.sprite.spritecollide(player, grounds, dokill=False)
		self.rect.x -=1 # this was changed to check for collision then changed back

		if hits and not self.jumping:
			self.jumping = True
			self.velocity.y = -12

	def attack(self):
		# cycle to the next frame depending on direction
		if self.direction == 'LEFT':
			self.image = attack_animation_L[self.attack_frame]
			self.correction()
		else:
			self.image = attack_animation_R[self.attack_frame]
		# update the frame
		self.attack_frame += 1
		# cycle back to 0 if it has cycled through 10 frames
		if self.attack_frame == 10:
			self.attack_frame = 0
			self.attacking = False

	def correction(self):
		# used to correct an error in left position frame
		if self.attack_frame == 1:
			self.pos.x -=20
		if self.attack_frame == 10:
			self.pos.x +=20


	def gravity_check(self):
		hits = pygame.sprite.spritecollide(player, grounds, dokill=False)
		if self.velocity.y > 0 and hits:
			
			if self.pos.y < hits[0].rect.bottom:
				
				self.pos.y = ground.rect.y + 1  
				self.velocity.y = 0
				self.jumping = False

	def hit(self):
		if not self.cooldown:
			self.cooldown == True
			pygame.time.set_timer(hit_cooldown, 0)
			print('hit')

	def render(self):
		screen.blit(self.image, self.rect)

class Enemy(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("./rpg_images/Enemy.png")
		self.rect = self.image.get_rect()
		self.pos = vec((0,0))
		self.velocity = vec((0,0))
		
		# initial direction
		self.direction = random.choice(['RIGHT','LEFT']) # 0 for Right, 1 for Left
		self.velocity.x = random.randint(2,6)
		self.pos.x = 0 if self.direction == 'RIGHT' else 700
		self.pos.y = 235

	def move(self):
		# switch directions at the boundary
		if self.pos.x >= (WIDTH-20):
			self.direction = 'LEFT'
		if self.pos.x <= 20:
			self.direction = 'RIGHT' 
		
		if self.direction == 'RIGHT':
			self.pos.x += self.velocity.x
		else:
			self.pos.x -= self.velocity.x 
		# bind the rect to the image
		self.rect.center = self.pos

	def update(self):
		hit_player = pygame.sprite.spritecollide(self, players, dokill=False)
		if hit_player and player.attacking and player.direction !=self.direction:
			self.kill()
		#	sys.exit(0)
		elif hit_player and not player.attacking:
			player.hit()
		else:
			pass

	def render(self):
		screen.blit(self.image, (self.pos.x, self.pos.y))


class Background(pygame.sprite.Sprite):

	def __init__(self):
		super().__init__()
		self.bgimg = pygame.image.load("./rpg_images/Background.png")
		self.bgY = 0
		self.bgX = 0

	def render(self):
		screen.blit(self.bgimg, (self.bgX, self.bgY))

class Ground(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("./rpg_images/Ground.png")
		self.rect = self.image.get_rect(center=(350,350))

	def render(self):
		screen.blit(self.image, (self.rect.x, self.rect.y))

# Main Game 

# Instancing the objects
background = Background()
ground = Ground()
player = Player()
enemy = Enemy()

# Creating groups and adding instances to groups
grounds = pygame.sprite.Group()
grounds.add(ground)

players = pygame.sprite.Group()
players.add(player)

enemies = pygame.sprite.Group()
enemies.add(enemy)

# Functions




# User-defined events
hit_cooldown = pygame.USEREVENT + 1




# Game Loop

while True:
	player.gravity_check() 

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pass

		if event.type == hit_cooldown:
			player.cooldown = False
			pygame.time.set_timer(hit_cooldown,0)
		
		if event.type == pygame.KEYDOWN:
			
			if event.key == pygame.K_SPACE:
				player.jump()
			
			if event.key == pygame.K_RETURN:
				if player.attacking == False:
					player.attacking = True
					player.attack()
	
	#Moves
	player.update()
	if player.attacking == True:
		player.attack()
	player.move()
	enemy.move()
	enemy.update()

	# Rendering
	pygame.display.update()
	background.render()
	ground.render()
	player.render()
	enemy.render()

	frames_per_second.tick(60)
