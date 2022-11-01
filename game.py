import copy
import pygame as pg

class Statements:
    def __init__(self):
        self.memory = []
        self.index = 0

    def AddStatement(self, statement):
        self.index += 1
        self.memory.append(copy.deepcopy(statement))

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            print ("Oops, you've reached the end of time")
            return
        self.index -= 1
        return self.memory[self.index]

    def Pop(self):
        if self.index == 1:
            print ("Oops, you've reached the end of time")
            return
        self.index -= 1
        return self.memory.pop()

class Character:
    def __init__(self, start, size, color):
        self.coords = start
        self.size = size
        self.accel = 0
        self.jump = 0
        self.deformation = 0
        self.color = color
        
    def GetCoords(self):
        return [int(i) for i in self.coords] + [self.size]*2

    def Jump(self):
        self.jump = 900
        #pg.draw.rect(screen, player.color, pg.Rect([0,0,100,100]))
        return

    def UpdateAccel(self, accel):
        self.accel += accel
        return

    def Set_All(self, dictAll):
        self.__dict__ = dictAll
        return

    def Draw(self):
        pg.draw.rect(screen, player.color, pg.Rect(self.GetCoords()))

class Shadow():
    def __init__(self, obj, length):
        self.obj = obj
        self.length = length
        self.color = obj.color
        self.size = obj.size
        self.shadows = [[-50, -50] for i in range(self.length)]
        pass

    def AddShadow(self):
        self.shadows = self.shadows[1:] + [copy.deepcopy(self.obj.coords)]
        pass

    def DrawForward(self):
        for i in range(self.length):
            tmp = [i + 25 for i in self.shadows[self.length - 1 - i]]
            tmp1 = 55 + i * 4
            pg.draw.circle(screen, (255, tmp1, tmp1), tmp, self.size//2)
        pass

    def DrawBack(self):
        for i in range(self.length):
            tmp = [i + 25 for i in self.shadows[self.length - 1 - i]]
            tmp1 = 55 + i * 4
            pg.draw.circle(screen, (tmp1, 255, 255), tmp, self.size//2)
        pass

if __name__ == "__main__":

    LENGHT_OF_SHADOW = 50
    global screen
    stop_time = 50
    back_time = False
    statements = Statements()
    sizeOfWindow = width, height = [1000, 600]
    screen = pg.display.set_mode(sizeOfWindow)
    clock = pg.time.Clock()
    pg.time.set_timer(pg.USEREVENT, 5)
    player = Character([500, height - 50], 50, pg.Color("Red"))
    shadow = Shadow(player, LENGHT_OF_SHADOW)
    #rectCoords = [500, height - 50, 50, 50]
    #rectAccel = 0
    #rectJump = 0
    #deformation = 0
    running = True

    while running:
        screen.fill((255,255,255,255))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            '''if event.type == pg.MOUSEMOTION and rectCoords[1] == height - 50:
                if event.pos[0] < rectCoords[0]:
                    rectAccel = 600
                else:
                    rectAccel = -600
                rectJump = 600'''
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_z:
                    back_time = True
                if event.key == pg.K_UP and not(back_time):
                    player.Jump()
                    player.deformation = -5
            if event.type == pg.KEYUP:
                if event.key == pg.K_z:
                    stop_time = 50
                    back_time = False
            if event.type == pg.USEREVENT:
                shadow.AddShadow()
        if not(back_time):
            if pg.key.get_pressed()[pg.K_RIGHT] and player.accel != -600:
                player.UpdateAccel(-10)
            if pg.key.get_pressed()[pg.K_LEFT] and player.accel != +600:
                player.UpdateAccel(+10)
            if player.accel > 0: player.accel -= 5
            if player.accel < 0: player.accel += 5
            if player.coords[0] < 0 or player.coords[0] > 950:
                player.accel = -player.accel
            player.coords[1] = int(player.coords[1] - (player.jump/200))
            if player.coords[1] < height - 50:
                player.jump -= 10
            else:
                player.jump = 0
            player.coords[0] -= (player.accel/200)

            if player.jump != 0 or player.accel != 0:
                statements.AddStatement(player.__dict__)
            shadow.DrawForward()
        else:
            pg.time.delay(stop_time)
            if stop_time:
                stop_time-=1
            tmp = statements.Pop()
            if tmp != None:
                player.Set_All(tmp)
            player.Draw()
            shadow.DrawBack()
            #pg.draw.rect(screen, player.color, pg.Rect(player.GetCoords()))

        player.Draw()
        #pg.draw.rect(screen, player.color, pg.Rect(player.GetCoords()))
        
        clock.tick_busy_loop(300)
        pg.display.flip()
        
        #print(statements.Pop())

    

    pg.quit()
