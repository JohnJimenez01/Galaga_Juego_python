""" Aqui se cre la ventana del juego y se crea al jugador 
se le da movimiento  """

import pygame , random
import os 

WIDTH = 800 
HEIGHT = 600 

BLACK = ( 0 , 0 , 0 )

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

class Player ( pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("./player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10 
        self.speed_x = 0 
        

    def update(self):
        self.speed_x = 0 
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5 
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0 :
            self.rect.left = 0

all_sprites = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# GAme Loop 
running = True
while running : 
    clock.tick(60)#keep loop running at the rigth speed 
    for event in pygame.event.get(): #process input (events)
        if event.type == pygame.QUIT: #check for closing window
            running = False

    #update 
    all_sprites.update()

    #Draw/ Render 

    screen.fill(BLACK)
    all_sprites.draw(screen)
    #"after" drawing everthing, flip the display.
    pygame.display.flip()

pygame.quit()


