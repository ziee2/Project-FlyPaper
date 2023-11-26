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
bgsound = pygame.mixer.Sound("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/sound/Intrumen Kebunbinatang.mp3")

jump_s = pygame.mixer.Sound("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/sound/Jump_s.mp3")

# Inisialisasi OpenGL
glOrtho(0, width, height, 0, -1, 1)         
# glOrtho(0, width, 0, height, -1, 1)


# Karakter
bird_size = 30
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
food_size = 50
food_x = random.randint(100, width - 100)
food_y = random.randint(50, height - 50)
food_speed = 2

# Skor
score = 0
font = pygame.font.SysFont(None, 25)

# nyawa
lives = 2
isi_nyawa = 0

# images
mainmenu_pict = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/FlyP per.png")
bg = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/3crop.jpg")
ground = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/ground.png")
koin = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/koin50.png")
pause = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/pause.png")
PaperPlane = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/pesawat.png")
pohon = pygame.image.load("E:/NgodinG/Python/kuliah/semes3/grafkom/Project_Flypaper/img/1.png")

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
    

def is_button_clicked(x, y, button_x, button_y, button_width, button_height):
    return (
        x >= button_x and
        x <= button_width and
        y >= button_y and
        y <= button_height
    )


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

def resetgame():
    global bird_x, bird_y, pipe_x, pipe_height, food_x, food_y, bird_speed, pipe_speed, lives
    bird_x = width // 4
    bird_y = height // 2 
    # Atur ulang posisi pipa 
    pipe_x = width
    pipe_height = random.randint(50, height - 100) 
    # Tambahan: Atur ulang posisi makanan jika ada
    food_x = width + 100 
    food_y = random.randint(50, height - 50)
    if lives == 0:
        lives = 2
        isi_nyawa = 0

clock = pygame.time.Clock()

# bgsound.play()
fly = False
run = True
show_menu = True
paused = False

while run:
    # Set frame rate
    
    clock.tick(60)

    if show_menu:
        menu = True
        screen.blit(mainmenu_pict,(0,0))

    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and show_menu == True:
            if is_button_clicked(event.pos[0], event.pos[1], 240, 266, 360, 294):
                pygame.quit()
                quit()
                
            elif is_button_clicked(event.pos[0], event.pos[1], 240, 140, 360, 170):
                show_menu = False  # Klik tombol "Start", jadi sembunyikan menu
                volume = 0.2  # Ini akan mengatur volume ke 50%
                bgsound.set_volume(volume)
                bgsound.play()
                fly = True
            elif is_button_clicked(event.pos[0], event.pos[1], 240, 204, 360, 234):
                print("oyeeeee")
            
    
    if fly == True:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    pygame.mixer.pause()
                    screen.blit(pause,(0,0))
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and show_menu == True:
                        if is_button_clicked(event.pos[0], event.pos[1], 240, 266, 360, 294):
                            pygame.quit()
                            quit()
                            
                        elif is_button_clicked(event.pos[0], event.pos[1], 240, 140, 360, 170):
                            show_menu = False  # Klik tombol "Start", jadi sembunyikan menu
                            volume = 0.2  # Ini akan mengatur volume ke 50%
                            # bgsound.set_volume(volume)
                            # bgsound.play()
                            fly = True
                        # elif is_button_clicked(event.pos[0], event.pos[1], 240, 204, 360, 234):
                        #     print("oyeeeee")
                            # show_menu = False  # Klik tombol "Start", jadi sembunyikan menu
        
        if keys[pygame.K_SPACE] and not paused:
            bird_y -= bird_speed

        else:
            bird_y = max(0, bird_y + bird_speed)
        
    # background
        ground_scroll -= scroll_speed
        ground_scroll_x2 -= scroll_speed

        if ground_scroll < -600:
            ground_scroll = 600
        if ground_scroll_x2 < -600:
            ground_scroll_x2 = 600

        screen.blit(bg,(0,0))
        screen.blit(ground,(ground_scroll, 50))
        screen.blit(ground,(ground_scroll_x2, 50))

        pygame.time.wait(10)

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
            
        screen.blit(PaperPlane,(bird_x,bird_y))
        screen.blit(koin,(food_x, food_y))
        screen.blit(pohon,(pipe_x, pipe_height))


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
                if bird_speed - 2 <= 3 and pipe_speed - 2 <= 3:
                    bird_speed = 3
                    pipe_speed = 3
                else:
                    bird_speed -= 2
                    pipe_speed -= 2
                lives -= 1
                if lives == 0:
                    print(f"Game Over. Skor Anda: {score}")
                    fly = False
                    show_menu = True
                resetgame()
            
    glClear(GL_COLOR_BUFFER_BIT)

    if fly == True:
        draw_text(f"Skor    : {score}", 10, 10)
        draw_text(f"Nyawa : {lives}", 10, 30)
        draw_text(f"Speed : {bird_speed}", 10, 50)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, pygame.image.tostring(pygame.display.get_surface(), 'RGBA'))
    # draw_ground()
    draw_background()

    draw_pipe()
    glDisable(GL_TEXTURE_2D)

    pygame.display.flip()