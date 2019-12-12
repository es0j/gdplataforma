import pygame
import math
import os


G_WIDTH=1200
G_HEIGHT=600
GRAVITY=pygame.Vector2(0,2)
GAME_CLOCK=30
BLOCK_SIZE=32
def readMap(mapPath):
        with open(mapPath,"r") as f:
                lines=f.read().split("\n")

        rect_matrix=[]
        for  i in range(len(lines)):
                
                width=1
                started=False
                block_type=0
                print(len(lines[i]))
                for j in range(len(lines[i])):
                        print(lines[i][j],end="")
                        if lines[i][j]=="A":
                                if started:
                                        width+=1
                                else:
                                        begin=j*BLOCK_SIZE
                                        started=True
                                        block_type="A"
                        if lines[i][j]=="B":
                                if started:
                                        width+=1
                                else:
                                        begin=j*BLOCK_SIZE
                                        started=True
                                        block_type="B"
                        if lines[i][j]==" ":
                                if started:
                                        if block_type=="A":
                                                rect_matrix.append(Platform(pygame.Rect(begin,BLOCK_SIZE*i,width*BLOCK_SIZE,BLOCK_SIZE)))
                                        elif block_type=="B":
                                                rect_matrix.append(Platform(pygame.Rect(begin,BLOCK_SIZE*i,width*BLOCK_SIZE,BLOCK_SIZE)))
                                        width=1
                                started=False
                        
        for i in rect_matrix:
                print(i.rect)
        return rect_matrix
                            



def OpenSprites(path,width,height):
        files = os.listdir(path)
        files.sort()
        if len(files)>100:
                print("this paste have more than 100 files on folder %s. Check for errors"%path)
                exit()
        for i in range (len(files)):
                img=pygame.image.load(path+"/"+files[i])
                scaled=pygame.transform.scale(img,(width,height))
                files[i]=scaled
                
        return files



class Entity(pygame.sprite.Sprite):
        def __init__(self,color,rect,path="", *groups):
                super().__init__(*groups)
                self.rect = rect 
                
                if (path==""):
                    self.image =  pygame.Surface((rect.width,rect.height))
                    self.image.fill(color)
                else:
                    
                    
                    img=pygame.image.load(path)
                    self.image=pygame.transform.scale(img,(rect.width,rect.height))
                   
                
                             
        


class Player(Entity):
        def __init__(self,rect,
                path_run="player/sans/right",path_jump="player/jump",moveSpeed=5,max_jump=100,max_run=100,*groups):
                Entity.__init__(self,pygame.Color("#FF00FF"),rect)
                self.run=OpenSprites(path_run,width=rect.width,height=rect.height)
                #self.rect=rect
                self.is_jumping=True
                self.is_running=False
                self.is_left=False
                
                self.jump_count=0
                self.run_count=0
                self.len_run=len(self.run)
                self.max_jump=max_jump
                self.max_run=max_run
                self.speed=pygame.Vector2((0,0))
                self.jump_power=30
                self.moveSpeed=moveSpeed
                self.gold=0
                self.vida=100



        def Update(self,manager):

                plataforms=manager.plataforms
                objects=manager.objects
                self.GetInput()
                self.is_jumping=True
                if self.is_jumping==True:
                         
                        self.speed+=GRAVITY
                        self.jump_count+=1
                        if self.jump_count > self.max_jump:
                                self.jump_count = 0
                                self.jumping = False
                                self.run_count=0
                                

                if self.is_running:
                        self.run_count+=1

                self.image=self.run[self.run_count%self.len_run]
                if self.is_left:
                        self.image = pygame.transform.flip(self.image, 1,0)
                

                self.rect.left+=self.speed.x
                self.collide(self.speed.x,0,plataforms)

                if self.is_jumping:
                        self.rect.bottom+=self.speed.y
                self.collide(0,self.speed.y,plataforms)
                #print("drawing")
                #self.rect=pygame.Rect(110,110,32,32)
                #win.blit(self.image,self.rect.topleft)
                self.interact(manager)
                
        def interact(self,manager):
            objects=manager.objects
            for o in objects:
                if pygame.sprite.collide_rect(self,o):
                    if isinstance(o,Coin):
                            self.gold+=10
                            objects.remove(o)
                            print
                    elif isinstance(o,Lava):
                        self.TirarVida(o.damage,manager)
        def TirarVida(self,dano,manager):
            self.vida-=dano
            if self.vida<0:
                manager.restart()

               

        def collide(self,xvel,yvel,obstacles):
                for o in obstacles:
                        if pygame.sprite.collide_rect(self,o):
                                collidad=True
                                if xvel >0:
                                        self.rect.right= o.rect.left
                                elif xvel < 0 :
                                        self.rect.left = o.rect.right
                                elif yvel > 0 :
                                        self.rect.bottom = o.rect.top
                                        self.is_jumping=False
                                        self.speed.y=0
                                elif yvel <0:
                                        self.rect.top = o.rect.bottom




        def GetInput(self):
                keyboard=pygame.key.get_pressed()
                
                if keyboard[pygame.K_UP]:
                        if not self.is_jumping:
                                self.speed.y-=self.jump_power
                                self.is_jumping=True

                elif keyboard[pygame.K_LEFT]:
                        self.speed.x = -self.moveSpeed
                        self.is_running=True
                        self.is_left=True
                        
                        
                elif keyboard[pygame.K_RIGHT]:
                        self.speed.x = self.moveSpeed
                        self.is_running=True
                        self.is_left=False
                else:
                        self.speed.x=0
                        self.is_running=False
class dinamicSprite(pygame.sprite.Sprite):
    def __init__(self,rect,path="",*groups):
        super().__init__(*groups)
        self.rect = rect

        self.sprites=OpenSprites(path,32,32)
        self.sprites_len=len(self.sprites)
        self.image=self.sprites[0]
        self.count=0
    def Update(self,manager):
        self.image=self.sprites[self.count%self.sprites_len]
        self.count+=1

class Coin(dinamicSprite):
    def __init__(self,rect,path="",*groups):
        super().__init__(rect,path,*groups)
        self.gold=10
class Lava(dinamicSprite):
     def __init__(self,rect,path="",*groups):
        super().__init__(rect,path,*groups)
        self.damage=10


class FlagTopo(dinamicSprite):
     def __init__(self,rect,path="",*groups):
        super().__init__(rect,path,*groups)
        
class Flag(Platform):
     def __init__(self,rect,path="",*groups):
        super().__init__(rect,path,*groups)

class Platform(Entity):
        def __init__(self, rect, *groups):
                super().__init__(pygame.Color("#FF00FF"), rect, *groups)
class End(Entity):
        def __init__(self, rect, *groups):
                super().__init__(pygame.Color("#0022FF"), rect, *groups)

                
class MainGame:
        def __init__(self,title="jogo1",width=G_WIDTH,height=G_HEIGHT):
                pygame.init()
                beginPlayer=pygame.Rect(600,0,32,32)

                self.clock_tick_rate= GAME_CLOCK
                self.size = (width, height)

                self.win = pygame.display.set_mode((width,height))
                pygame.display.set_caption(title)
                self.clock=pygame.time.Clock() 


                
                self.objects=[]
                self.plataforms=[]
                self.readMap2("maps/map2.txt")
                
                
                self.player=Player(rect=beginPlayer)
                
                self.objects.append(self.player)
                self.cam=Camera(self.win,self.objects,self.plataforms,focus=self.player.rect)
                self.mainLoop()
        def mainLoop(self):
                is_running=True
                while is_running == True:
                        
                        for e in pygame.event.get():
                                if e.type == pygame.QUIT: 
                                        return


                        
                        for i in self.objects:
                            i.Update(self)
                        
                        self.cam.DrawFrame(self.objects,self.plataforms)     
                                  
                        pygame.display.flip()
                        self.clock.tick(self.clock_tick_rate)
        def readMap2(self,mapPath):
            with open(mapPath,"r") as f:
                    lines=f.read().split("\n")

            rect_matrix=[]
            for  i in range(len(lines)):
                    for j in range(len(lines[i])):
                            print(lines[i][j],end="")
                            if lines[i][j]=="G":
                                    self.plataforms.append(Platform(pygame.Rect(BLOCK_SIZE*j,BLOCK_SIZE*i,BLOCK_SIZE,BLOCK_SIZE),"textura/grass.png"))
                            elif lines[i][j]=="M":
                                    self.plataforms.append(End(pygame.Rect(BLOCK_SIZE*j,BLOCK_SIZE*i,BLOCK_SIZE,BLOCK_SIZE),"textura/marble.png"))
                            elif lines[i][j]=="C":
                                    self.objects.append(Coin(pygame.Rect(BLOCK_SIZE*j,BLOCK_SIZE*i,BLOCK_SIZE,BLOCK_SIZE),"textura/coins/"))
                            elif lines[i][j]=="L":
                                    self.objects.append(Lava(pygame.Rect(BLOCK_SIZE*j,BLOCK_SIZE*i,BLOCK_SIZE,BLOCK_SIZE),"textura/lava/"))
                            
            for i in rect_matrix:
                    print(i.rect)
            
        def restart(self):
            print("restarted")
            self.__init__()
                
                
class Camera:
    def __init__(self,win,objects,plataforms,focus,bg_path="bg.bmp"):
        self.win=win
        self.focus=focus
        self.bg=pygame.image.load(bg_path).convert()
        self.limiteR=0
        self.limiteL=9999
        self.lastPos=0
        self.offset=pygame.Vector2(G_WIDTH/2,0)
    def DrawFrame(self,objects,plataforms):
        self.win.blit(self.bg,[ 0,0])


        allobjects=objects+plataforms

        for i in allobjects:
            
            xpos=i.rect.x-self.focus.x+self.offset.x
         
            ypos=i.rect.top
            self.win.blit(i.image,(xpos,ypos))
        #for i in plataforms:
        #    self.win.blit(i.image,(i.rect.left-self.focus.left+G_WIDTH/2,i.rect.top))


def subTuple(t1,t2):
    return (t1[0]-t2[0],t1[1]-t2[1])


if __name__ == "__main__":
           j=MainGame()
                        

