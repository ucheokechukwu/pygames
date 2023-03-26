# Initialization

import pygame
from pygame.locals import *
import sys
import random
from tkinter import *
from tkinter import filedialog
print(Tk())

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

class Castle(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.hide = False
		self.image = pygame.image.load("./rpg_images/Castle.png")

	def render(self):
		if self.hide == False:
			screen.blit(self.image, (400,80))

class EventHandler():
	def __init__(self):
		self.enemy_count = 0
		self.battle = False
		#enemy generation
		self.enemy_generation = pygame.USEREVENT + 1
		self.stage_enemies =[]
		# formula to calculate the number of enemies in each level
		for x in range(1,21):
			self.stage_enemies.append(int(x**2 / 2  +  1))
			
	def stage_handler(self):
		# code for the Tkinter stage selection window
		self.root = Tk()
		self.root.geometry('200x170')

		button1 = Button(self.root, text='Twilight Dungeon',
									width=18,
									height=2,
									command=self.world1)
		button2 = Button(self.root, text='Skyward Dungeon',
									width=18,
									height=2,
									command=self.world2)			
		button3 = Button(self.root, text='Hell Dungeon',
									width=18,
									height=2,
									command=self.world3)
		button1.place(x=40,y=15)
		button2.place(x=40,y=65)
		button3.place(x=40,y=115)
		
		self.root.mainloop()
		print ("Buttons")

	def world1(self):
		self.root.destroy()
		pygame.time.set_timer(self.enemy_generation, 2000)
		castle.hide = True
		self.battle = True

	def world2(self):
		self.battle = True
		pass

	def world3(self):
		self.battle = True
		pass

# Main Game 

# Instancing the objects
background = Background()
ground = Ground()
castle = Castle()
handler = EventHandler()




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
				
			if event.key == pygame.K_e: # and (450 < player.rect.x < 550):
			# the above code checks to see the player is near the Castle entrace when 'e' is pressed
				handler.stage_handler()
				



	#Moves
	player.update()
	if player.attacking == True:
		player.attack()
	player.move()


	# Rendering
	pygame.display.update()
	background.render()
	ground.render()
	castle.render()
	player.render()


	frames_per_second.tick(60)
