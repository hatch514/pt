import pygame
import time, random
import copy

pygame.init()
FPS=30

display_height = 400
display_width = 200

white = (255,255,255)
black = (0,0,0)
blue = (0,100,255)
red = (255,0,0)

block_size= 20
startpoint_X=20*5
startpoint_Y=0
groundPoint=block_size*19
rightwallPoint=block_size*9
leftwallPoint=0

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Simple TETRIS')
# font setting
pygame.font.init()
  
def frame():
  pygame.draw.rect(gameDisplay, 
          black, 
          [display_width/2-(block_size*5),display_height/2-(block_size*10),block_size*10,block_size*20])

def returnBlock():
  pass
  
def startScreen():
  gameDisplay.fill(white)
  fontTitle = pygame.font.SysFont("Consolas",20)
  fontHowTo = pygame.font.SysFont("Consolas",12)
  txtTitle = fontTitle.render('Py Tetris', False, black)
  txtHowTo = fontHowTo.render('press any key to start', False, black)
  gameDisplay.blit(txtTitle,(55,100))
  gameDisplay.blit(txtHowTo,(25,200))
  pygame.display.update()

  screenLoop = True
  while screenLoop:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN: 
        screenLoop = False  
  return 0

def gameoverScreen():
  gameDisplay.fill(white)
  fontTitle = pygame.font.SysFont("Consolas",20)
  fontHowTo = pygame.font.SysFont("Consolas",12)
  txtTitle = fontTitle.render('GAME OVER', False, red)
  txtHowTo = fontHowTo.render('press any key to go start screen', False, black)
  gameDisplay.blit(txtTitle,(55,100))
  gameDisplay.blit(txtHowTo,(25,200))
  pygame.display.update()

  screenLoop = True
  while screenLoop:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN: 
        screenLoop = False  
  return 0
 
def moveBlock(nowBlock,direction):
  for eachBlock_XnY in nowBlock: 
    if direction=="right":
      eachBlock_XnY[0] = eachBlock_XnY[0]+block_size
      eachBlock_XnY[1] = eachBlock_XnY[1]
    if direction=="down":
      eachBlock_XnY[0] = eachBlock_XnY[0]
      eachBlock_XnY[1] = eachBlock_XnY[1]+block_size
    if direction=="left":
      eachBlock_XnY[0] = eachBlock_XnY[0]-block_size
      eachBlock_XnY[1] = eachBlock_XnY[1]
  return nowBlock

def eval_ground(nowBlock,blockList):
  for eachBlock_XnY in nowBlock:
    if eachBlock_XnY[1] == groundPoint:
      return True
    for eachFloorBlock in blockList: # There is a room for improvement
      if eachBlock_XnY[0] == eachFloorBlock[0] and (eachBlock_XnY[1] + block_size)== eachFloorBlock[1] :
        return True
  return False

def eval_wall(nowBlock,blockList,direction):
  if direction == "right":
    for eachBlock_XnY in nowBlock:
      if eachBlock_XnY[0] == rightwallPoint:
        return True
      for eachWallBlock in blockList:
        if eachBlock_XnY[0] + block_size == eachWallBlock[0] and eachBlock_XnY[1] == eachWallBlock[1]:
          return True
          
  if direction == "left": 
    for eachBlock_XnY in nowBlock:
      if eachBlock_XnY[0] == leftwallPoint:
        return True
      for eachWallBlock in blockList:
        if eachBlock_XnY[0] - block_size == eachWallBlock[0] and eachBlock_XnY[1] == eachWallBlock[1]:
          return True
        
  return False

def evalGameOver(blockList):
  for eachBlock in blockList:
    if eachBlock[0] == startpoint_X and eachBlock[1] == startpoint_Y:
      return False
  return True

def initBlock():
  nowBlock=[[startpoint_X,startpoint_Y],
      [startpoint_X+0,startpoint_Y+block_size],
      [startpoint_X+block_size,startpoint_Y+0],
      [startpoint_X+block_size,startpoint_Y+block_size]]
  return nowBlock
  
def drawAllBlock(blockList):
  for eachBlock_XnY in blockList:
    pygame.draw.rect(gameDisplay,blue,[eachBlock_XnY[0],eachBlock_XnY[1],block_size,block_size])
  
def tetris():
  gameLoop = True
  score=0
  fallCount=0
  clock=pygame.time.Clock()
  blockList=[]
  nowBlock=[[startpoint_X,startpoint_Y],
      [startpoint_X+0,startpoint_Y+block_size],
      [startpoint_X+block_size,startpoint_Y+0],
      [startpoint_X+block_size,startpoint_Y+block_size]]
      
  while gameLoop:
    pygame.display.set_caption("Simple TETRIS : score "+str(score))
    frame()
    clock.tick(FPS)

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        quit()    
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
          if not eval_wall(nowBlock,blockList,"left"):
            nowBlock = moveBlock(nowBlock,"left")
        elif event.key == pygame.K_RIGHT:
          if not  eval_wall(nowBlock,blockList,"right"):
            nowBlock = moveBlock(nowBlock,"right")
        elif event.key == pygame.K_UP:
          pass
        elif event.key == pygame.K_DOWN:
          if eval_ground(nowBlock,blockList):
            fallCount == 30
          else:
            nowBlock = moveBlock(nowBlock,"down")
          
    pygame.draw.rect(gameDisplay,blue,[nowBlock[0][0],nowBlock[0][1],block_size,block_size])
    pygame.draw.rect(gameDisplay,blue,[nowBlock[1][0],nowBlock[1][1],block_size,block_size])
    pygame.draw.rect(gameDisplay,blue,[nowBlock[2][0],nowBlock[2][1],block_size,block_size])
    pygame.draw.rect(gameDisplay,blue,[nowBlock[3][0],nowBlock[3][1],block_size,block_size])
    drawAllBlock(blockList)
    fallCount+=1
    
    if fallCount >= 30:
      if eval_ground(nowBlock,blockList):
        for eachBlock_XnY in nowBlock:
          blockList.append(copy.deepcopy(eachBlock_XnY))
        nowBlock = initBlock()
        fallCount=0
      else :
        nowBlock = moveBlock(nowBlock,"down")
        fallCount=0

    pygame.display.update()
    gameLoop = evalGameOver(blockList)

if __name__ == "__main__":
  mainLoop = True
  while mainLoop:
    startScreen()
    tetris()
    gameoverScreen()
