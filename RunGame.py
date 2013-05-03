import pygame, sys, random       
import Images 
from os import sep

## Coded by Matthew Hollenbeck
## Art by Matthew Hollenbeck
## Music: Forgotten over time; original mix by Cameron Cerullo
## Sprite momement framework taken from Manning's "Hello World" Listing 18-2
## Text Display Code (including in-game, instructions, and end-game) by David Hollenbeck
## If it's not listed as someone else's, it's mine. -Matthew                                      
pygame.init()
                                                         
screen = pygame.display.set_mode([1200,800])                           
background = pygame.Surface(screen.get_size())                        
background.fill([100,100,100])                                      
clock = pygame.time.Clock()     

upPressed = False
downPressed = False 
rightPressed = False
leftPressed = False
spacePressed = False

inRedGas = False
inOrangeGas = False
inYellowGas = False
inGreenGas = False
inBlueGas = False
inPurpleGas = False

reset = False
gamemode = 0

jump = 0 ## Do not change, prevents double-jumping
jumpmax = -21 ## Subtracting from this number increases jump height, i.e. if it was -41, the player would go higher than if it was -3.
              ## -21 is the default for this number.
            
y = 0 ## Timeout for gases
hvar = 4 ## Speed for saw blades

playerRunVar = 0
playerHealth = 100

LASERPOSITIONLIST = [1, 81, 161, 241, 321, 401, 481, 561, 641, 721, 801, 881, 961, 1041, 1121]
LASER1TIME = 250 ## Time until new laser spawns
LASER2TIME = 750
LASER3TIME = 1250
LASER4TIME = 2000
LTO = 100
LSTO = 50
lasers1 = []
lasers2 = []
lasers3 = []
lasers4 = []

timescore = 0
timeScore = 0

font1 = pygame.font.Font(None, 50)
font2 = pygame.font.Font(None, 32)

class Player(pygame.sprite.Sprite):                                     
    def __init__(self, runVar, vert, image_file, speed, playerPos, playerJump, facing, direction, health, action, dead):                   
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer  
        self.speed = speed
        self.jumpmax = jumpmax
        self.health = health
        self.jump = playerJump
        self.facing = facing
        self.action = action
        self.direction = direction
        self.vert = vert  
        self.playerRunVar = 0
        self.imageString = ('%sMChar%s%s.png') %(self.vert, self.direction, self.action)
        self.image = pygame.image.load(self.imageString)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = playerPos
        self.runVar = runVar
        self.dead = dead
    def shadow(self):
        a = 100
        r = 0
        while a > 0:
            a -= 1
            r += 1
            pygame.draw.circle(screen, (150, 150, 150, a), (self.rect.left, self.rect.top), r, 0)
    def gasAct(self):
        if inRedGas and not downPressed:
            self.health -= .2
        if inGreenGas and self.health <= 100:
            self.health += .2        
    def move(self):
        ## Resetting the jump variable when the player is falling
        if self.speed[1] < -3 and not inBlueGas:
            self.jump = 0
        if self.speed[1] > 3 and inBlueGas:
            self.jump = 0
        ## Key events that will affect the player's movement
        if upPressed == True:
            if not inBlueGas and jump == 0:
                if self.speed[1] == 0:
                    self.speed[1] = jumpmax
                if self.speed[1] < -1:
                    self.speed[1] += 1
                if self.speed[1] == -1:
                    self.speed[1] += 2
                if self.speed[1] > 0:
                    self.speed[1] += 2
                self.jump += 1
            if inBlueGas and jump == 0:
                if self.speed[1] == 0:
                    self.speed[1] = -jumpmax
                if self.speed[1] > 1: 
                    self.speed[1] -= 1
                if self.speed[1] == 1:
                    self.speed[1] -= 2
                if self.speed[1] < 0:
                    self.speed[1] -= 2
                self.jump += 1
        if upPressed == False:
            self.jump = 1
            if not inBlueGas:
                self.speed[1] += 2
            if inBlueGas:
                self.speed[1] -= 2        
        if downPressed == True:
            if not inBlueGas:
                self.speed[1] += 3
            if inBlueGas:
                self.speed[1] -= 3
        if leftPressed == True:
            self.facing = 'l'
            if not inOrangeGas:
                self.speed[0] -= 1
                if self.speed[0] <= -20:
                    self.speed[0] = -20
            if inOrangeGas:
                self.speed[0] -= 2
                if self.speed[0] <= -40:
                    self.speed[0] = -40
        if rightPressed == True:
            self.facing = 'r'
            if not inOrangeGas:
                self.speed[0] += 1
                if self.speed[0] >= 20:
                    self.speed[0] = 20
            if inOrangeGas:
                self.speed[0] += 2
                if self.speed[0] >= 40:
                    self.speed[0] = 40
        if rightPressed == False and leftPressed == False:
            self.speed[0] = 0
            
        ## Reducing player speed (to make the game work better)
        self.speed[0] = self.speed[0] / 1.1
        
        ## Objects and Boundaries that will affect the player's movement
        if self.rect.left < screen.get_rect().left:
            self.rect.left = screen.get_rect().left
            self.speed[0] = 1
        if self.rect.right > screen.get_rect().right:
            self.rect.right = screen.get_rect().right
            self.speed[0] = -1
        if self.rect.bottom > screen.get_rect().bottom - 20:
            self.rect.bottom = screen.get_rect().bottom - 20
            if self.speed[1] > 0:
                self.speed[1] = 0
            if downPressed:
                self.speed[1] = 0
                self.speed[0] = 0
        if self.rect.top < 0:
            self.rect.top = 0
            if self.speed[1] < 0:
                self.speed[1] = 0
            if downPressed:
                self.speed[1] = 0
        if self.dead:
            self.speed[0] = 0
            self.facing = 'r'
        newpos = self.rect.move(self.speed)  
        self.rect = newpos
    
    ## Code to change the image based on player movement
    def dispImage(self):
        if self.facing == 'r':
            self.direction = 'Right'
        elif self.facing == 'l':
            self.direction = 'Left'
        if not inBlueGas: ## If antigravity is not on
            self.vert = 'N'
            if self.speed[1] < 0:
                self.action = 'Jump'
            if self.speed[1] > 2:
                self.action = 'Fall'
            if self.speed[1] == 0:
                if self.speed[0] == 0:
                    self.action = 'Face'
                if self.speed[0] != 0:
                    self.runVar += 1
                    if self.runVar < 5:
                        self.action = 'Run1'
                    elif self.runVar < 10:
                        self.action = 'Run2'
                    elif self.runVar > 9:
                        self.runVar = 0
                
        if inBlueGas: ## If antigravity is on
            self.vert = 'U'
            if self.speed[1] > 0:
                self.action = 'Jump'
            if self.speed[1] < -2:
                self.action = 'Fall'
            if self.speed[1] == 0:
                if self.speed[0] == 0:
                    self.action = 'Face'
                if self.speed[0] != 0:
                    if self.runVar < 5:
                        self.action = 'Run1'
                        self.runVar += 1
                    elif self.runVar < 10:
                        self.action = 'Run2'
                        self.runVar += 1
                    elif self.runVar > 9:
                        self.runVar = 0
        
        if downPressed:
            self.action = 'Crouch'
            
        if self.health <= 0:
            self.action = 'Dead'
            self.dead = True
        self.imageString = str('%sMChar%s%s.png') % (self.vert, self.direction, self.action) 
        self.image = pygame.image.load(self.imageString)
        
## The next few sections are repeats, I tried to compact them all into one class, but they were glitchy. This way 
## doesn't slow down the computer and removes the glitches.

class Laser1(pygame.sprite.Sprite):
    def __init__(self, image_file, location, mode, lasertime, lto, lsto):
        self.image = pygame.image.load('Laser.jpg')
        self.rect = self.image.get_rect('laserShoot.jpg')
        self.rect.left, self.rect.top = location
        self.mode = mode
        self.lto = lto
        self.lsto = lsto
        self.lasertime = lasertime
    
    def spawnLaser(self):
        self.lasertime += 1
        if self.lasertime >= LASER1TIME:
            if len(lasers1) < 1:
                self.lasertime = 0
                l = random.choice(LASERPOSITIONLIST)
                laser1 = Laser1(Images.laser, [l, 0], 0, 0, 100, 100)
                LASERPOSITIONLIST.remove(l)
                lasers1.append(laser1)
            else: 
                pass
    
    def collide(self, player):
        if self.mode == 2:
            if player.rect.right > self.rect.left and player.rect.right < self.rect.right:
                player.health -= 1
                print player.health
            if player.rect.left < self.rect.right and player.rect.left > self.rect.left:
                player.health -= 1
                if inYellowGas:
                    player.health -= 1
                print player.health
    
    def laserAct(self, mode):
        for laser1 in lasers1:
            if self.mode == 0:
                l = random.randint(1, 100)
                if l == 100:
                    self.mode += 1
            if self.mode == 1:
                self.lto += 1
                if self.lto == 150:
                    self.lto = 0
                    self.mode = 2
            if self.mode == 2:
                self.lsto += 1
                if self.lsto == 150:
                    self.lsto = 0
                    self.mode = 0
                      
    def dispImage(self):
        if self.mode == 0:
            self.image = pygame.image.load('Laser.jpg')
        elif self.mode == 1:
            self.image = pygame.image.load('LaserPrep.jpg')
        elif self.mode == 2:
            self.image = pygame.image.load('LaserShoot.jpg')
            
class Laser2(pygame.sprite.Sprite):
    def __init__(self, image_file, location, mode, lasertime, lto, lsto):
        self.image = pygame.image.load('Laser.jpg')
        self.rect = self.image.get_rect('laserShoot.jpg')
        self.rect.left, self.rect.top = location
        self.mode = mode
        self.lto = lto
        self.lsto = lsto
        self.lasertime = lasertime
    
    def spawnLaser(self):
        self.lasertime += 1
        if self.lasertime >= LASER2TIME:
            if len(lasers2) < 1:
                self.lasertime = 0
                l = random.choice(LASERPOSITIONLIST)
                laser2 = Laser2(Images.laser, [l, 0], 0, 0, 100, 100)
                LASERPOSITIONLIST.remove(l)                
                lasers2.append(laser2)
            else: 
                pass
                
    def collide(self, player):
        if self.mode == 2:
            if player.rect.right > self.rect.left and player.rect.right < self.rect.right:
                player.health -= 1
                print player.health
            if player.rect.left < self.rect.right and player.rect.left > self.rect.left:
                player.health -= 1
                if inYellowGas:
                    player.health -= 1
                print player.health
    
    def laserAct(self, mode):
        for laser2 in lasers2:
            if self.mode == 0:
                l = random.randint(1, 100)
                if l == 100:
                    self.mode += 1
            if self.mode == 1:
                self.lto += 1
                if self.lto == 150:
                    self.lto = 0
                    self.mode = 2
            if self.mode == 2:
                self.lsto += 1
                if self.lsto == 150:
                    self.lsto = 0
                    self.mode = 0
                      
    def dispImage(self):
        if self.mode == 0:
            self.image = pygame.image.load('Laser.jpg')
        elif self.mode == 1:
            self.image = pygame.image.load('LaserPrep.jpg')
        elif self.mode == 2:
            self.image = pygame.image.load('LaserShoot.jpg')
            
class Laser3(pygame.sprite.Sprite):
    def __init__(self, image_file, location, mode, lasertime, lto, lsto):
        self.image = pygame.image.load('Laser.jpg')
        self.rect = self.image.get_rect('laserShoot.jpg')
        self.rect.left, self.rect.top = location
        self.mode = mode
        self.lto = lto
        self.lsto = lsto
        self.lasertime = lasertime
    
    def spawnLaser(self):
        self.lasertime += 1
        if self.lasertime >= LASER3TIME:
            if len(lasers3) < 1:
                self.lasertime = 0
                l = random.choice(LASERPOSITIONLIST)
                laser3 = Laser3(Images.laser, [l, 0], 0, 0, 100, 100)
                LASERPOSITIONLIST.remove(l)
                lasers3.append(laser3)
            else: 
                pass
    
    def collide(self, player):
        if self.mode == 2:
            if player.rect.right > self.rect.left and player.rect.right < self.rect.right:
                player.health -= 1
                if inYellowGas:
                    player.health -= 1                
                print player.health
            if player.rect.left < self.rect.right and player.rect.left > self.rect.left:
                player.health -= 1
                print player.health
                
    def laserAct(self, mode):
        for laser3 in lasers3:
            if self.mode == 0:
                l = random.randint(1, 100)
                if l == 100:
                    self.mode += 1
            if self.mode == 1:
                self.lto += 1
                if self.lto == 150:
                    self.lto = 0
                    self.mode = 2
            if self.mode == 2:
                self.lsto += 1
                if self.lsto == 150:
                    self.lsto = 0
                    self.mode = 0
                      
    def dispImage(self):
        if self.mode == 0:
            self.image = pygame.image.load('Laser.jpg')
        elif self.mode == 1:
            self.image = pygame.image.load('LaserPrep.jpg')
        elif self.mode == 2:
            self.image = pygame.image.load('LaserShoot.jpg')
            
class Laser4(pygame.sprite.Sprite):
    def __init__(self, image_file, location, mode, lasertime, lto, lsto):
        self.image = pygame.image.load('Laser.jpg')
        self.rect = self.image.get_rect('laserShoot.jpg')
        self.rect.left, self.rect.top = location
        self.mode = mode
        self.lto = lto
        self.lsto = lsto
        self.lasertime = lasertime
    
    def spawnLaser(self):
        self.lasertime += 1
        if self.lasertime >= LASER4TIME:
            if len(lasers4) < 1:
                self.lasertime = 0
                l = random.choice(LASERPOSITIONLIST)
                laser4 = Laser4(Images.laser, [l, 0], 0, 0, 100, 100)
                LASERPOSITIONLIST.remove(l)
                lasers4.append(laser4)
            else: 
                pass
                
    def collide(self, player):
        if self.mode == 2:
            if player.rect.right > self.rect.left and player.rect.right < self.rect.right:
                player.health -= 1
                if inYellowGas:
                    player.health -= 1                
                print player.health
            if player.rect.left < self.rect.right and player.rect.left > self.rect.left:
                player.health -= 1
                print player.health
                
    def laserAct(self, mode):
        for laser4 in lasers4:
            if self.mode == 0:
                l = random.randint(1, 100)
                if l == 100:
                    self.mode += 1
            if self.mode == 1:
                self.lto += 1
                if self.lto == 150:
                    self.lto = 0
                    self.mode = 2
            if self.mode == 2:
                self.lsto += 1
                if self.lsto == 150:
                    self.lsto = 0
                    self.mode = 0
                      
    def dispImage(self):
        if self.mode == 0:
            self.image = pygame.image.load('Laser.jpg')
        elif self.mode == 1:
            self.image = pygame.image.load('LaserPrep.jpg')
        elif self.mode == 2:
            self.image = pygame.image.load('LaserShoot.jpg')

class Saw1(pygame.sprite.Sprite):
    def __init__(self, image_file, location, speed, hvar):
        self.image = pygame.image.load('sawBlade.png')
        self.rect = self.image.get_rect(self.image)
        self.rect.left, self.rect.top = location
        self.speed = speed
        self.y = 0
        self.hvar = hvar
    
    def move(self):
        self.y += 1
        if self.y == 200:
            self.y = 0
            self.speed = [hvar, random.randint(-1, 1)]
                
        newPos = self.rect.move(self.speed)
        self.rect = newPos
        if self.rect.right > 1300:
            self.rect.left, self.rect.top = [random.randint(-200, -100), random.randint(100, 400)]
        
    def collide(self, player):
        global playerHealth
        if player.rect.left > self.rect.left and player.rect.left < self.rect.right:
            if self.rect.top > player.rect.top and self.rect.top < player.rect.top + 176:
                player.health -= 1
        if player.rect.right > self.rect.left and player.rect.right < self.rect.right:
            if self.rect.top > player.rect.top and self.rect.top < player.rect.top + 176:
                player.health -= 1
                
class Saw2(pygame.sprite.Sprite):
    def __init__(self, image_file, location, speed, hvar):
        self.image = pygame.image.load('sawBlade.png')
        self.rect = self.image.get_rect(self.image)
        self.rect.left, self.rect.top = location
        self.speed = speed
        self.y = y
        self.hvar = hvar
        
    def move(self):
        self.y += 1
        if self.y == 200:
            self.y = 0
            self.speed = [hvar, random.randint(-1, 1)]
                
        newPos = self.rect.move(self.speed)
        self.rect = newPos
        if self.rect.right > 1300:
            self.rect.left, self.rect.top = [random.randint(-200, -100), random.randint(200, 600)]
    
    def collide(self, player):
        global playerHealth
        if player.rect.left > self.rect.left and player.rect.left < self.rect.right:
            if self.rect.top > player.rect.top and self.rect.top < player.rect.top + 176:
                player.health -= 1
        if player.rect.right > self.rect.left and player.rect.right < self.rect.right:
            if self.rect.top > player.rect.top and self.rect.top < player.rect.top + 176:
                player.health -= 1
                
class Saw3(pygame.sprite.Sprite):
    def __init__(self, image_file, location, speed, hvar):
        self.image = pygame.image.load('sawBlade.png')
        self.rect = self.image.get_rect(self.image)
        self.rect.left, self.rect.top = location
        self.speed = speed
        self.y = y
        self.hvar = hvar
        
    def move(self):
        self.y += 1
        if self.y == 200:
            self.y = 0
            self.speed = [hvar, random.randint(-1, 1)]
                
        newPos = self.rect.move(self.speed)
        self.rect = newPos
        if self.rect.right > 1300:
            self.rect.left, self.rect.top = [random.randint(-200, -100), random.randint(400, 800)]
            
    def collide(self, player):
        global playerHealth
        if player.rect.left > self.rect.left and player.rect.left < self.rect.right:
            if self.rect.top > player.rect.top and self.rect.top < player.rect.top + 176:
                player.health -= 1
        if player.rect.right > self.rect.left and player.rect.right < self.rect.right:
            if self.rect.top > player.rect.top and self.rect.top < player.rect.top + 176:
                player.health -= 1
                
class Saw4(pygame.sprite.Sprite):
    def __init__(self, image_file, location, speed, hvar):
        self.image = pygame.image.load('sawBlade.png')
        self.rect = self.image.get_rect(self.image)
        self.rect.left, self.rect.top = location
        self.speed = speed
        self.y = y
        self.hvar = hvar
        
    def move(self):
        self.y += 1
        if self.y == 200:
            self.y = 0
            self.speed = [hvar, random.randint(-1, 1)]
                
        newPos = self.rect.move(self.speed)
        self.rect = newPos
        if self.rect.right > 1300:
            self.rect.left, self.rect.top = [random.randint(-200, -100), random.randint(100, 700)]

    def collide(self, player):
        if player.rect.left > self.rect.left and player.rect.left < self.rect.right:
            if self.rect.top > player.rect.top and self.rect.top < player.rect.top + 176:
                player.health -= 1
        if player.rect.right > self.rect.left and player.rect.right < self.rect.right:
            if self.rect.top > player.rect.top and self.rect.top < player.rect.top + 176:
                player.health -= 1
        
class redJar(pygame.sprite.Sprite):
    def __init__(self, location, speed, spawn, y):
        self.image = pygame.image.load('RedJar.png')
        self.rect = self.image.get_rect(self.image)
        self.rect.left, self.rect.top = location
        self.speed = speed
        self.spawn = spawn
        self.y = y
        
    def spawnCheck(self):
        x = random.randint(1, 2000)
        if x == 1:
            self.spawn = True
        
    def move(self):
        global inRedGas
        global inOrangeGas
        global inYellowGas
        global inGreenGas
        global inBlueGas
        global inPurpleGas
        
        if self.spawn == True:
            self.speed[1] = 4
        if self.rect.top > 800:
            inRedGas = True
            inOrangeGas = False
            inYellowGas = False
            inGreenGas = False
            inBlueGas = False
            inPurpleGas = False
            
            self.spawn = False
            self.rect.top = -100
            self.speed[1] = 0
        newpos = self.rect.move(self.speed)
        self.rect = newpos
        
    def timeout(self):
        global inRedGas
        if self.y == 0 and inRedGas:
            self.y = random.randint(200, 400)
        if self.y != 0:
            self.y -= 1
        if self.y == 1:
            inRedGas = False
            self.y = 0
        
        

class orangeJar(pygame.sprite.Sprite):
    def __init__(self, location, speed, spawn, y):
        self.image = pygame.image.load('OrangeJar.png')
        self.rect = self.image.get_rect(self.image)
        self.rect.left, self.rect.top = location
        self.speed = speed
        self.spawn = spawn
        self.y = y
    def spawnCheck(self):
        x = random.randint(1, 2000)
        if x == 1:
            self.spawn = True
            
    def move(self):
        global inRedGas
        global inOrangeGas
        global inYellowGas
        global inGreenGas
        global inBlueGas
        global inPurpleGas
        
        if self.spawn == True:
            self.speed[1] = 4
        if self.rect.top > 800:
            inRedGas = False
            inOrangeGas = True
            inYellowGas = False
            inGreenGas = False
            inBlueGas = False
            inPurpleGas = False
            
            self.spawn = False
            self.rect.top = -100
            self.speed[1] = 0
        newpos = self.rect.move(self.speed)
        self.rect = newpos
    
    def timeout(self):
        global inOrangeGas
        if self.y == 0 and inOrangeGas:
            self.y = random.randint(200, 400)
        if self.y != 0:
            self.y -= 1
        if self.y == 1:
            inOrangeGas = False
            self.y = 0

## Yellow Gas increases the damage done by hazards
class yellowJar(pygame.sprite.Sprite):
    def __init__(self, location, speed, spawn, y):
        self.image = pygame.image.load('YellowJar.png')
        self.rect = self.image.get_rect(self.image)
        self.rect.left, self.rect.top = location
        self.speed = speed
        self.spawn = spawn
        self.y = y
    def spawnCheck(self):
        x = random.randint(1, 4000)
        if x == 1:
            self.spawn = True
            
    def move(self):
        global inRedGas
        global inOrangeGas
        global inYellowGas
        global inGreenGas
        global inBlueGas
        global inPurpleGas
        
        if self.spawn == True:
            self.speed[1] = 4
        if self.rect.top > 800:
            inRedGas = False
            inOrangeGas = False
            inYellowGas = True
            inGreenGas = False
            inBlueGas = False
            inPurpleGas = False
            
            self.spawn = False
            self.rect.top = -100
            self.speed[1] = 0
        newpos = self.rect.move(self.speed)
        self.rect = newpos
    
    def timeout(self):
        global inYellowGas
        if self.y == 0 and inYellowGas:
            self.y = random.randint(200, 400)
        if self.y != 0:
            self.y -= 1
        if self.y == 1:
            inYellowGas = False
            self.y = 0
            
## Green Gas restores the player's health
class greenJar(pygame.sprite.Sprite):
    def __init__(self, location, speed, spawn, y):
        self.image = pygame.image.load('GreenJar.png')
        self.rect = self.image.get_rect(self.image)
        self.rect.left, self.rect.top = location
        self.speed = speed
        self.spawn = spawn
        self.y = y
    def spawnCheck(self):
        x = random.randint(1, 4000)
        if x == 1:
            self.spawn = True
            
    def move(self):
        global inRedGas
        global inOrangeGas
        global inYellowGas
        global inGreenGas
        global inBlueGas
        global inPurpleGas
        
        if self.spawn == True:
            self.speed[1] = 4
        if self.rect.top > 800:
            inRedGas = False
            inOrangeGas = False
            inYellowGas = False
            inGreenGas = True
            inBlueGas = False
            inPurpleGas = False
            
            self.spawn = False
            self.rect.top = -100
            self.speed[1] = 0
        newpos = self.rect.move(self.speed)
        self.rect = newpos
    
    def timeout(self):
        global inGreenGas
        if self.y == 0 and inGreenGas:
            self.y = random.randint(200, 400)
        if self.y != 0:
            self.y -= 1
        if self.y == 1:
            inGreenGas = False
            self.y = 0
        
## Blue Gas reverses gravity
class blueJar(pygame.sprite.Sprite):
    def __init__(self, location, speed, spawn, y):
        self.image = pygame.image.load('BlueJar.png')
        self.rect = self.image.get_rect(self.image)
        self.rect.left, self.rect.top = location
        self.speed = speed
        self.spawn = spawn
        self.y = y
        
    def spawnCheck(self):
        x = random.randint(1, 2000)
        if x == 1:
            self.spawn = True
            
    def move(self):
        global inRedGas
        global inOrangeGas
        global inYellowGas
        global inGreenGas
        global inBlueGas
        global inPurpleGas
        
        if self.spawn == True:
            self.speed[1] = 4
        if self.rect.top > 800:
            inRedGas = False
            inOrangeGas = False
            inYellowGas = False
            inGreenGas = False
            inBlueGas = True
            inPurpleGas = False
            
            self.spawn = False
            self.rect.top = -100
            self.speed[1] = 0
        newpos = self.rect.move(self.speed)
        self.rect = newpos
        
    def timeout(self):
        global inBlueGas
        if self.y == 0 and inBlueGas:
            self.y = random.randint(200, 400)
        if self.y != 0:
            self.y -= 1
        if self.y == 1:
            inBlueGas = False
            self.y = 0
            
## Purple Gas randomizes the direction of travel
class purpleJar(pygame.sprite.Sprite):
    def __init__(self, location, speed, spawn, y):
        self.image = pygame.image.load('PurpleJar.png')
        self.rect = self.image.get_rect(self.image)
        self.rect.left, self.rect.top = location
        self.speed = speed
        self.spawn = spawn
        self.y = y
    
    def spawnCheck(self):
        x = random.randint(1, 2000) ##Lower this variable to increase the amount of jars that fall
        if x == 1:
            self.spawn = True
            
    def move(self):
        global inRedGas
        global inOrangeGas
        global inYellowGas
        global inGreenGas
        global inBlueGas
        global inPurpleGas
        
        if self.spawn == True:
            self.speed[1] = 4
        if self.rect.top > 800:
            inRedGas = False
            inOrangeGas = False
            inYellowGas = False
            inGreenGas = False
            inBlueGas = False
            inPurpleGas = True
            
            self.spawn = False
            self.rect.top = -100
            self.speed[1] = 0
        newpos = self.rect.move(self.speed)
        self.rect = newpos
       
    def timeout(self):
        global inPurpleGas
        if self.y == 0 and inPurpleGas:
            self.y = random.randint(200, 400)
        if self.y != 0:
            self.y -= 1
        if self.y == 1:
            inPurpleGas = False
            self.y = 0 
    

## Setting Attributes for Sprites
player = Player(0, 'N', Images.player, [10,0], [40, 600], 0, 'r', 'Right', playerHealth, 'Face', False)
laser1 = Laser1(Images.laser, [random.randint(1, 1160), 0], 0, 0, 100, 100)
laser2 = Laser2(Images.laser, [random.randint(1, 1160), 0], 0, 0, 100, 100)
laser3 = Laser3(Images.laser, [random.randint(1, 1160), 0], 0, 0, 100, 100)
laser4 = Laser4(Images.laser, [random.randint(1, 1160), 0], 0, 0, 100, 100)

rjar = redJar([580, -100], [0, 0], False, 0)
ojar = orangeJar([580, -100], [0, 0], False, 0)
yjar = yellowJar([580, -100], [0, 0], False, 0)
gjar = greenJar([580, -100], [0, 0], False, 0)
bjar = blueJar([580, -100], [0, 0], False, 0)
pjar = purpleJar([580, -100], [0, 0], False, 0)

sawBlade1 = Saw1('sawBlade.png', [-100, random.randint(1, 800)], [0, 0], hvar)
sawBlade2 = Saw2('sawBlade.png', [1300, random.randint(1, 800)], [0, 0], hvar)
sawBlade3 = Saw3('sawBlade.png', [1300, random.randint(1, 800)], [0, 0], hvar)
sawBlade4 = Saw4('sawBlade.png', [-100, random.randint(1, 800)], [0, 0], hvar)

text_1 = font2.render("Welcome to Gauntlet!", 1, (0, 0, 0))
text_2 = font2.render("To move, press A and D to move right and left.", 1, (0, 0, 0))
text_3 = font2.render("To jump, press W.", 1, (0, 0, 0))
text_4 = font2.render("Avoid everything. Chances are, it'll hurt you.", 1, (0, 0, 0))
text_5 = font2.render("Red causes damage. Duck to avoid it.", 1, (0, 0, 0))
text_6 = font2.render("Orange speeds you up. Use it wisely", 1, (0, 0, 0))
text_7 = font2.render("Yellow increases the damage caused by lasers.", 1, (0, 0, 0))
text_8 = font2.render("Green heals you. You're lucky if you get it.", 1, (0, 0, 0))
text_9 = font2.render("Blue reverses gravity.", 1, (0, 0, 0))
text_10 = font2.render("Purple causes you to lose control fo some time.", 1, (0, 0, 0))

text_13 = font2.render("Press any key to exit", 1, (0, 0, 0))
text_14 = font2.render("Thanks for playing!", 1, (0, 0, 0))
def deathsequence(dead):
    if dead:
        text_11 = font2.render("Congratulations! You survived for %s seconds." % timeScore, 1, (0, 0, 0))
        text_12 = font2.render("", 1, (0, 0, 0)) 
        
        x = True
        animateIntro(text_11, text_12)
        introProgress(x)
        animateIntro(text_13, text_14)
        introProgress(x)
        sys.exit()
        
def animateIntro(text1, text2):
    #by David Hollenbeck
    screen.fill([100, 100, 100])
    rect1 = text1.get_rect()
    rect1.centerx = screen.get_rect().centerx
    rect1.centery = screen.get_rect().centery
    
    rect2 = text2.get_rect()
    rect2.centerx = screen.get_rect().centerx
    rect2.centery = screen.get_rect().centery + 30
    
    screen.blit(text1, rect1)
    screen.blit(text2, rect2)
    
    pygame.display.flip()
    
def introProgress(x):
    while x == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                x = False


## Pregame Introduction Sequence
x = True
animateIntro(text_1, text_4)
introProgress(x)
animateIntro(text_2, text_3)
introProgress(x)
animateIntro(text_5, text_6)
introProgress(x)
animateIntro(text_7, text_8)
introProgress(x)
animateIntro(text_9, text_10)
introProgress(x)
        
while True:             
    for event in pygame.event.get():                                  
        if event.type == pygame.QUIT:                                 
            sys.exit()                                                
        if event.type == pygame.KEYDOWN:
            ## Movement Variables                            
            if event.key == pygame.K_w:                              
                upPressed = True  
                downPressed = False         
            if event.key == pygame.K_s:                          
                downPressed = True
                upPressed = False
            if event.key == pygame.K_a:
                leftPressed = True
                rightPressed = False
            if event.key == pygame.K_d:
                rightPressed = True
                leftPressed = False

        if event.type == pygame.KEYUP:
            ## Movement Variables
            if event.key == pygame.K_w:                              
                upPressed = False
            if event.key == pygame.K_s:                          
                downPressed = False
            if event.key == pygame.K_a:
                leftPressed = False
            if event.key == pygame.K_d:
                rightPressed = False
    
    ## Purple Gas Randomizing the direction of travel
    if inPurpleGas:
        x = random.randint(0,1)
        if x == 0:
            rightPressed = True
            leftPressed = False
        if x == 1:
            leftPressed = True
            rightPressed = False
            
    clock.tick(30)             
    if inRedGas:
        BackgroundColor = (255, 0, 0)
    elif inOrangeGas:
        BackgroundColor = (255, 127, 0)
    elif inYellowGas:
        BackgroundColor = (255, 255, 0)
    elif inGreenGas:
        BackgroundColor = (0, 255, 0)
    elif inBlueGas:
        BackgroundColor = (0, 0, 255)
    elif inPurpleGas:
        BackgroundColor = (127, 0, 127)
    else:
        BackgroundColor = (100, 100, 100)
    screen.fill(BackgroundColor)
    
    laser1.spawnLaser()
    laser1.laserAct(laser1.mode)
    laser1.dispImage()
    laser1.collide(player)
    
    laser2.spawnLaser()
    laser2.laserAct(laser2.mode)
    laser2.dispImage()
    laser2.collide(player)
    
    laser3.spawnLaser()
    laser3.laserAct(laser3.mode)
    laser3.dispImage()
    laser3.collide(player)
    
    laser4.spawnLaser()
    laser4.laserAct(laser4.mode)
    laser4.dispImage()
    laser4.collide(player)
    
    sawBlade1.move()
    sawBlade1.collide(player)
    sawBlade2.move() 
    sawBlade2.collide(player)   
    sawBlade3.move()
    sawBlade3.collide(player)
    sawBlade4.move()
    sawBlade4.collide(player)
    
    rjar.spawnCheck()
    rjar.move()
    rjar.timeout()
    ojar.spawnCheck()
    ojar.move()
    ojar.timeout()
    yjar.spawnCheck()
    yjar.move() 
    yjar.timeout()   
    gjar.spawnCheck()
    gjar.move()
    gjar.timeout()    
    bjar.spawnCheck()
    bjar.move()
    bjar.timeout()
    pjar.spawnCheck()
    pjar.move()
    pjar.timeout()
    
    player.gasAct()                                  
    player.move()
    player.shadow()
    player.dispImage()
    screen.blit(player.image, player.rect)
    
    screen.blit(sawBlade1.image, sawBlade1.rect)
    screen.blit(sawBlade2.image, sawBlade2.rect)
    screen.blit(sawBlade3.image, sawBlade3.rect)
    screen.blit(sawBlade4.image, sawBlade4.rect)
    
    screen.blit(rjar.image, rjar.rect)
    screen.blit(ojar.image, ojar.rect)
    screen.blit(yjar.image, yjar.rect)
    screen.blit(gjar.image, gjar.rect)
    screen.blit(bjar.image, bjar.rect)
    screen.blit(pjar.image, pjar.rect)
    
    for laser1 in lasers1:
        screen.blit(laser1.image, laser1.rect)
        pygame.sprite.Sprite.kill
    for laser2 in lasers2:
        screen.blit(laser2.image, laser2.rect)
        pygame.sprite.Sprite.kill
    for laser3 in lasers3:
        screen.blit(laser3.image, laser3.rect)
        pygame.sprite.Sprite.kill
    for laser4 in lasers4:
        screen.blit(laser4.image, laser4.rect)
        pygame.sprite.Sprite.kill
        
    pygame.display.flip()
    
    timescore += 1
    timeScore = timescore // 30
    deathsequence(player.dead)
    
    if timeScore < 30:
        hvar = 8
    elif timeScore < 60:
        hvar = 12
    elif timeScore < 90:
        hvar = 16
    elif timeScore < 120:
        hvar = 20
    
    life_text = font1.render("Health: " + str(player.health), 1, (0, 0, 0))
    time_text = font1.render("Time: " + str(timeScore), 1, (0, 0, 0))
    
    screen.blit(life_text, [504, 10])
    screen.blit(time_text, [1000, 10])
    pygame.display.flip()
