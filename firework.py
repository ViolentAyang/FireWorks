import pygame
import random
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("ViolentAyang - FireWorks")

class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = HEIGHT
        self.target_y = y
        self.speed = 5  # 降低上升速度（原来是8）
        self.exploded = False
        self.particles = []
        self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
    def update(self):
        if not self.exploded:
            # 上升阶段
            self.y -= self.speed
            if self.y <= self.target_y:
                self.explode()
        else:
            # 爆炸后更新所有粒子
            for particle in self.particles[:]:
                particle.move()
                if particle.lifetime <= 0:
                    self.particles.remove(particle)
    def explode(self):
        self.exploded = True
        # 创建爆炸粒子
        for _ in range(100):
            self.particles.append(Particle(self.x, self.y, self.color))
    
    def draw(self, screen):
        if not self.exploded:
            # 绘制上升阶段的火箭
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 2)
            # 绘制火箭尾迹
            pygame.draw.circle(screen, (255, 200, 100), (int(self.x), int(self.y + 5)), 1)
        else:
            # 绘制爆炸后的粒子
            for particle in self.particles:
                particle.draw(screen)

# 定义烟花粒子类
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.speed = random.uniform(2, 6)
        self.angle = random.uniform(0, 2 * math.pi)
        self.lifetime = 100
        # 为每个粒子随机生成一个颜色，而不是使用烟花的颜色
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        
    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed - 0.1
        self.lifetime -= 1
        
    def draw(self, screen):
        if self.lifetime > 0:
            alpha = int((self.lifetime / 100) * 255)
            color = (*self.color, alpha)
            # 增加粒子大小，从3x3改为5x5
            surf = pygame.Surface((5, 5), pygame.SRCALPHA)
            # 增加粒子半径，从1改为2
            pygame.draw.circle(surf, color, (2, 2), 2)
            screen.blit(surf, (int(self.x), int(self.y)))

# 主游戏循环
fireworks = []
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 点击鼠标创建多个烟花
            x, y = pygame.mouse.get_pos()
            # 在点击位置周围随机生成3个烟花
            for _ in range(3):
                offset_x = x + random.randint(-50, 50)
                offset_y = y + random.randint(-30, 30)
                fireworks.append(Firework(offset_x, offset_y))
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.size
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    
    screen.fill((0, 0, 0))
    
    # 更新和绘制所有烟花
    for firework in fireworks[:]:
        firework.update()
        firework.draw(screen)
        if firework.exploded and len(firework.particles) == 0:
            fireworks.remove(firework)
    
    # 随机生成多个烟花
    if random.random() < 0.02:  # 2%的概率生成新烟花
        # 一次生成2-4个烟花
        for _ in range(random.randint(2, 4)):
            x = random.randint(0, WIDTH)
            y = random.randint(HEIGHT//4, HEIGHT//2)
            fireworks.append(Firework(x, y))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
