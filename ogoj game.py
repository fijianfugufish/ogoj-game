from pygame import *
import sys
from math import sqrt, pow, dist

winx = 1200
winy = 800

padding = 5

counter = 0

scrolls = []

game = True

window = display.set_mode((winx,winy))
display.set_caption('super cool ogoj game')
window.fill((100,100,100))

font.init()

class gameSprite(sprite.Sprite):
    def __init__(self,sprite,X,Y,w,h,speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite),(w,h))
        self.w = w
        self.h = h
        self.speed = speed
        self.diagonalSpeed = ((sqrt((pow(speed,2) + pow(speed,2))) / 2) + speed / 7)
        self.rect = self.image.get_rect()
        self.rect.x = X
        self.rect.y = Y
        self.yv = 0
    def blit(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
    def checkCollision(self,obj):
        return Rect.colliderect(self.rect,obj.rect)
    def checkCollisionWOtherRect(self,obj1,obj2):
        return Rect.colliderect(obj1,obj2.rect)

class GUI(sprite.Sprite):
    def __init__(self,X,Y,w,h,col,trans):
        self.w = w
        self.h = h
        self.x = X
        self.y = Y
        self.rect = Rect(0,0,w,h)
        self.colour = col
        self.transparency = trans
        self.surface = Surface((w,h))
        self.surface.set_alpha(trans)
        self.font = font.SysFont('Arial', 25)
        self.display = ''
        global ui
        ui.append(self)
    def draw(self):
        global window
        draw.rect(self.surface,self.colour,self.rect)
        if not self.display == '':
            self.surface = self.font.render(self.display,False,(255,0,0))
        self.surface.set_alpha(self.transparency)
        window.blit(self.surface,(self.x,self.y))

class surfaceGUI(GUI):
    def __init__(self,X,Y,w,h,col,trans):
        super().__init__(X,Y,w,h,col,trans)
        global scrolls
        scrolls.append(self)
    def scroll(self,movement):
        self.x += movement

class damageSurfaceGUI(surfaceGUI):
    def __init__(self,X,Y,w,h,col,trans,damage):
        super().__init__(X,Y,w,h,col,trans)
        self.count = 0
        self.display = str(damage)
        self.x -= self.w/2
    def stepAnim(self):
        self.count += 1
        self.transparency -= 5
        self.y -= 1
        if self.transparency == 0:
            global ui
            ui.remove(self)
        
class person(gameSprite):
    def __init__(self,sprite,X,Y,w,h,speed,health):
        super().__init__(sprite,X,Y,w,h,speed)
        self.health = health
        self.spriteString = sprite
        global peopole
        people.append(self)
        global scrolls
        scrolls.append(self)
    def hit(self,dangerous):
        for i in dangerous:
            if self.checkCollision(i):
                self.health -= i.damage
                damageUI = damageSurfaceGUI(self.rect.x + self.w/2,self.rect.y,50,50,(255,0,0),255,i.damage)
        if self.health <= 0 and not self.spriteString == 'log.png':
            global peopole
            people.remove(self)
            global scrolls
            scrolls.remove(self)
    def scroll(self,movement):
        self.rect.x += movement

class effect(gameSprite):
    def __init__(self,sprite,X,Y,w,h,speed,creator):
        super().__init__(sprite,X,Y,w,h,speed)
        self.angle = 0
        self.creator = creator
        self.alpha = 255
        self.count = 0
    def rotate(self,degrees):
        self.angle += degrees
        imgCopy = transform.rotate(self.image, self.angle)
        rotatedRect = imgCopy.get_rect(center = (round(self.rect.x) + self.w/2, round(self.rect.y) + self.h/2))
        self.blitEffect(imgCopy,rotatedRect)
    def blitEffect(self,copy,effect):
        window.blit(copy, effect)
    def scale(self,size):
        self.image = transform.scale(self.image,size)
    def transparency(self,value):
        self.alpha += value
        self.image.set_alpha(self.alpha)
    def lockToPlayer(self,player):
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y

class redWow(effect):
    def __init__(self,sprite,X,Y,w,h,speed,creator):
        super().__init__(sprite,X,Y,w,h,speed,creator)
    def stepAnim(self):
        self.count += 1
        if self.count > 60:
            self.creator.abilitiesToBlit.remove(self)
        rotated = self.rotate(20)
        self.lockToPlayer(self.creator)

class redFlash(effect):
    def __init__(self,sprite,X,Y,w,h,speed,creator):
        super().__init__(sprite,X,Y,w,h,speed,creator)
    def stepAnim(self):
        self.count += 1
        if self.count > 60:
            self.image = transform.scale(image.load("red.png"),(winx,winy))
            self.transparency(-5)
            if self.alpha == 0:
                self.creator.abilitiesToBlit.remove(self)

class actuallyRed(effect):
    def __init__(self,sprite,X,Y,w,h,speed,creator):
        super().__init__(sprite,X,Y,w,h,speed,creator)
        global scrolls
        scrolls.append(self)
        global dangerous
        dangerous.append(self)
        self.damage = float('inf')
    def stepAnim(self):
        self.count += 1
        if self.count >= 60:
            if self.count == 60:
                if self.creator.direction:
                    self.speed = 30
                else:
                    self.speed = -30
            self.image = transform.scale(image.load("aka.png"),(self.w,self.h))
            self.rect.x += self.speed
            if (self.rect.x > winx + 500) or (self.rect.x < -500):
                self.creator.abilitiesToBlit.remove(self)
                global scrolls
                scrolls.remove(self)
                global dangerous
                dangerous.remove(self)
        else:
            self.lockToPlayer(self.creator)
    def scroll(self,movement):
        self.rect.x += movement

class splat(effect):
    def __init__(self,sprite,X,Y,w,h,speed,creator):
        super().__init__(sprite,X,Y,w,h,speed,creator)
        self.alpha = 250
        global scrolls
        scrolls.append(self)
    def stepAnim(self):
        self.count += 1
        if self.count == 0:
            self.lockToPlayer(self.creator)
        self.transparency(-10)
        if self.alpha == 0:
            global bullets
            bullets.remove(self.creator)
            self.creator.effects.remove(self)
    def scroll(self,movement):
        self.rect.x += movement
        
class solid(gameSprite):
    def __init__(self,sprite,X,Y,w,h,speed,group,noScroll):
        super().__init__(sprite,X,Y,w,h,speed)
        group.append(self)
        if not noScroll:
            global scrolls
            scrolls.append(self)
    def scroll(self,movement):
        self.rect.x += movement

class turret(solid):
    def __init__(self,sprite,X,Y,w,h,speed,group,firerate,shotSpeed,group2):
        super().__init__(sprite,X,Y,w,h,speed,group,False)
        self.firerate = firerate
        self.shotSpeed = shotSpeed
        self.counter = 0
        group2.append(self)
    def scroll(self,movement):
        self.rect.x += movement
    def shoot(self):
        self.counter += 1
        if counter == self.firerate:
            shot = bullet("bullet.png",(self.rect.x + self.w/2) - 15,(self.rect.y + self.h/2) - 15,30,30,self.shotSpeed,self)

class bullet(gameSprite):
    def __init__(self,sprite,X,Y,w,h,speed,parent):
        super().__init__(sprite,X,Y,w,h,speed)
        self.parent = parent
        self.origSpeed = speed
        self.effects = []
        self.gotgot = False
        global scrolls
        global dangerous
        global bullets
        scrolls.append(self)
        dangerous.append(self)
        bullets.append(self)
        self.damage = 10
    def move(self):
        self.rect.x += self.speed
        if ((self.rect.x > winx + 500) or (self.rect.x < -500)) and not self.gotgot:
            global bullets
            bullets.remove(self)
            global dangerous
            dangerous.remove(self)
    def scroll(self,movement):
        self.rect.x += movement
    def splat(self,objects):
        for i in objects:
            if self.checkCollision(i):
                global scrolls
                if self in scrolls:
                    scrolls.remove(self)
                global dangerous
                if self in dangerous:
                    dangerous.remove(self)
                squirt = splat("splat.png",(self.rect.x + self.w/2) - 50,(self.rect.y + self.h/2) - 50,100,100,0,self)
                self.effects.append(squirt)
                self.image = transform.scale(image.load("nil.png"),(0,0))
                self.gotgot = True
                break
    def effect(self):
        try:
            self.effects[0].blit()
            self.effects[0].stepAnim()
        except:
            pass

class player(gameSprite):
    def __init__(self,sprite,X,Y,w,h,speed,jump):
        super().__init__(sprite,X,Y,w,h,speed)
        self.jump = jump
        self.jumping = False
        self.showHitbox = True
        self.hitboxes = []
        self.abilitiesToBlit = []
        self.rcd = 2 * 60
        self.direction = True
    def move(self,objects):
        keysPressed = key.get_pressed()
        global scrolls
        if (keysPressed[K_a]):
            #self.rect.x -= self.speed
            self.direction = False
            for i in scrolls:
                i.scroll(self.speed)
            #bg.x += self.speed
        if (keysPressed[K_d]):
            #self.rect.x += self.speed
            self.direction = True
            for i in scrolls:
                i.scroll(-1 * self.speed)
        if (keysPressed[K_w] and self.yv == 0 and not self.jumping):
            self.jumping = True
            self.yv = self.jump
    def gravity(self,objects):
        collidedDown = False
        nextFrameRect = Rect((self.rect.x + (self.w / 8) * 3),self.rect.y + self.h - 10 - self.yv,(self.w / 4),10)
        self.hitboxes.append(nextFrameRect)
        for i in objects:
            collidedDown = collidedDown or self.checkCollisionWOtherRect(nextFrameRect,i)
        if not collidedDown:
            self.yv -= 1
            self.rect.y -= self.yv
        else:
            if not self.yv - 0.5 > 0:
                self.rect.y += self.yv - 0.5
            self.yv = 0
            self.jumping = False
        if self.showHitbox:
            self.showHitboxes(self.hitboxes,(255,0,0))
        self.hitboxes.remove(nextFrameRect)
    def restrainMovementR(self,objects):
        collidedRight = False
        nextFrameRect = Rect(self.rect.x + ((self.w / 4) * 3) - self.w/10,self.rect.y + self.h/10,self.w/10,(self.h / 10) * 8)
        self.hitboxes.append(nextFrameRect)
        for i in objects:
            collidedRight = collidedRight or self.checkCollisionWOtherRect(nextFrameRect,i)
        if collidedRight:
            #self.rect.x -= self.speed + 0.5
            global scrolls
            for i in scrolls:
                i.scroll(self.speed + 0.5)
        if self.showHitbox:
            self.showHitboxes(self.hitboxes,(255,0,0))
        self.hitboxes.remove(nextFrameRect)
    def restrainMovementL(self,objects):
        collidedLeft = False
        nextFrameRect = Rect(self.rect.x + (self.w / 4),self.rect.y + self.h/10,self.w/10,(self.h / 10) * 8)
        self.hitboxes.append(nextFrameRect)
        for i in objects:
            collidedLeft = collidedLeft or self.checkCollisionWOtherRect(nextFrameRect,i)
        if collidedLeft:
            #self.rect.x += self.speed + 0.5
            global scrolls
            for i in scrolls:
                i.scroll(-1 * (self.speed + 0.75))
        if self.showHitbox:
            self.showHitboxes(self.hitboxes,(255,0,0))
        self.hitboxes.remove(nextFrameRect)
    def restrictJump(self,objects):
        collidedUp = False
        nextFrameRect = Rect((self.rect.x + (self.w / 8) * 3),self.rect.y,(self.w / 4),self.h/10)
        self.hitboxes.append(nextFrameRect)
        for i in objects:
            collidedUp = collidedUp or self.checkCollisionWOtherRect(nextFrameRect,i)
        if collidedUp:
            if not self.yv + 0.5 < 0:
                self.rect.y += self.yv + 0.5
            self.yv *= -0.5
        if self.showHitbox:
            self.showHitboxes(self.hitboxes,(255,0,0))
        self.hitboxes.remove(nextFrameRect)
    def showHitboxes(self,hitboxes,col):
        for i in hitboxes:
            draw.rect(window,col,i,2)
    def physics(self,objects):
        self.move(objects)
        self.gravity(objects)
        self.restrictJump(objects)
        self.restrainMovementR(objects)
        self.restrainMovementL(objects)
    def cursedTechinqueReversalRed(self):
        keysPressed = key.get_pressed()
        if keysPressed[K_e] and self.rcd <= 0:
            self.abilitiesToBlit.clear()
            redGlow = redWow("redGlow.png",(self.rect.x + self.w/2) - 50,(self.rect.y + self.h/2) - 50,100,100,0,self)
            redScreen = redFlash("nil.png",0,0,winx,winy,0,self)
            aka = actuallyRed("nil.png",(self.rect.x + self.w/2) - 50,(self.rect.y + self.h/2) - 50,50,50,0,self)
            self.abilitiesToBlit.append(redGlow)
            self.abilitiesToBlit.append(redScreen)
            self.abilitiesToBlit.append(aka)
            self.rcd = 2 * 60
    def infinity(self):
        global bullets
        infiRight = Rect(self.rect.x + (self.w / 2),self.rect.y - self.h*0.25,self.w,self.h * 1.5)
        infiLeft = Rect(self.rect.x - (self.w / 2),self.rect.y - self.h*0.25,self.w,self.h * 1.5)
        self.hitboxes.append(infiRight)
        self.hitboxes.append(infiLeft)
        for i in bullets:
            distance = dist((self.rect.x + self.w/2,self.rect.y + self.h/2),(i.rect.x  + i.w/2,i.rect.y + i.w/2))
            if distance <= 500 and distance > 150:
                distance -= 200
                distance = distance/350
                if not ((i.origSpeed * distance < 0 and i.origSpeed > 0) or (i.origSpeed * distance > 0 and i.origSpeed < 0)): 
                    i.speed = i.origSpeed * distance
                else:
                    i.speed = 0
            elif distance <= 150 and distance > 100:
                i.speed = 0
            elif distance <= 100:
                distance = distance/100
                if i.origSpeed < 0:
                    if self.checkCollisionWOtherRect(infiRight,i):
                        i.speed = (distance - 1) * i.origSpeed
                    elif self.checkCollisionWOtherRect(infiLeft,i):
                        i.speed = (distance - 1) * -1 * i.origSpeed
                else:
                    if self.checkCollisionWOtherRect(infiRight,i):
                        i.speed = (distance - 1) * -1 * i.origSpeed
                    elif self.checkCollisionWOtherRect(infiLeft,i):
                        i.speed = (distance - 1) * i.origSpeed
        if self.showHitbox:
            self.showHitboxes(self.hitboxes,(0,100,200))
        self.hitboxes.remove(infiRight)
        self.hitboxes.remove(infiLeft)
    def abilityBlit(self):
        for i in self.abilitiesToBlit:
            i.blit()
            if counter:
                i.stepAnim()
    def abilities(self):
        self.cursedTechinqueReversalRed()
        self.infinity()
    def cooldowns(self):
        self.rcd -= 1

people = []
ogoj = player("ogoj.png",winx/2 - 50,0,100,150,5,20)

dummy = person("log.png",2500,475,60,125,0,100)

solids = []
brick0 = solid("black.png",-3000,600,6000,3000,0,solids,True)
brick1 = solid("black.png",900,350,100,100,0,solids,False)
brick2 = solid("black.png",750,500,100,100,0,solids,False)
brick3 = solid("black.png",1825,500,50,120,0,solids,False)

bullets = []
turrets = []
dangerous = []
gunBrick0 = turret("black.png",1300,500,0,0,10,solids,60,15,turrets)
gunBrick1 = turret("black.png",2300,500,0,0,10,solids,60,-15,turrets)

ui = []

clock = time.Clock()
FPS = 60

while game:
    counter += 1
    window.fill((100,100,100))

    ogoj.physics(solids)
    ogoj.abilities()
    ogoj.cooldowns()

    for i in people:
        i.blit()
    
    ogoj.blit()
    
    for i in bullets:
        i.move()
        i.splat(solids)
        i.effect()
        i.blit()

    for i in people:
        i.hit(dangerous)

    for i in bullets:
        i.splat(people)
    
    for i in solids:
        i.blit()
    for i in turrets:
        i.blit()
        i.shoot()

    ogoj.abilityBlit()

    for i in ui:
        i.draw()
        try:
            i.stepAnim()
        except:
            pass
    
    display.update()

    for e in event.get():
        if e.type == QUIT:
            game = False

    clock.tick(FPS)

    display.update()
    if counter > 60:
        counter = 0
    
quit()
