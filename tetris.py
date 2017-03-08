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

pointDict = {'0':0,'1':100,'2':400,'3':900,'4':1600}

DisplayHeight = blockSize * (groundPoint+1)
DisplayWidth = blockSize * (rightWallPoint+1)
gameDisplay = pg.display.set_mode((DisplayWidth,DisplayHeight))
# font setting
pg.font.init()
  
def gameFrame():
  pg.draw.rect(gameDisplay, black, [0, 0, DisplayWidth, DisplayHeight])

def returnBlock():
  pass
  
def startScreen():
  pg.display.set_caption('python TETRIS')
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
        if event.key == pg.K_q:
          pg.quit()
          quit()    
        else:
          screenLoop = False  
      if event.type == pg.QUIT:
        pg.quit()
        quit()    
  return 0

def gameoverScreen(score):
  gameDisplay.fill(white)
  fontTitle = pg.font.SysFont("Consolas",20)
  fontScore = pg.font.SysFont("Consolas",16)
  fontHowTo = pg.font.SysFont("Consolas",12)
  txtTitle = fontTitle.render('GAME OVER', False, red)
  txtScore = fontScore.render('score '+str(score), False, black)
  txtHowTo = fontHowTo.render('press any key to go start screen', False, black)
  gameDisplay.blit(txtTitle,(55,100))
  gameDisplay.blit(txtScore,(67,140))
  gameDisplay.blit(txtHowTo,(20,200))
  pg.display.update()

  screenLoop = True
  while screenLoop:
    for event in pg.event.get():
      if event.type == pg.KEYDOWN:
         if event.key == pg.K_q:
          pg.quit()
          quit()    
         else:
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
    if direction=="up":
      block[0] = block[0]
      block[1] = block[1] - 1  
  return nowBlock

def evalGround(nowBlock,blockList):
  for block in nowBlock:
    if block[1] == groundPoint:
      return True
    for eachFloorBlock in blockList: # There is a room for improvement
      if block[0] == eachFloorBlock[0] and (block[1] + 1)== eachFloorBlock[1]:
        return True
  return False

def evalAllBlock(nowBlock,blockList,direction):
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

def evalWall(nowBlock):
  for block in nowBlock:
    if block[0] == leftWallPoint or block[0] == rightWallPoint:
      return True
  return False

def slideFromRightWall(nowBlock,blockList):
  rightEnd = 0
  for block in nowBlock:
    rightEnd = block[0] if block[0] > rightEnd else rightEnd
  
  maxSlide = 0
  for block in nowBlock:
    if block[0] == rightWallPoint + 1:
      slide = (rightEnd - block[0]) + 1 
      maxSlide = slide if slide > maxSlide else maxSlide 
  return maxSlide

def slideFromLeftWall(nowBlock,blockList):
  leftEnd = rightWallPoint
  for block in nowBlock:
    leftEnd = block[0] if block[0] < leftEnd else leftEnd
  
  maxSlide = 0
  for block in nowBlock:
    if block[0] == - 1:
      slide = (block[0] - leftEnd) + 1
      maxSlide = slide if slide > maxSlide else maxSlide 
  return maxSlide

def slideFromGroundBlock(nowBlock,blockList):
  bottomEnd = -5 
  for block in nowBlock:
    bottomEnd = block[1] if block[1] > bottomEnd else bottomEnd 
  
  maxSlide = 0
  for block in nowBlock:
    if block[1] == groundPoint + 1:
      slide = (bottomEnd - block[1]) + 1
      maxSlide = slide if slide > maxSlide else maxSlide 
      for stack in blockList:
        if block[0] == stack[0] and block[1] == stack[1]:
          slide = (bottomEnd - block[1]) + 1
          maxSlide = slide if slide > maxSlide else maxSlide 
  return maxSlide

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
  variety = ['square','L','L-reverse','S','S-reverse','T','I']
  nextBlock = variety[random.randint(0, len(variety) - 1)]
  if nextBlock == 'square':
    return [[s_X, s_Y], [s_X + 1, s_Y], [s_X, s_Y - 1], [s_X + 1, s_Y - 1]]
  if nextBlock == 'L':
    return [[s_X, s_Y], [s_X + 1, s_Y], [s_X, s_Y - 1], [s_X, s_Y - 2]]
  if nextBlock == 'L-reverse':
    return [[s_X, s_Y], [s_X - 1, s_Y], [s_X, s_Y - 1], [s_X, s_Y - 2]]
  if nextBlock == 'S':
    return [[s_X, s_Y], [s_X, s_Y + 1], [s_X - 1, s_Y], [s_X - 1, s_Y - 1]]
  if nextBlock == 'S-reverse':
    return [[s_X, s_Y], [s_X, s_Y + 1], [s_X + 1, s_Y], [s_X + 1, s_Y - 1]]
  if nextBlock == 'T':
    return [[s_X, s_Y], [s_X, s_Y + 1], [s_X - 1, s_Y], [s_X + 1, s_Y]]
  if nextBlock == 'I':
    return [[s_X, s_Y], [s_X, s_Y - 1], [s_X, s_Y - 2], [s_X, s_Y - 3]]

def evalConflict(nowBlock,blockList):
  for block in nowBlock:
     for stack in blockList:
       if block[0] == stack[0] and block[1] == stack[1]:
         return True
  return False

def rotateBlock(block,direction,blockList):
  originBlock = copy.deepcopy(block)
  originX = block[0][0]
  originY = block[0][1]
  vector = [[block[0][0]-originX, block[0][1]-originY],
            [block[1][0]-originX, block[1][1]-originY],
            [block[2][0]-originX, block[2][1]-originY],
            [block[3][0]-originX, block[3][1]-originY]]

  if(direction == "right"):
    for i in range(0, len(block)):
      block[i][0] = originX + vector[i][1] 
      block[i][1] = originY - vector[i][0]

  elif(direction == "left"):
    for i in range(0, len(block)):
      block[i][0] = originX - vector[i][1] 
      block[i][1] = originY + vector[i][0]
 
  correctRight = slideFromRightWall(block,blockList)
  for i in range(0,correctRight):
    block = moveBlock(block,"left")
  correctLeft = slideFromLeftWall(block,blockList)
  for i in range(0,correctLeft):
    block = moveBlock(block,"right")
  if vector[1][1] > 0 or vector[2][1] > 0 or vector[3][1] > 0:
    correctGround = slideFromGroundBlock(block,blockList)
    for i in range(0,correctGround):
      block = moveBlock(block,"up")

  if evalConflict(block,blockList):
    return originBlock
  return block 

def eliminateLine(blockList):
  # TODO
  checkIsOver = False
  disappearLines = 0
  while not checkIsOver:
    checkIsOver = True
    for height in range(0,(groundPoint+1)):
      countBlock = 0
      disaList = []
      for stack in blockList:
        if stack[1] == height:
          disaList.append(stack)

      if len(disaList) == (rightWallPoint+1):
        disappearLines += 1
        for removeBlock in disaList:
          blockList.remove(removeBlock)
        for stack in blockList:
          if stack[1] < height:
            stack[1] = stack[1] + 1
   
        checkIsOver = False
        break

  point = pointDict[str(disappearLines)]
  result = {'blockList':blockList, 'point':point} 
  
  return result

def tetris():
  gameLoop = True
  score = 0
  fallCount = 0
  clock = pg.time.Clock()
  blockList = []
  nowBlock = initBlock()
  pg.display.set_caption("score "+str(score))

  while gameLoop:
    gameFrame()
    clock.tick(FPS)

    for event in pg.event.get():
      if event.type == pg.QUIT:
        pg.quit()
        quit()    
      if event.type == pg.KEYDOWN:
        if event.key == pg.K_q:
          pg.quit()
          quit()    
        elif event.key == pg.K_z:
          nowBlock = rotateBlock(nowBlock,"right",blockList)
        elif event.key == pg.K_x:
          nowBlock = rotateBlock(nowBlock,"left",blockList)

    pg.event.pump()
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
      if not evalAllBlock(nowBlock,blockList,"left"):
        nowBlock = moveBlock(nowBlock,"left")
    elif keys[pg.K_RIGHT]:
      if not  evalAllBlock(nowBlock,blockList,"right"):
        nowBlock = moveBlock(nowBlock,"right")
    elif keys[pg.K_UP]:
      pass
    elif keys[pg.K_DOWN]:
      if evalGround(nowBlock,blockList):
        fallCount = 30
      else:
        nowBlock = moveBlock(nowBlock,"down")
        score += 1 
          
    drawNowBlock(nowBlock)
    drawAllBlock(blockList)
    fallCount += 1
    
    if fallCount >= 30:
      if evalGround(nowBlock,blockList):
        for block in nowBlock:
          blockList.append(copy.deepcopy(block))
        result = eliminateLine(blockList)
        blockList = result['blockList']
        score = score + result['point'] 
        nowBlock = initBlock()
        fallCount = 0
      else :
        nowBlock = moveBlock(nowBlock,"down")
        fallCount = 0
 
    pg.display.set_caption("score "+str(score))
    pg.display.update()
    gameLoop = evalGameOver(blockList)

  return score

if __name__ == "__main__":
  mainLoop = True
  while mainLoop:
    startScreen()
    score = tetris()
    gameoverScreen(score)
