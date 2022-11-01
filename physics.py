import pygame
import math
from random import randint
import copy

def draw(balls, tracer, numOfBalls):
    screen.fill((255, 255, 255))
    color = pygame.Color("Red")
    for i in range(numOfBalls):
        pygame.draw.circle(screen, color, (balls[i][0], balls[i][1]), 30)
    '''tracer.append([x,y])
    for i in tracer:
        pygame.draw.circle(screen, "Black", (i[0], i[1]), 1)'''

if __name__ == "__main__":
    
    pygame.init()
    numOfBalls = 20
    size = width, height = [1000, 600]
    screen = pygame.display.set_mode(size)
    fps = 100
    clock = pygame.time.Clock()
    running = True
    balls = [[randint(0, 1000), randint(0,600)] for i in range(numOfBalls)]
    accel = 0.5
    speed = [[0, 0] for i in range(numOfBalls)]
    tracer = []
    tracerTimer = 10
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                xdelta, ydelta = event.pos
                delta = [[xdelta - balls[i][0], ydelta - balls[i][1]] for i in range(numOfBalls)]
                start = copy.deepcopy(balls)
                hypo = [math.sqrt((delta[i][0] * delta[i][0]) + (delta[i][1] * delta[i][1])) for i in range(numOfBalls)]
                trig = [[delta[i][0] / hypo[i], delta[i][1] / hypo[i]]for i in range(numOfBalls)]
                #cosa = xdelta / hypo
                #sina = ydelta / hypo
                tmp = 15
                speed = [[tmp * trig[i][0], tmp * trig[i][1]] for i in range(numOfBalls)]
                #print(speed)
                #print(int(tmp * sina * 2 / (0.5)))
                timey = [abs(int(speed[i][1] * 20.9 / (accel))) for i in range(numOfBalls)]
                timex = [abs(int(speed[i][0] * 20.9 / (accel))) for i in range(numOfBalls)]
                for i in range(numOfBalls):
                    pygame.time.set_timer(pygame.USEREVENT + i, max(timey[i], timex[i]), 1)
                #pygame.time.set_timer(pygame.USEREVENT + 1, tracerTimer)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    start = [[balls[i][0],balls[i][1]] for i in range(numOfBalls)]
                    speed = [[0,0] for i in range(numOfBalls)]
            for i in range(numOfBalls):
                if event.type == pygame.USEREVENT + i:
                    '''if (speed[0] > 0):
                        x += 3
                    else:
                        x -= 3
                    y = start[1]'''
                    speed[i] = [0,0]
                '''if event.type == pygame.USEREVENT + 1:
                    if (len(tracer)!=0):
                        tracer = tracer[1:]'''
        for i in range(numOfBalls):
            balls[i][0] += speed[i][0]
            balls[i][1] += speed[i][1]
        #x += speed[0]
        #y += speed[1]
            if speed[i][1] > 0:
                if balls[i][1] > start[i][1]:
                    speed[i][1] -= accel
                else:
                    speed[i][1] += accel
            if speed[i][1] < 0:
                if balls[i][1] < start[i][1]:
                    speed[i][1] += accel
                else:
                    speed[i][1] -= accel
            if speed[i][0] > 0:
                if balls[i][0] > start[i][0]:
                    speed[i][0] -= accel
                else:
                    speed[i][0] += accel
            if speed[i][0] < 0:
                if balls[i][0] < start[i][0]:
                    speed[i][0] += accel
                else:
                    speed[i][0] -= accel
        draw(balls, tracer, numOfBalls)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
        
