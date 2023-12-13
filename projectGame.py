import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random

# Inisialisasi
pygame.init()
pygame.mixer.init()
width, height = 600, 400
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("FlyPaper")
glOrtho(0, width, height, 0, -1, 1)

#sound
bgsound = pygame.mixer.Sound("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/sound/Intrumen Kebunbinatang.mp3")
coins_s = pygame.mixer.Sound("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/sound/sfx_coins.mp3")
sfx_gameover = pygame.mixer.Sound("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/sound/sfx_gameover.mp3")
sfx_buttuon = pygame.mixer.Sound("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/sound/sfx_button.mp3")
sfx_start = pygame.mixer.Sound("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/sound/sfx_start.mp3")
sfx_crash = pygame.mixer.Sound("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/sound/sfx_crash.mp3")

# Inisialisasi OpenGL

# Karakter
flypaper_size = 25
flypaper_x = 150
flypaper_y = 200 
flypaper_speed = 4

# Pipa
halangan_width = 40
halangan_height = random.randint(50, height - 100)
halangan_x = width
halangan_speed = 4
halangan_gap = 110

# food
koin_size = 50
koin_x = random.randint(100, width - 100)
koin_y = random.randint(50, height - 50)
koin_speed = 2

# Skor
score = 0
font = pygame.font.SysFont(None, 25)

# nyawa
lives = 2
isi_nyawa = 0

# images
mainmenu_pict = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/mainmenu.png")
bg = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/background.jpg")
ground = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/ground.png")
koin = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/koin.png")
PaperPlane = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/char.png")
gameover_pict = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/Gameover.png")
Halangan_bawah = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/halangan1.png")
Halangan_atas = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/halangan-1.png")


ground_scroll = 0
ground_scroll_x2 = 600
scroll_speed = 3

def button_MM():
    glPushMatrix()
    glBegin(GL_QUADS)
    glVertex2f(240, 140)
    glVertex2f(240, 170)
    glVertex2f(360, 170)
    glVertex2f(360, 140)
    glEnd()
    glBegin(GL_QUADS)
    glVertex2f(240, 202)
    glVertex2f(240, 232)
    glVertex2f(360, 232)
    glVertex2f(360, 202)
    glEnd()
    glBegin(GL_QUADS)
    glVertex2f(240, 266)
    glVertex2f(240, 294)
    glVertex2f(360, 294)
    glVertex2f(360, 266)
    glEnd()
    glPopMatrix()
    

def draw_background():
    glBegin(GL_QUADS)
    glTexCoord(0, 0)
    glVertex2f(0, 0)
    glTexCoord(1 , 0)
    glVertex2f(width, 0)
    glTexCoord(1, 1)
    glVertex2f(width, height)
    glTexCoord(0, 1)
    glVertex2f(0, height)
    glEnd()

def draw_ground():
    glBegin(GL_QUADS)
    glTexCoord(0, 1) 
    glVertex2f(0, -50)
    glTexCoord(1, 1) 
    glVertex2f(0, 120)
    glTexCoord(1, 0)  
    glVertex2f(600, 120)
    glTexCoord(0, 0)
    glVertex2f(600, -50)
    glEnd()

def draw_koin():
    glBegin(GL_QUADS)
    glTexCoord(0, 1)
    glVertex2f(koin_x, koin_y)
    glTexCoord(1, 1)
    glVertex2f(koin_x + koin_size, koin_y)
    glTexCoord(1, 0)
    glVertex2f(koin_x + koin_size, koin_y + koin_size)
    glTexCoord(0, 0)
    glVertex2f(koin_x, koin_y +  koin_size)             
    glEnd()

def draw_flypaper():
    glBegin(GL_QUADS)
    glVertex2f(flypaper_x, flypaper_y)
    glVertex2f(flypaper_x + flypaper_size, flypaper_y)
    glVertex2f(flypaper_x + flypaper_size, flypaper_y + flypaper_size)
    glVertex2f(flypaper_x, flypaper_y + flypaper_size)
    glEnd()

def draw_halangan():
    glBegin(GL_QUADS)
    glVertex2f(halangan_x, 0)
    glVertex2f(halangan_x + halangan_width, 0)
    glVertex2f(halangan_x + halangan_width, halangan_height)
    glVertex2f(halangan_x, halangan_height)
    
    glVertex2f(halangan_x, halangan_height + halangan_gap)
    glVertex2f(halangan_x + halangan_width, halangan_height + halangan_gap)
    glVertex2f(halangan_x + halangan_width, height)
    glVertex2f(halangan_x, height)
    glEnd()

def draw_text(text, x, y): 
    render_text = font.render(text, True, (255, 255, 255))
    pygame.display.get_surface().blit(render_text, (x, y))

def game_over():
    sfx_gameover.play()
    global collision, game_state
    if gameover:
        collision = True
        game_state = "game_over"
        screen.blit(gameover_pict,(0,0))

def is_button_clicked(x, y, button_x, button_y, button_width, button_height):
    return (
        x >= button_x and
        x <= button_width and
        y >= button_y and
        y <= button_height
    )

def resetgame():
    global flypaper_x, flypaper_y, halangan_x, halangan_height, koin_x, koin_y, flypaper_speed, halangan_speed, lives
    flypaper_x = width // 4
    flypaper_y = height // 2 
    halangan_x = width
    halangan_height = random.randint(50, height - 100) 
    koin_x = width + 100 
    koin_y = random.randint(50, height - 50)
    if lives == 0:
        lives = 2
        isi_nyawa = 0

clock = pygame.time.Clock()

fly = False
run = True
collision = True
paused = False
menu = True
game_state = "main_menu"

while run:
    clock.tick(60)
    if menu:
        collision = True
        game_state = "main_menu"
        screen.blit(mainmenu_pict,(0,0))

    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and collision == True:
            if is_button_clicked(event.pos[0], event.pos[1], 240, 266, 360, 294):
                sfx_buttuon.play()
                if game_state == "game_over":
                    gameover = False
                    menu = True
                
            if is_button_clicked(event.pos[0], event.pos[1], 240, 140, 360, 170):
                sfx_buttuon.play()
                if game_state == "main_menu":
                    sfx_start.play()
                    menu = False
                    volume = 0.5
                    bgsound.set_volume(volume)
                    bgsound.play()
                    fly = True
                
            if is_button_clicked(event.pos[0], event.pos[1], 240, 204, 360, 234):
                sfx_buttuon.play()
                if game_state == "game_over":
                    sfx_start.play()
                    gameover = False
                    fly = True
                    volume = 0.5
                    bgsound.set_volume(volume)
                    bgsound.play()
                if game_state == "main_menu":
                    pygame.quit()
                    quit()

    if fly:
        collision = False

        if keys[pygame.K_SPACE]:
            flypaper_y -= flypaper_speed

        else:
            flypaper_y = max(0, flypaper_y + flypaper_speed)

        # Batasi agar burung tidak melewati batas layar
        flypaper_y = min(height - flypaper_size, flypaper_y)
        flypaper_y = max(0, flypaper_y)

        ground_scroll -= scroll_speed
        ground_scroll_x2 -= scroll_speed

        if ground_scroll < -600:
            ground_scroll = 600
        if ground_scroll_x2 < -600:
            ground_scroll_x2 = 600

        pipe = halangan_height + halangan_gap
        p1 = 350 - halangan_height

        screen.blit(bg,(0,0))
        screen.blit(ground,(ground_scroll, 75))
        screen.blit(ground,(ground_scroll_x2, 75))
        screen.blit(PaperPlane,(flypaper_x,flypaper_y))
        screen.blit(koin,(koin_x, koin_y))
        screen.blit(Halangan_bawah,(halangan_x, pipe))
        screen.blit(Halangan_atas,(halangan_x, -p1))
        
        pygame.time.wait(10)

        koin_x -= koin_speed
        if koin_x < -koin_size:
            koin_x = width
            koin_y = random.randint(50, height - 50)
        if (
            flypaper_x < koin_x + koin_size
            and flypaper_x + flypaper_size > koin_x
            and flypaper_y < koin_y + koin_size
            and flypaper_y + flypaper_size > koin_y
        ):
            coins_s.play()
            koin_x = width + 100
            koin_y = random.randint(50, height - 50)
            isi_nyawa += 25 
            score += 1
            if score % 10 == 0:
                flypaper_speed += 1
                halangan_speed += 1
                
            if isi_nyawa == 100:
                lives += 1
                isi_nyawa = 0 
                flypaper_speed += 1
                halangan_speed += 1

        halangan_x -= halangan_speed
        if halangan_x < -halangan_width:
            halangan_x = width
            halangan_height = random.randint(50, height - 100)  
            score += 1
            if score % 10 == 0:
                flypaper_speed += 1
                halangan_speed += 1

        if flypaper_x < halangan_x + halangan_width and flypaper_x + flypaper_size > halangan_x:
            if flypaper_y < halangan_height or flypaper_y + flypaper_size > halangan_height + halangan_gap:
                sfx_crash.play()
                if flypaper_speed - 2 <= 3 and halangan_speed - 2 <= 3:
                    flypaper_speed = 4
                    halangan_speed = 4
                else:
                    flypaper_speed -= 2
                    halangan_speed -= 2
                lives -= 1
                if lives == 0:
                    bgsound.stop()
                    print(f"Game Over. Skor Anda: {score}")
                    fly = False
                    gameover = True
                    game_over()

                resetgame()
            
    glClear(GL_COLOR_BUFFER_BIT)

    if fly == True:
        draw_text(f"Skor    : {score}", 10, 10)
        draw_text(f"Nyawa : {lives}", 10, 30)
        # draw_text(f"Speed : {flypaper_speed}", 10, 50)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(pygame.display.get_surface(), 'RGBA'))
    draw_background()
    # draw_halangan()
    # draw_flypaper()
    # button_MM()
    glDisable(GL_TEXTURE_2D)

    pygame.display.flip()