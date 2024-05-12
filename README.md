# ogoj-game
based off of gojo from jjk

it was just supposed to be a supid thing to test my skills, but it ended up becoming my best project

the code is really bad and probably really ineficient, don't judge me - it is my first platformer style thing

to turn hitboxes *off* change `self.showHitbox` to `False` under the `player` class
```
class player(gameSprite):
  def __init__(self,sprite,X,Y,w,h,speed,jump) :
    super().__init__(sprite,X,Y,w,h,speed)
    self.jump = jump
    self.jumping = False
    self.showHitbox = True
    self.hitboxes = []
    self.abilitiesToBlit = []
    self.rcd = 2 * 60
    self.direction = True
```
