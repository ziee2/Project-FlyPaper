import pygame
import sys
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import random

# Inisialisasi Pygame
pygame.init()

pygame.mixer.init()

width, height = 600, 400
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Pesawat kertas")

#sound
bgsound = pygame.mixer.Sound("E:/NgodinG/Python/kuliah/semes3/grafkom/project/sound/Intrumen Kebunbinatang.mp3")


# Inisialisasi OpenGL
glOrtho(0, width, height, 0, -1, 1)         
# glOrtho(0, width, 0, height, -1, 1)


# Karakter
bird_size = 20
bird_x = width // 4   
bird_y = height // 2
bird_speed = 4

# Pipa
pipe_width = 50
pipe_height = random.randint(50, height - 100)
pipe_x = width
pipe_speed = 4
pipe_gap = 100

# food
food_size = 10
food_x = random.randint(100, width - 100)
food_y = random.randint(50, height - 50)
food_speed = 2

# Skor
score = 0
font = pygame.font.SysFont(None, 25)

# nyawa
lives = 10
isi_nyawa = 0

mainmenu_pict = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/project/img/FlyP per.png")

bg = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/project/img/3crop.jpg")

ground = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/project/img/ground.png")

koin = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/project/img/koin.png")

ground_scroll = 0
ground_scroll_x2 = 600
scroll_speed = 3

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
    glTexCoord(0, 1)  # Sudut kiri bawah
    glVertex2f(0, -50)

    glTexCoord(1, 1)  # Sudut kiri atas
    glVertex2f(0, 120)

    glTexCoord(1, 0)  # Sudut kanan atas
    glVertex2f(600, 120)

    glTexCoord(0, 0)  # Sudut kanan bawah
    glVertex2f(600, -50)
    glEnd()


def draw_food():
    glBegin(GL_QUADS)
    glTexCoord(0, 1)
    glVertex2f(food_x, food_y)

    glTexCoord(1, 1)
    glVertex2f(food_x + food_size, food_y)

    glTexCoord(1, 0)
    glVertex2f(food_x + food_size, food_y + food_size)

    glTexCoord(0, 0)
    glVertex2f(food_x, food_y +  food_size)             
    glEnd()


def draw_bird():
    glBegin(GL_QUADS)
    glVertex2f(bird_x, bird_y)
    glVertex2f(bird_x + bird_size, bird_y)
    glVertex2f(bird_x + bird_size, bird_y + bird_size)
    glVertex2f(bird_x, bird_y + bird_size)
    glEnd()

# def draw_paper_plane():
#     # glRotate(320,0,0,1)
#     glBegin(GL_TRIANGLES)
#     # glColor3f(0.0, 1.0, 0.0)  # Warna hijau untuk pesawat kertas
#     glVertex2f(bird_x, bird_y + bird_size)
#     glVertex2f(bird_x - bird_size / 2, bird_y)
#     glVertex2f(bird_x + bird_size / 2, bird_y)
#     glVertex2f(bird_x, bird_y + bird_size)
#     glEnd()

def draw_paper_plane():
    # glRotate(320,0,0,1)
    glBegin(GL_TRIANGLES)
    glVertex2f( 160.0 , 200.0)
    glVertex2f( 131.0, 210.5)
    glVertex2f( 137.0, 213.5)

    glVertex2f( 160.0 , 200.0)
    glVertex2f( 150.0, 220.0)
    glVertex2f( 141.0, 215.5)
    # glVertex2f(, bird_y + bird_size)
    glVertex2f( 144.0, 217.0)
    glVertex2f( 140.5, 220.5)
    glVertex2f( 141.0, 215.5)

    glVertex2f( 160.0 , 200.0)
    glVertex2f( 137.0, 213.5)
    glVertex2f( 140.5, 220.5)
    glEnd()

def draw_pipe():
    glBegin(GL_QUADS)
    glVertex2f(pipe_x, 0)
    glVertex2f(pipe_x + pipe_width, 0)
    glVertex2f(pipe_x + pipe_width, pipe_height)
    glVertex2f(pipe_x, pipe_height)
    
    glVertex2f(pipe_x, pipe_height + pipe_gap)
    glVertex2f(pipe_x + pipe_width, pipe_height + pipe_gap)
    glVertex2f(pipe_x + pipe_width, height)
    glVertex2f(pipe_x, height)
    glEnd()

def draw_text(text, x, y): 
    render_text = font.render(text, True, (255, 255, 255))
    pygame.display.get_surface().blit(render_text, (x, y))

# def mainmenu_game():

# Loop permainan
clock = pygame.time.Clock()

bgsound.play()
fly = False
run = True

while run:
    # Set frame rate
    clock.tick(60)

    # screen.blit(mainmenu_pict,(0,0))
    # background
    screen.blit(bg,(0,0))
    screen.blit(ground,(ground_scroll, 50))
    screen.blit(ground,(ground_scroll_x2, 50))

    # screen.blit(koin,(food_x, food_y))

    # pygame.time.wait(10)
    ground_scroll -= scroll_speed
    ground_scroll_x2 -= scroll_speed

    if ground_scroll < -600:
        ground_scroll = 600
    if ground_scroll_x2 < -600:
        ground_scroll_x2 = 600


    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False
        elif event.type == pygame.KEYDOWN:
            fly = True

    if fly == True:
        if keys[pygame.K_SPACE]:
            bird_y -= bird_speed 
        else:
            bird_y = max(0, bird_y + bird_speed)

# Batasi agar burung tidak melewati batas bawah layar
        bird_y = min(height - bird_size, bird_y)

        pipe_x -= pipe_speed
        if pipe_x < -pipe_width:
            pipe_x = width
            pipe_height = random.randint(50, height - 100)  
            score += 1
            if score % 10 == 0:
                bird_speed += 2
                pipe_speed += 2
            
        food_x -= food_speed
        if food_x < -food_size:
            food_x = width
            food_y = random.randint(50, height - 50)
        # Deteksi makanan oleh burung
        if (
            bird_x < food_x + food_size
            and bird_x + bird_size > food_x
            and bird_y < food_y + food_size
            and bird_y + bird_size > food_y
        ):
            # Burung memakan makanan
            food_x = width + 100  # Geser makanan ke luar layar
            food_y = random.randint(50, height - 50)
            isi_nyawa += 25  # Tambahkan skor
            score += 3
            if score % 10 == 0:
                bird_speed += 2
                pipe_speed += 2
                
            if isi_nyawa == 100:
                lives += 1
                isi_nyawa = 0 
                bird_speed += 1
                pipe_speed += 1

        # Deteksi tabrakan dengan pipa
        if bird_x < pipe_x + pipe_width and bird_x + bird_size > pipe_x:
            if bird_y < pipe_height or bird_y + bird_size > pipe_height + pipe_gap:
                if bird_speed - 2 < 3 and pipe_speed - 2 < 3:
                    bird_speed = 3
                    pipe_speed = 3
                else:
                    bird_speed -= 3
                    pipe_speed -= 3

                lives -= 1
                bird_x = width // 4
                bird_y = height // 2
                # Atur ulang posisi pipa 
                pipe_x = width
                pipe_height = random.randint(50, height - 100) 
                # Tambahan: Atur ulang posisi makanan jika ada
                food_x = width + 100 
                food_y = random.randint(50, height - 50)
                # Cek apakah nyawa habis
                if lives == 0:
                    print(f"Game Over. Skor Anda: {score}")
                    pygame.quit()
                    quit()

    # Bersihkan layar
    glClear(GL_COLOR_BUFFER_BIT)

    draw_text(f"Skor    : {score}", 10, 10)
    draw_text(f"Nyawa : {lives}", 10, 30)
    draw_text(f"Speed : {bird_speed}", 10, 50)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(pygame.display.get_surface(), 'RGBA'))
    draw_ground()
    draw_background()
    glDisable(GL_TEXTURE_2D)


    # Gambar elemen-elemen permainan

    draw_pipe()
    draw_bird()
    draw_paper_plane()
    draw_food()

    # Gambar skor

    # Perbarui layar
    # pygame.display.update()
    pygame.display.flip()

    
