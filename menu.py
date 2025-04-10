# Se importan módulos necesarios
import pygame, random
import os

# Definición de constantes de pantalla y colores
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Ruta para acceder a la carpeta de imágenes
ROOT_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(ROOT_DIR, 'assets')

# Se inician las librerías de Pygame
pygame.init()
pygame.mixer.init()

# Configuración de la ventana del juego
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()  # Reloj para controlar FPS

# Función para dibujar texto en pantalla
def draw_text(surface, text, size, x, y):
	font = pygame.font.SysFont("serif", size)  # Fuente
	text_surface = font.render(text, True, WHITE)  # Renderizado del texto
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)  # Posicionamiento del texto
	surface.blit(text_surface, text_rect)  # Mostrar en pantalla

# Función para dibujar barra de escudo
def draw_shield_bar(surface, x, y, percentage):
	BAR_LENGHT = 100
	BAR_HEIGHT = 10
	fill = (percentage / 100) * BAR_LENGHT  # Porcentaje de escudo
	border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
	fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
	pygame.draw.rect(surface, GREEN, fill)  # Barra verde
	pygame.draw.rect(surface, WHITE, border, 2)  # Borde blanco

# Clase para el jugador
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load(os.path.join(IMAGE_DIR,"player.png")).convert()
		self.image.set_colorkey(BLACK)  # Elimina fondo negro
		self.rect = self.image.get_rect()
		self.rect.centerx = WIDTH // 2  # Centro horizontal
		self.rect.bottom = HEIGHT - 10  # Posición inicial en la parte inferior
		self.speed_x = 0
		self.speed_y = 0
		self.shield = 100  # Escudo inicial

	def update(self):
		self.speed_x = 0
		self.speed_y = 0
		keystate = pygame.key.get_pressed()

		# Movimiento horizontal y vertical con teclas flecha
		if keystate[pygame.K_LEFT]:
			self.speed_x = -5
		if keystate[pygame.K_RIGHT]:
			self.speed_x = 5
		if keystate[pygame.K_UP]:
			self.speed_y = -5
		if keystate[pygame.K_DOWN]:
			self.speed_y = 5

		# Aplicar movimiento
		self.rect.x += self.speed_x
		self.rect.y += self.speed_y

		# Limitar movimiento a los bordes de la pantalla
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0
		if self.rect.top < 0:
			self.rect.top = 0
		if self.rect.bottom > HEIGHT:
			self.rect.bottom = HEIGHT

	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)  # Crear bala en posición actual
		all_sprites.add(bullet)
		bullets.add(bullet)
		laser_sound.play()  # Sonido de disparo con un ligero eco

# Clase para meteoritos enemigos
class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = random.choice(meteor_images)  # Imagen aleatoria de meteoro
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-140, -100)  # Aparecen fuera de pantalla
		self.speedy = random.randrange(1, 10)
		self.speedx = random.randrange(-5, 5)

	def update(self):
		self.rect.y += self.speedy
		self.rect.x += self.speedx
		# Si sale de la pantalla, reaparece arriba
		if self.rect.top > HEIGHT + 10 or self.rect.left < -40 or self.rect.right > WIDTH + 40:
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-140, - 100)
			self.speedy = random.randrange(1, 10)

# Clase para las balas disparadas
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		super().__init__()
		self.image = pygame.image.load(os.path.join(IMAGE_DIR,"laser1.png"))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.y = y
		self.rect.centerx = x
		self.speedy = -10  # Movimiento hacia arriba

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:  # Si sale de pantalla, se destruye
			self.kill()

# Clase para animación de explosiones
class Explosion(pygame.sprite.Sprite):
	def __init__(self, center):
		super().__init__()
		self.image = explosion_anim[0]  # Primer cuadro de la animación
		self.rect = self.image.get_rect()
		self.rect.center = center 
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 50  # Tiempo entre cuadros

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim):  # Fin de la animación
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

# Mostrar pantalla de inicio o game over
def show_go_screen():
	screen.blit(background, [0, 0])
	if 'score' in globals():  # Si ya se jugó una partida
		draw_text(screen, f"Puntaje final: {score}", 40, WIDTH // 2, HEIGHT // 2)
	else:  # Pantalla de inicio
		draw_text(screen, "SHOOTER", 65, WIDTH // 2, HEIGHT // 4)
		draw_text(screen, "¡Dispara a los meteoritos y sobrevive!", 27, WIDTH // 2, HEIGHT // 2)
		draw_text(screen, "Usa las flechas para moverte y SPACE para disparar", 20, WIDTH // 2, HEIGHT // 2 + 30)
		draw_text(screen, "Presiona cualquier tecla para comenzar", 20, WIDTH // 2, HEIGHT * 3/4)
	
	pygame.display.flip()

	waiting = True
	while waiting:  # Espera hasta que se presione una tecla
		clock.tick(60)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.KEYUP:
				waiting = False

# Cargar imágenes de meteoritos
# Aunque todos dicen grey hay meteoritos de color cafe (brown)
meteor_images = []
meteor_list = ["meteorGrey_big1.png", "meteorGrey_big2.png", "meteorGrey_big3.png", "meteorGrey_big4.png",
			   "meteorGrey_med1.png", "meteorGrey_med2.png", "meteorGrey_small1.png", "meteorGrey_small2.png",
			   "meteorGrey_tiny1.png", "meteorGrey_tiny2.png"]
for img in meteor_list:
	meteor_images.append(pygame.image.load(os.path.join(IMAGE_DIR, img)).convert())

# Cargar imágenes de explosión
explosion_anim = []
for i in range(9):
	file = "regularExplosion0{}.png".format(i)
	img = pygame.image.load(os.path.join(IMAGE_DIR, file)).convert()
	img.set_colorkey(BLACK)
	img_scale = pygame.transform.scale(img, (70,70))  # Redimensionar
	explosion_anim.append(img_scale)

# Cargar imagen de fondo
background = pygame.transform.scale(
	pygame.image.load(os.path.join(IMAGE_DIR, "background.png")).convert(),
	(WIDTH, HEIGHT)
)

# Cargar efectos de sonido
laser_sound = pygame.mixer.Sound(os.path.join(IMAGE_DIR, "laser5.ogg"))
explosion_sound = pygame.mixer.Sound(os.path.join(IMAGE_DIR, "explosion.wav"))

# Cargar música de fondo
pygame.mixer.music.load(os.path.join(IMAGE_DIR,"music.ogg"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)  # Música en bucle

# Variables para controlar el juego
game_over = True
running = True

# Bucle principal del juego
while running:
	if game_over:
		show_go_screen()
		game_over = False
		all_sprites = pygame.sprite.Group()
		meteor_list = pygame.sprite.Group()
		bullets = pygame.sprite.Group()

		player = Player()
		all_sprites.add(player)

		# Crear meteoritos
		for i in range(8):
			meteor = Meteor()
			all_sprites.add(meteor)
			meteor_list.add(meteor)

		score = 0  # Reiniciar puntuación

	clock.tick(60)  # FPS
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				player.shoot()  # Disparo al presionar espacio

	all_sprites.update()  # Actualizar todos los sprites

	# Colisiones entre balas y meteoritos
	hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
	for hit in hits:
		score += 10
		explosion_sound.play()
		explosion = Explosion(hit.rect.center)
		all_sprites.add(explosion)
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)

	# Colisiones entre jugador y meteoritos
	hits = pygame.sprite.spritecollide(player, meteor_list, True)
	for hit in hits:
		player.shield -= 25
		meteor = Meteor()
		all_sprites.add(meteor)
		meteor_list.add(meteor)
		if player.shield <= 0:
			game_over = True  # Fin del juego

	# Dibujar todo en pantalla
	screen.blit(background, [0, 0])
	all_sprites.draw(screen)
	draw_text(screen, str(score), 25, WIDTH // 2, 10)  # Mostrar puntuación
	draw_shield_bar(screen, 5, 5, player.shield)  # Barra de escudo

	pygame.display.flip()  # Actualizar pantalla

# Salir del juego
pygame.quit()
