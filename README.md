# ogoj-game
based off of gojo from jjk
_______________________________________________________________________________________________________________________________________

It was just supposed to be a supid thing to test my skills, but it ended up becoming my best project.

The code is really bad, messy and probably really ineficient. Don't judge me - it is my first platformer style thing.

## controls
- WASD to move
- E to use 'red'
- 'infinity' is passive

### download
[ogoj-game.zip](https://github.com/fijianfugufish/ogoj-game/files/15286959/ogoj-game.zip)

### other stuff
To turn hitboxes *off* change ```self.showHitbox``` to ```False``` under the ```player``` class.
```python
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
```

This game is mainly just a test, not some super cool game you were hoping for.
