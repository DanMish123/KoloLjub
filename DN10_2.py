import random
import time
from pygame import mixer
import pygame

class Kolesar:
    def __init__(self, screen):
        self.body = pygame.image.load("kolesar.png")
        self.x = screen.get_width() // 2 - self.body.get_width() // 2
        self.y = screen.get_height() - self.body.get_height()
        self.rectangle = self.body.get_rect(topleft=(self.x, self.y))
        self.rectangle.x = self.x
        self.rectangle.y = self.y
        self.lives = 3
        self.points = 0
        self.level = 1

    def left(self):
        self.x -= 300 * dt
    def right(self):
        self.x += 300 * dt
    def up(self):
        self.y -= 300 * dt
    def down(self):
        self.y += 300 * dt
    def update_rectangle(self):
        self.rectangle.y = self.y
        self.rectangle.x = self.x


class Ovira:
    def __init__(self, ovire):
        self.picname = random.choice(ovire)
        self.body = pygame.image.load(self.picname)
        self.x = random.randint(0, 800)
        self.y = -self.body.get_height()
        self.rectangle = self.body.get_rect(topleft=(self.x, self.y))
        self.rectangle.x = self.x
        self.rectangle.y = self.y
        self.collided = False
    def move_down(self):
        self.y += 1
        self.rectangle.y = self.y


pygame.init()
mixer.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
sound = mixer.Sound("arcade.mp3")
collisionSound = mixer.Sound("explosion.mp3")
pointsSound = mixer.Sound("jump.mp3")
mixer.set_num_channels(3)
ovire = ["flowers.png", "grass.png", "scooter.png", "stones.png", "walker.png", "mol.png"]
gameOver = False

ovire_moving = []
interval_ovire = random.randint(30, 150)
i = 0
dt = 0
points5 = []

font = pygame.font.SysFont("monospace", 15)

kolesar = Kolesar(screen)
ovira = Ovira(ovire)
mixer.Channel(0).play(sound, loops=-1)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")
    text = font.render("Lives: " + str(kolesar.lives), True, (245, 230, 83))
    screen.blit(text, (650, 50))

    text = font.render("Lvl: " + str(kolesar.level), True, (245, 230, 83))
    screen.blit(text, (360, 50))

    text = font.render("Pts: " + str(kolesar.points), True, (245, 230, 83))
    screen.blit(text, (50, 50))

    screen.blit(kolesar.body, kolesar.rectangle)

    if i >= interval_ovire:
        if kolesar.level > 1:
            interval_ovire = random.randint(30, 160 - 10 * kolesar.level)
        elif kolesar.level >= 13:
            interval_ovire = 30
        else: interval_ovire = random.randint(30, 150)
        ovire_moving.append(Ovira(ovire))
        i = 0

    for ov in ovire_moving:
        screen.blit(ov.body, ov.rectangle)
        ov.move_down()
        if not ov.collided and kolesar.rectangle.colliderect(ov.rectangle):
            if ov.picname != "mol.png":
                kolesar.lives -= 1
                ov.collided = True
                mixer.Channel(1).play(collisionSound)
                ovire_moving.remove(ov)
                if kolesar.lives <= 0:
                    gameOver = True
            else:
                kolesar.points += 1
                mixer.Channel(2).play(pointsSound)
                ov.collided = True
                ovire_moving.remove(ov)
                points5.append(1)
                if len(points5) == 5:
                    kolesar.level += 1
                    points5.clear()
                    interval_ovire = random.randint(30, 160 - 10 * kolesar.level)
                    if kolesar.level >= 13:
                        interval_ovire = 30
        if ov.y > screen.get_height():
            ovire_moving.remove(ov)

    if gameOver:
        font = pygame.font.SysFont("monospace", 50)
        text = font.render("Game over.", True, (245, 230, 83))
        screen.blit(text, (screen.get_width() // 2 - 150, screen.get_height() // 2))
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        kolesar.up()
        kolesar.update_rectangle()
    if keys[pygame.K_s]:
        kolesar.down()
        kolesar.update_rectangle()
    if keys[pygame.K_a]:
        kolesar.left()
        kolesar.update_rectangle()
    if keys[pygame.K_d]:
        kolesar.right()
        kolesar.update_rectangle()

    pygame.display.flip()
    dt = clock.tick(480) / 1000
    i += 1

pygame.quit()