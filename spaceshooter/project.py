import pygame
import random
import time

WIDTH = 800
HEIGHT = 600
FPS = 60

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (225, 255, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACY")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def d_text(surf, text, size, x,y):
	font = pygame.font.Font(font_name, size)
	text_surf = font.render(text, True, green)
	text_rect = text_surf.get_rect()
	text_rect.midtop = (x,y)
	surf.blit(text_surf,text_rect)

class Ship(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image=pygame.transform.scale(ship_img, (70,70))
		self.image.set_colorkey(black)
		self.rect=self.image.get_rect()
		self.radius = 30
		self.rect.centerx = WIDTH/2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0 
		self.shoot_delay = 50
		self.last_shot = pygame.time.get_ticks()
		
	
	def update(self):
		self.speedx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -8
		if keystate[pygame.K_RIGHT]:
			self.speedx = 8
		if keystate[pygame.K_SPACE]:
			self.shoot()
		self.rect.x += self.speedx
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
			
	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			bullet = Bullet(self.rect.center, self.rect.top)
			all_sprites.add(bullet)
			bullets.add(bullet)

class enemy(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = e_img
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.radius = 27
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-100,-40)
		self.speedy = random.randrange(1,8)
		self.speedx = random.randrange(-3,3)
	def update(self):
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH +20:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-100,-40)
			self.speedy = random.randrange(1,8)
	
class Bullet(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = bullet_img
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.rect.bottom = y
		self.rect.center = x
		self.speedy = -10
		
	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()
			
class explode(pygame.sprite.Sprite):
	def __init__(self, center ,size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explode_a[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 150
		
	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame  += 1
		if self.frame == len(explode_a[self.size]):
			self.kill()
		else:
			center = self.rect.center
			self.image = explode_a[self.size][self.frame]
			self.rect = self.image.get_rect()
			self.rect.center = center
		
def s_o_s():
	d_text(screen, "SPACY",64,WIDTH/2,HEIGHT/4)
	d_text(screen, "Press a key to begin", 22,WIDTH/2,HEIGHT*3/4)
	pygame.display.flip()
	time.sleep(2)
	waiting = True
	while waiting:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False
		
		
bg = pygame.image.load('bg.png').convert()
bg_rect = bg.get_rect()		
ship_img = pygame.image.load('spacy.png').convert()
e_img = pygame.image.load('e2.png','e3.png').convert()
bullet_img = pygame.image.load('laser.png').convert()
		
explode_a = {}
explode_a['lg'] = []
for i in range(9):
	filename = 'regularExplosion0{}.png'.format(i)
	img = pygame.image.load(filename).convert_alpha()
	img_lg = pygame.transform.scale(img , (70,70))
	explode_a['lg'].append(img_lg)
	
	

	
game_over = True

running = True
while running:
	if game_over:
		s_o_s()
		game_over = False
		all_sprites = pygame.sprite.Group()
		enemys = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		ship = Ship()
		all_sprites.add(ship)
		for i in range(20):
			m = enemy()
			all_sprites.add(m)
			enemys.add(m)
		score = 0
	
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	all_sprites.update()
	hits = pygame.sprite.groupcollide(enemys, bullets, True, True)
	for hit in hits:
		score += 10
		expl=explode(hit.rect.center, 'lg')
		all_sprites.add(expl)
		m = enemy()
		all_sprites.add(m)
		enemys.add(m)
	hits = pygame.sprite.spritecollide(ship, enemys, False, pygame.sprite.collide_circle)
	if hits:
		game_over = True
		
	screen.fill(black)
	screen.blit(bg,bg_rect)
	all_sprites.draw(screen)
	d_text(screen, str(score), 25,WIDTH/2,10)
	pygame.display.flip()

pygame.quit()
