import pygame
import random

class Main():
    def __init__(self):
        self.Running = True
        self.ScreenWidth = 500; self.ScreenHight = 500
        self.Game_Screen = pygame.display.set_mode((self.ScreenWidth, self.ScreenHight))
        self.Clock = pygame.time.Clock()
        self.Tick = 0
        global Partical, Matter_States
        Partical = {"Empty" : 0,
                    "Stone" : 1,
                    "Sand" : 2,
                    "Water" : 3}
        Matter_States = {"Gas": [Partical["Empty"]],
                         "Liquid": [Partical["Water"]],
                         "Solid": [Partical["Stone"], Partical["Sand"]]}
        self.Game_Grid = [[0 for _ in range(100)] for _ in range(100)]
        self.Player1 = self.Player()
        self.Partical_Update = self.Element_Interaction()

    def Input(self):
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                self.Running = False
            self.Player1.Input(Event)

    def Main(self):
        while self.Running:
            self.Clock.tick(60)
            self.Input()

            self.Tick += 1
            if not self.Player1.ChangeMakeType and not self.Player1.Pause:
                self.Game_Grid = self.Player1.Update_Grid(self.Game_Grid)
                self.Game_Grid = self.Partical_Update.Update_Grid(self.Game_Grid)
                if self.Tick % 10:
                    self.Partical_Update.WaterDirect += 1
                    self.Partical_Update.WaterDirect %= 2
            elif self.Player1.ChangeMakeType:
                self.Player1.ChangeElements()
            elif self.Player1.Pause:
                self.Game_Grid = self.Player1.Update_Grid(self.Game_Grid)
            
            self.Draw()
        pygame.quit()

    def Draw(self):
        self.Game_Screen.fill((0, 0, 0))

        if not self.Player1.ChangeMakeType:
            for X in range(len(self.Game_Grid)):
                for Y in range(len(self.Game_Grid)):
                    if self.Game_Grid[X][Y] == Partical["Empty"]:
                        pygame.draw.rect(self.Game_Screen, (0, 0, 0), (X * 5, Y * 5, 5, 5))
                    elif self.Game_Grid[X][Y] == Partical["Stone"]:
                        pygame.draw.rect(self.Game_Screen, (200, 200, 200), (X * 5, Y * 5, 5, 5))
                    elif self.Game_Grid[X][Y] == Partical["Sand"]:
                        pygame.draw.rect(self.Game_Screen, (250, 250, 100), (X * 5, Y * 5, 5, 5))
                    elif self.Game_Grid[X][Y] == Partical["Water"]:
                        pygame.draw.rect(self.Game_Screen, (150, 150, 250), (X * 5, Y * 5, 5, 5))
        elif self.Player1.ChangeMakeType:
            for X in range(5):
                for Y in range(5):
                    pygame.draw.rect(self.Game_Screen, (255, 255, 255), (X*72 + X*22 + 26, Y*72 + Y*22 + 26, 72, 72))

        pygame.display.flip()

    class Player():
        def __init__(self):
            self.Pause = False
            self.Mouse_X = 0
            self.Mouse_Y = 0
            self.Mouse_Pos = [self.Mouse_X, self.Mouse_Y]
            self.MakeType = Partical["Sand"]
            self.ChangeMakeType = False
            self.Mouse_Down = False
            self.Game_Grid = []
        
        def Input(self, Event):
            if Event.type == pygame.MOUSEMOTION:
                self.MouseMove()
            if Event.type == pygame.MOUSEBUTTONDOWN:
                self.Mouse_Down = True
            if Event.type == pygame.MOUSEBUTTONUP:
                self.Mouse_Down = False
            if Event.type == pygame.KEYDOWN:
                if Event.key == pygame.K_SPACE and not self.Pause:
                    self.Pause = True
                elif Event.key == pygame.K_SPACE:
                    self.Pause = False
                if Event.key == pygame.K_TAB and not self.ChangeMakeType:
                    self.ChangeMakeType = True
                elif Event.key == pygame.K_TAB:
                    self.ChangeMakeType = False

        def Update_Grid(self, Game_Grid):
            self.Game_Grid = Game_Grid
            
            if 0 <= self.Mouse_Pos[0] < 100 and 0 <= self.Mouse_Pos[1] < 100 and self.Game_Grid[self.Mouse_Pos[0]][self.Mouse_Pos[1]] == Partical["Empty"] and self.Mouse_Down:
                self.Game_Grid[self.Mouse_Pos[0]][self.Mouse_Pos[1]] = self.MakeType
            elif 0 <= self.Mouse_Pos[0] < 100 and 0 <= self.Mouse_Pos[1] < 100 and self.MakeType == Partical["Empty"] and self.Mouse_Down:
                self.Game_Grid[self.Mouse_Pos[0]][self.Mouse_Pos[1]] = self.MakeType

            return self.Game_Grid

        def MouseMove(self):
            self.Mouse_X, self.Mouse_Y = pygame.mouse.get_pos()
            self.Mouse_Pos = [self.Mouse_X // 5, self.Mouse_Y // 5]

        def ChangeElements(self):
            if self.Mouse_Down == True:
                if 26 <= self.Mouse_X <= 98 and 26 <= self.Mouse_Y <= 98:
                    self.MakeType = Partical["Empty"]
                elif 120 <= self.Mouse_X <= 192 and 26 <= self.Mouse_Y <= 98:
                    self.MakeType = Partical["Stone"]
                elif 214 <= self.Mouse_X <= 286 and 26 <= self.Mouse_Y <= 98:
                    self.MakeType = Partical["Sand"]
                elif 308 <= self.Mouse_X <= 380 and 26 <= self.Mouse_Y <= 98:
                    self.MakeType = Partical["Water"]
    
    class Element_Interaction():
        def __init__(self):
            self.Game_Grid = []
            self.Partical = 0
            self.WaterDirect = 0
        
        def Update_Grid(self, Game_Grid):
            self.Game_Grid = Game_Grid
            for self.Y in range(len(self.Game_Grid) - 1, -1, -1):
                for self.X in range(len(self.Game_Grid)):
                    self.Stone()
                    self.Sand()
                    self.Water()

            return self.Game_Grid

        def If_Gas(self, Add_X = 0, Add_Y = 0):
            for Key, Value in Partical.items():
                if self.Game_Grid[self.X + Add_X][self.Y + Add_Y] == Value:
                    if Partical[Key] in Matter_States["Gas"]:
                        return True
                    else:
                        return False
                    
        def If_Liquid(self, Add_X = 0, Add_Y = 0):
            for Key, Value in Partical.items():
                if self.Game_Grid[self.X + Add_X][self.Y + Add_Y] == Value:
                    if Partical[Key] in Matter_States["Liquid"]:
                        return True
                    else:
                        return False

        def Sand(self):
            if self.Y + 1 < len(self.Game_Grid):
                if self.Game_Grid[self.X][self.Y] == Partical["Sand"] and (self.If_Gas(0, 1) or self.If_Liquid(0, 1)):
                    self.Partical = self.Game_Grid[self.X][self.Y + 1]
                    self.Game_Grid[self.X][self.Y] = self.Partical
                    self.Game_Grid[self.X][self.Y + 1] = Partical["Sand"]
                elif self.X-1 >= 0 and self.Game_Grid[self.X][self.Y] == Partical["Sand"] and (self.If_Gas(-1, 1) or self.If_Liquid(-1, 1)):
                    self.Partical = self.Game_Grid[self.X - 1][self.Y + 1]
                    self.Game_Grid[self.X][self.Y] = self.Partical
                    self.Game_Grid[self.X - 1][self.Y + 1] = Partical["Sand"]
                elif self.X + 1 < 100 and self.Game_Grid[self.X][self.Y] == Partical["Sand"] and (self.If_Gas(1, 1) or self.If_Liquid(1, 1)):
                    self.Partical = self.Game_Grid[self.X + 1][self.Y + 1]
                    self.Game_Grid[self.X][self.Y] = self.Partical
                    self.Game_Grid[self.X + 1][self.Y + 1] = Partical["Sand"]

        def Stone(self):
            if self.Y + 1 < len(self.Game_Grid):
                if self.Game_Grid[self.X][self.Y] == Partical["Stone"] and (self.If_Gas(0, 1) or self.If_Liquid(0, 1)):
                    self.Partical = self.Game_Grid[self.X][self.Y + 1]
                    self.Game_Grid[self.X][self.Y] = self.Partical
                    self.Game_Grid[self.X][self.Y + 1] = Partical["Stone"]
        
        def Water(self):
            if self.Y + 1 < len(self.Game_Grid):
                if self.Game_Grid[self.X][self.Y] == Partical["Water"] and self.If_Gas(0, 1):
                    self.Partical = self.Game_Grid[self.X][self.Y + 1]
                    self.Game_Grid[self.X][self.Y] = self.Partical
                    self.Game_Grid[self.X][self.Y + 1] = Partical["Water"]
                elif self.X - 1 >= 0 and self.Game_Grid[self.X][self.Y] == Partical["Water"] and self.If_Gas(-1, 1):
                    self.Partical = self.Game_Grid[self.X - 1][self.Y + 1]
                    self.Game_Grid[self.X][self.Y] = self.Partical
                    self.Game_Grid[self.X - 1][self.Y + 1] = Partical["Water"]
                elif self.X + 1 < len(self.Game_Grid) and self.Game_Grid[self.X][self.Y] == Partical["Water"] and self.If_Gas(1, 1):
                    self.Partical = self.Game_Grid[self.X + 1][self.Y + 1]
                    self.Game_Grid[self.X][self.Y] = self.Partical
                    self.Game_Grid[self.X + 1][self.Y + 1] = Partical["Water"]
            if self.X - 1 >= 0 and self.WaterDirect == 1:
                if self.Game_Grid[self.X][self.Y] == Partical["Water"] and self.If_Gas(-1, 0):
                    self.Partical = self.Game_Grid[self.X - 1][self.Y]
                    self.Game_Grid[self.X][self.Y] = self.Partical
                    self.Game_Grid[self.X - 1][self.Y] = Partical["Water"]
            elif self.X + 1 < len(self.Game_Grid) and self.WaterDirect == 0:
                if self.Game_Grid[self.X][self.Y] == Partical["Water"] and self.If_Gas(1, 0):
                    self.Partical = self.Game_Grid[self.X + 1][self.Y]
                    self.Game_Grid[self.X][self.Y] = self.Partical
                    self.Game_Grid[self.X + 1][self.Y] = Partical["Water"]



Game = Main()
Game.Main()
