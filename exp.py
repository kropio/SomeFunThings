import pygame
import math
from random import randint, getrandbits

#Отрисовка далеких звезд, вывел сюда, чтобы глаза не мозолила
def draw_far_stars():
    for i in far_stars:
        for j in i:
            #Прикольная штука, за счет getrandbits(1) получается "мерцание" такое
            pygame.draw.circle(screen, (240, ) * 3, j, 2, getrandbits(1), getrandbits(1), getrandbits(1), getrandbits(1), getrandbits(1))
            pass

class CosmicObject(pygame.sprite.Sprite):
    def __init__(self, mass, speed, center, radius, color, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((radius * 2,) * 2, pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, ) * 2, radius)
        self.rect = pygame.Rect(center, (0, ) * 2).inflate(radius * 2, radius * 2)
        self.speed = speed
        self.coords = list(center)
        self.mass = mass
        self.tracer = [center]*LENTGH_OF_ORBIT
        self.color = color

    def on_screen(self):
        if self.rect.left >= WIDTH or self.rect.right <= 0 or self.rect.bottom <= 0 or self.rect.top >= HEIGHT:
            return False
        else: return True

    #Кривой квадратный коллижн
    """def collision(self, s):
        if self.rect.right >= s.rect.left and self.rect.left <= s.rect.right and self.rect.bottom > s.rect.top and self.rect.top < s.rect.bottom"""

    def update(self):
        #притяжение звезды
        too_far_from_star_or_planet = True
        for star in stars:
            hypo = math.sqrt(((star.rect.center[0] - self.coords[0]) ** 2) + ((star.rect.center[1] - self.coords[1]) ** 2))
            if hypo <= DOESNT_MATTER:
                too_far_from_star_or_planet = False
                accel = star.mass * self.mass / hypo / hypo
                sina, cosa = [(self.coords[1] - star.rect.center[1]) / hypo, (self.coords[0] - star.rect.center[0]) / hypo]
                if pygame.sprite.collide_circle(self, star):
                    accel = -accel
                self.speed[0] -= accel * cosa
                self.speed[1] -= accel * sina
            else:
                accel = 0

        #Отталкивание от далеких точек за экраном
        if not self.on_screen():
            accel = self.mass * 100 * (1 / ((WIDTH + FAR_FAR - self.rect.center[0]) * (WIDTH + FAR_FAR - self.rect.center[0]) + 1) - 1 / ((FAR_FAR + self.rect.center[0]) * (FAR_FAR + self.rect.center[0]) + 1))
            self.speed[0] -= accel
            accel = self.mass * 100 * (1 / ((HEIGHT + FAR_FAR - self.rect.center[1]) * (HEIGHT + FAR_FAR - self.rect.center[1]) + 1) - 1 / ((FAR_FAR + self.rect.center[1]) * (FAR_FAR + self.rect.center[1]) + 1))
            self.speed[1] -= accel
        
        #притяжение планет
        for planet in planets:
            if self != planet:
                hypo = math.sqrt(((planet.rect.center[0] - self.coords[0]) ** 2) + ((planet.rect.center[1] - self.coords[1]) ** 2))
                if hypo <= DOESNT_MATTER // 10:
                    too_far_from_star_or_planet = False
                    accel = planet.mass * self.mass / hypo / hypo / 10
                    if pygame.sprite.collide_circle(self, planet):
                        accel = -accel
                    sina, cosa = [(self.coords[1] - planet.rect.center[1]) / hypo, (self.coords[0] - planet.rect.center[0]) / hypo]
                    self.speed[0] -= accel * cosa
                    self.speed[1] -= accel * sina
                else:
                    accel = 0

        #Уменьшение скорости
        if not too_far_from_star_or_planet:
            if (self.speed[0] > 0 and self.speed[0] - 0.005 > 0.5):
                self.speed[0] -= 0.005
            if (self.speed[0] < 0 and self.speed[0] + 0.005 < -0.5):
                self.speed[0] += 0.005
            if (self.speed[1] > 0 and self.speed[1] - 0.005 > 0.5):
                self.speed[1] -= 0.005
            if (self.speed[1] < 0 and self.speed[1] + 0.005 < -0.5):
                self.speed[1] += 0.005

        #Ограчинение скорости
        if math.sqrt(self.speed[0] * self.speed[0] + self.speed[0] * self.speed[0]) > HIGH_SPEED:
            self.speed[0] /= 1.618
            self.speed[1] /= 1.618

            
        if abs(int(self.coords[0] + self.speed[0]) - int(self.coords[0])) > 0:
            self.rect.x += int(self.coords[0] + self.speed[0]) - int(self.coords[0])
        if abs(int(self.coords[1] + self.speed[1]) - int(self.coords[1])) > 0:
            self.rect.y += int(self.coords[1] + self.speed[1]) - int(self.coords[1])
        self.coords[0] += self.speed[0]
        self.coords[1] += self.speed[1]

        #закольцованный экран. нужно создавать второй объект
        """if self.rect.left >= WIDTH:
            self.rect.right = 0
        if self.rect.right <= 0:
            self.rect.left = WIDTH
        if self.rect.top >= HEIGHT:
            self.rect.bottom = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.top = HEIGHT"""

        #Резиновые рамки
        """if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speed[0] = -self.speed[0]
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]"""

        #Орбиты
        if self.on_screen():
            self.tracer = self.tracer[1:] + [self.rect.center]
        for j in range(LENTGH_OF_ORBIT):
            pygame.draw.circle(screen, self.color, self.tracer[j], 1)
        

    '''def hit(self):
        self.speed[0], self.speed[1] = self.speed[1], self.speed[0]'''
        
        

class Star(CosmicObject):
    def __init__(self, mass, color, center, radius, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((radius * 2,) * 2, pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, ) * 2, radius)
        self.rect = pygame.Rect(center, (0, 0)).inflate(radius * 2, radius * 2)
        self.speed = [0] * 2
        self.mass = mass
        #radius влияет на то, насколько близко к центру будет отталкивать звезда, то бишь когда произойдет коллизия
        self.radius = radius * 0.75

    def update(self):
        pass

class Planet(CosmicObject):
    def set_speed(self, speed):
        self.speed = speed

    

if __name__ == "__main__":
    global screen_color, planets, star, screen, WIDTH, HEIGHT, HIGH_SPEED, LENTGH_OF_ORBIT, FAR_FAR, DOESNT_MATTER
    FAR_FAR, HIGH_SPEED, LENTGH_OF_ORBIT, DOESNT_MATTER = 1000, 25, 500, 2000
    screen_color = (0, 28, 65)
    fps = 100

    
    pygame.init()
    size = WIDTH, HEIGHT = [1400, 800]

    #Огромная строчка кода, в которой заключены координаты фоновых звезд
    far_stars = [[(randint(100*(i%(WIDTH//100)), 100*(i%(WIDTH//100)+1)), randint(100*(i//(WIDTH//100)), 100*((i//(WIDTH//100))+1))) for j in range(randint(1,3))] for i in range(WIDTH * HEIGHT // 10000)]
    
    
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    
    running = True
    stars = [Star(100, (255, 255, randint(130, 200)), (WIDTH//4, HEIGHT//2), 50, screen), Star(100, (255, 255, randint(130, 200)), (WIDTH//4*3, HEIGHT//2), 50, screen), Star(100, (255, 255, randint(130, 200)), (WIDTH//2, HEIGHT//2), 50, screen)]
    all_sprites = pygame.sprite.Group([*stars])
    #all_sprites = pygame.sprite.Group()
    planet_sprites = pygame.sprite.Group()
    planets = []
    isdown = False

    #print(star.rect.center)
    #print(pygame.mouse.get_pos())

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                memory = pygame.mouse.get_pos()
                planet = Planet(randint(10, 20), [0, 0], memory, randint(10, 30), (randint(100,255), randint(100,255), randint(100,255)), screen)
                all_sprites.add(planet)
                planet_sprites.add(planet)
                planets.append(planet)
                isdown = True
                all_sprites.draw(screen)
                pygame.display.flip()
            if event.type == pygame.MOUSEBUTTONUP:
                now = pygame.mouse.get_pos()
                planet.set_speed([(now[i] - memory[i])/100 for i in range(2)])
                #print(now, memory)
                isdown = False
            if event.type == pygame.KEYDOWN and not isdown:
                if event.key == pygame.K_SPACE:
                    for planet in planets:
                        planet.speed[0] *= 4
                        planet.speed[1] *= 4
                

            
        if isdown:
            continue
        
        screen.fill(screen_color)
        draw_far_stars()
        #pygame.draw.circle(screen, (255, 255, 139), *screen.get_rect().center, 40)
        all_sprites.update()
        all_sprites.draw(screen)
        clock.tick(fps)
        pygame.display.flip()
        
    pygame.quit()
