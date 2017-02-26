import pygame as pg
import time, random
import copy

pg.init()
FPS = 30

white = (255,255,255)
black = (0,0,0)
blue = (0,100,255)
red = (255,0,0)

blockSize =  20
s_X = 5
s_Y = 0
groundPoint = 19
rightWallPoint = 9
leftWallPoint = 0

DisplayHeight = blockSize * (groundPoint+1)
DisplayWidth = blockSize * (rightWallPoint+1)
gameDisplay = pg.display.set_mode((DisplayWidth,DisplayHeight))
pg.display.set_caption('python TETRIS')
# font setting
pg.font.init()
  
def gameFrame():
  pg.draw.rect(gameDisplay, black, [0, 0, DisplayWidth, DisplayHeight])

def returnBlock():
  pass
  
def startScreen():
  gameDisplay.fill(white)
  fontTitle = pg.font.SysFont("Consolas",20)
  fontHowTo = pg.font.SysFont("Consolas",12)
  txtTitle = fontTitle.render('Py Tetris', False, black)
  txtHowTo = fontHowTo.render('press any key to start', False, black)
  gameDisplay.blit(txtTitle,(55,100))
  gameDisplay.blit(txtHowTo,(25,200))
  pg.display.update()

  screenLoop = True
  while screenLoop:
    for event in pg.event.get():
      if event.type == pg.KEYDOWN:
        screenLoop = False  
      if event.type == pg.QUIT:
        pg.quit()
        quit()    
  return 0

def gameoverScreen():
  gameDisplay.fill(white)
  fontTitle = pg.font.SysFont("Consolas",20)
  fontHowTo = pg.font.SysFont("Consolas",12)
  txtTitle = fontTitle.render('GAME OVER', False, red)
  txtHowTo = fontHowTo.render('press any key to go start screen', False, black)
  gameDisplay.blit(txtTitle,(55,100))
  gameDisplay.blit(txtHowTo,(25,200))
  pg.display.update()

  screenLoop = True
  while screenLoop:
    for event in pg.event.get():
      if event.type == pg.KEYDOWN:
        screenLoop = False  
      if event.type == pg.QUIT:
        pg.quit()
        quit()    
  return 0
 
def moveBlock(nowBlock,direction):
  for block in nowBlock:
    if direction=="right":
      block[0] = block[0] + 1
      block[1] = block[1]
    if direction=="down":
      block[0] = block[0]
      block[1] = block[1] + 1
    if direction=="left":
      block[0] = block[0] - 1
      block[1] = block[1]
  return nowBlock

def evalGround(nowBlock,blockList):
  for block in nowBlock:
    if block[1] == groundPoint:
      return True
    for eachFloorBlock in blockList: # There is a room for improvement
      if block[0] == eachFloorBlock[0] and (block[1] + 1)== eachFloorBlock[1]:
        return True
  return False

def evalWall(nowBlock,blockList,direction):
  if direction == "right":
    for block in nowBlock:
      if block[0] == rightWallPoint:
        return True
      for eachWallBlock in blockList:
        if (block[0] + 1) == eachWallBlock[0] and block[1] == eachWallBlock[1]:
          return True
          
  if direction == "left": 
    for block in nowBlock:
      if block[0] == leftWallPoint:
        return True
      for eachWallBlock in blockList:
        if (block[0] - 1) == eachWallBlock[0] and block[1] == eachWallBlock[1]:
          return True
        
  return False

def evalGameOver(blockList):
  for block in blockList:
    if block[0] == s_X and block[1] == s_Y:
      return False
  return True

def drawNowBlock(nowBlock):
  bs = blockSize
  for block in nowBlock:
    pg.draw.rect(gameDisplay,blue,[bs * block[0], bs * block[1], bs, bs])

def drawAllBlock(blockList):
  bs = blockSize
  for block in blockList:
    pg.draw.rect(gameDisplay,blue,[bs * block[0], bs * block[1], bs, bs])

def initBlock():
  variety = ['square']
  nextBlock = variety[0]
  if nextBlock == 'square':
    return [[s_X, s_Y], [s_X + 1, s_Y], [s_X, s_Y - 1], [s_X + 1,s_Y - 1]]

def tetris():
  gameLoop = True
  score = 0
  fallCount = 0
  clock = pg.time.Clock()
  blockList = []
  nowBlock = initBlock()

  while gameLoop:
    pg.display.set_caption("Simple TETRIS : score "+str(score))
    gameFrame()
    clock.tick(FPS)

    for event in pg.event.get():
      if event.type == pg.QUIT or event.key == pg.K_q:
        pg.quit()
        quit()    

    pg.event.pump()
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
      if not evalWall(nowBlock,blockList,"left"):
        nowBlock = moveBlock(nowBlock,"left")
    elif keys[pg.K_RIGHT]:
      if not  evalWall(nowBlock,blockList,"right"):
        nowBlock = moveBlock(nowBlock,"right")
    elif keys[pg.K_UP]:
      pass
    elif keys[pg.K_DOWN]:
      if evalGround(nowBlock,blockList):
        fallCount = 30
      else:
        nowBlock = moveBlock(nowBlock,"down")
          
    drawNowBlock(nowBlock)
    drawAllBlock(blockList)
    fallCount+=1
    
    if fallCount >= 30:
      if evalGround(nowBlock,blockList):
        for block in nowBlock:
          blockList.append(copy.deepcopy(block))
        nowBlock = initBlock()
        fallCount = 0
      else :
        nowBlock = moveBlock(nowBlock,"down")
        fallCount = 0

    pg.display.update()
    gameLoop = evalGameOver(blockList)

if __name__ == "__main__":
  mainLoop = True
  while mainLoop:
    startScreen()
    tetris()
    gameoverScreen()
