import pygame

class RecursiveObj():
    def __init__(self, start, size):
        self.coords = start
        self.size = size
        if self.size*2/3 > 0.6:
            self.inside = RecursiveObj([i+self.size/6 for i in self.coords], self.size*2/3)
        else:
            self.inside = None
        pygame.draw.rect(screen, pygame.Color("Red"), pygame.Rect(self.GetCoords()), 2)

    def GetCoords(self):
        return [int(i) for i in self.coords] + [self.size]*2

    def Update(self):
        pygame.draw.rect(screen, pygame.Color("Red"), pygame.Rect(self.GetCoords()), 2)
        if self.inside == None:
            return
        self.inside.Update()
        return

    def MoveVert(self, y):
        self.coords[1] -= y
        if self.inside == None:
            return
        self.inside.MoveVert(y)

    def MoveHor(self, x):
        self.coords[0] += x
        if self.inside == None:
            return
        self.inside.MoveHor(x)


if __name__ == "__main__":

    global screen

    pygame.init()
    size = WIDTH, HEIGHT = [1400, 800]

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    recursiveObj = None

    running = True

    while running:
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                tmp = list(pygame.mouse.get_pos())
                recursiveObj = RecursiveObj(tmp, 300)
            
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            recursiveObj.MoveHor(-10)
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            recursiveObj.MoveHor(10)
        if pygame.key.get_pressed()[pygame.K_UP]:
            recursiveObj.MoveVert(10)
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            recursiveObj.MoveVert(-10)
        if recursiveObj:
            recursiveObj.Update()
        
        
        clock.tick_busy_loop(300)
        pygame.display.flip()


    pygame.quit()
