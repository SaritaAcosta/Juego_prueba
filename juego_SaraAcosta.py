#Creado por Sara Valeria Acosta
#contacto: +57 3112001543
#El juego es un juego sencillo de disparos a enemigos
#cuenta con 2 menus: menu principal y la pantalla de fin de juego
#se usan las flechas del teclado para mover al jugador
import pygame
import random

# Iniciar Pygame
pygame.init()

# Configuración de ventana
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego disparar")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
# posición y movimiento jugador
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
#disparo del jugador
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Enemigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randrange(1, 4)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed = random.randrange(1, 4)

# Bala de disparo
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 14))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed = -10
#movimiento y posición de disparo
    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Estados del juego
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Funciones de estados del juego

#menu de inicio
def show_menu():
    window.fill(BLACK)
    
    # Título
    title_font = pygame.font.Font(None, 64)
    title = title_font.render("Dispara a los enemigos!", True, WHITE)
    title_rect = title.get_rect(centerx=WIDTH//2, y=HEIGHT//6)
    window.blit(title, title_rect)
    
    # Instrucciones
    instructions_font = pygame.font.Font(None, 25)
    instructions = instructions_font.render("Dispara con ESPACIO y te mueves con las flechas, si un enemigo te toca, se acabó el juego", True, WHITE)
    instructions_rect = instructions.get_rect(centerx=WIDTH//2, y=HEIGHT//2 - 50)
    window.blit(instructions, instructions_rect)
    
    # Mensaje para iniciar
    start_font = pygame.font.Font(None, 32)
    start = start_font.render("Presiona ESPACIO para iniciar", True, WHITE)
    start_rect = start.get_rect(centerx=WIDTH//2, y=HEIGHT//2 + 50)
    window.blit(start, start_rect)
    
    pygame.display.flip()

#Ventana de juego terminado
def show_game_over(score):
    window.fill(BLACK)
    font = pygame.font.Font(None, 64)
    title = font.render("Game Over: Te comieron", True, WHITE)
    window.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
    
    font = pygame.font.Font(None, 32)
    score_text = font.render(f"Enemigos asesinados: {score}", True, WHITE)
    window.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    
    restart = font.render("Preisona ESPACIO para jugar de nuevo", True, WHITE)
    window.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT*3//4))
    
    pygame.display.flip()

# Se inician los grupos
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Creación de jugador
player = Player()
all_sprites.add(player)

# Pantalla de inicio
running = True
game_state = MENU
clock = pygame.time.Clock()
score = 0

while running:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == MENU:
                    game_state = PLAYING
                    # Aparición de enemigos
                    for _ in range(8):
                        enemy = Enemy()
                        all_sprites.add(enemy)
                        enemies.add(enemy)
                elif game_state == PLAYING:
                    player.shoot()
                elif game_state == GAME_OVER:
                    # Reiniciar juego
                    game_state = PLAYING
                    all_sprites.empty()
                    enemies.empty()
                    bullets.empty()
                    player = Player()
                    all_sprites.add(player)
                    score = 0
                    for _ in range(5):
                        enemy = Enemy()
                        all_sprites.add(enemy)
                        enemies.add(enemy)

    if game_state == MENU:
        show_menu()
    elif game_state == PLAYING:
        # Update
        all_sprites.update()

        # Acierto de disparos
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 1
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        hits = pygame.sprite.spritecollide(player, enemies, False)
        if hits:
            game_state = GAME_OVER

        #Fondo de juego
        window.fill(BLACK)
        all_sprites.draw(window)
        
        # Puntaje en pantalla
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Enemigos muertos: {score}", True, WHITE)
        window.blit(score_text, (10, 10))
        
        pygame.display.flip()
    elif game_state == GAME_OVER:
        show_game_over(score)

pygame.quit()