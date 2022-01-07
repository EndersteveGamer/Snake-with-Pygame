from pygame import *
from random import *
from time import sleep,clock
import json
import colorsys as colorsys
import webbrowser

#Initialisation
init()

screen=display.set_mode((800,800),FULLSCREEN)
display.set_caption("Snake!")

snake=None
dead=False
mouse.set_visible(False)
rainbow=[0,0,0]
monochrome=[0,0,0]
tickManager=time.Clock()

#Loading stats
stats=json.load(open("stats.json"))

#Functions
def drawmap():
    k=40
    for x in range(19):
        if k==400:
            width=3
        else:
            width=1
        draw.line(screen,inverted_bg_color,(k,0),(k,800),width)
        k+=40
    k=40
    for x in range(19):
        if k==400:
            width=3
        else:
            width=1
        draw.line(screen,inverted_bg_color,(0,k),(800,k),width)
        k+=40
    draw.line(screen,inverted_bg_color,(0,0),(800,0),3)
    draw.line(screen,inverted_bg_color,(800,0),(800,800),3)
    draw.line(screen,inverted_bg_color,(0,0),(0,800),3)
    draw.line(screen,inverted_bg_color,(0,800),(800,800),3)

def drawApple():
    for apple in appleList:
        x=apple[0]
        y=apple[1]
        draw.rect(screen,(255,0,0),Rect(x*40+1,y*40+1,39,39))

def drawWall():
    for wall in wallList:
        x=wall[0]
        y=wall[1]
        draw.rect(screen,(150,150,150),Rect(x*40+1,y*40+1,39,39))

def drawSnake():
    global rainbow
    global monochrome
    for part in snake.body:
        if part.type=="Head":
            if stats["head_color"]!="rainbow" and stats["head_color"]!="monochrome":
                color=(stats["head_color"][0],stats["head_color"][1],stats["head_color"][2])
            elif stats["head_color"]=="rainbow":
                color=rainbow
            else:
                color=monochrome
        if part.type=="Tail":
            if part.life%3==0:
                if stats["color3"]!="rainbow" and stats["color3"]!="monochrome":
                    color=(stats["color3"][0],stats["color3"][1],stats["color3"][2])
                elif stats["color3"]=="rainbow":
                    color=rainbow
                else:
                    color=monochrome
            if part.life%3==1:
                if stats["color2"]!="rainbow" and stats["color2"]!="monochrome":
                    color=(stats["color2"][0],stats["color2"][1],stats["color2"][2])
                elif stats["color2"]=="rainbow":
                    color=rainbow
                else:
                    color=monochrome
            if part.life%3==2:
                if stats["color1"]!="rainbow" and stats["color1"]!="monochrome":
                    color=(stats["color1"][0],stats["color1"][1],stats["color1"][2])
                elif stats["color1"]=="rainbow":
                    color=rainbow
                else:
                    color=monochrome
        draw.rect(screen,color,Rect(part.x*40+1,part.y*40+1,39,39))

#Orientation:
#0=Left
#1=Up
#2=Right
#3=Down
class Head:
    def __init__(self,length =3):
        self.length=length
        self.x=2
        self.y=9
        self.orientation=2
        self.forbidden_orientation=0
        self.type="Head"

class Tail:
    def __init__(self,life,coords):
        self.life=life
        self.type="Tail"
        self.x=coords[0]
        self.y=coords[1]
    def update(self):
        self.life-=1

class Snake:
    def __init__(self,startingSnake):
        self.body=startingSnake
    def canPlaceApple(self,appleX,appleY):
        for part in self.body:
            if part.x==appleX and part.y==appleY:
                return False
        for apple in appleList:
            if apple[0]==appleX and apple[1]==appleY:
                return False
        sideWalls=0
        for wall in wallList:
            if wall[0]==appleX and wall[1]==appleY:
                return False
            if wall[1]==appleY and (wall[0]==appleX-1 or wall[0]==appleX+1):
                sideWalls+=1
            if wall[0]==appleX and (wall[1]==appleY-1 or wall[1]==appleY+1):
                sideWalls+=1
        if appleX==0 or appleX==19:
            sideWalls+=1
        if appleY==0 or appleY==19:
            sideWalls+=1
        if sideWalls>2:
            return False
        return True

appleList=[]

def placeApple():
    global appleList
    while True:
        appleX=randint(0,19)
        appleY=randint(0,19)
        if snake.canPlaceApple(appleX,appleY)==True:
            appleList.append((appleX,appleY))
            if modeNum==2:
                placeWall()
            break

def update_forbidden():
    if snake.body[0].orientation==0:
        snake.body[0].forbidden_orientation=2
    if snake.body[0].orientation==1:
        snake.body[0].forbidden_orientation=3
    if snake.body[0].orientation==2:
        snake.body[0].forbidden_orientation=0
    if snake.body[0].orientation==3:
        snake.body[0].forbidden_orientation=1

def detectTail(snake):
    headX=snake.body[0].x
    headY=snake.body[0].y
    for part in snake.body:
        if part.type=="Tail":
            if part.x==headX and part.y==headY:
                return True
    return False

def update_snake():
    global dead
    global stats
    snake.body.append(Tail(snake.body[0].length,(snake.body[0].x,snake.body[0].y)))
    if snake.body[0].orientation==0:
        snake.body[0].x-=1
    if snake.body[0].orientation==1:
        snake.body[0].y-=1
    if snake.body[0].orientation==2:
        snake.body[0].x+=1
    if snake.body[0].orientation==3:
        snake.body[0].y+=1
    if snake.body[0].x<0 or snake.body[0].x>19 or snake.body[0].y<0 or snake.body[0].y>19:
        if modeNum!=3:
            dead=True
        if modeNum==3:
            if snake.body[0].x<0:
                snake.body[0].x=19
            if snake.body[0].x>19:
                snake.body[0].x=0
            if snake.body[0].y<0:
                snake.body[0].y=19
            if snake.body[0].y>19:
                snake.body[0].y=0
    if detectTail(snake)==True and modeNum!=3:
        dead=True
    if modeNum==2:
        for wall in wallList:
            if wall[0]==snake.body[0].x and wall[1]==snake.body[0].y:
                dead=True
    if dead==False:
        apple_detected=False
        for apple in appleList:
            if snake.body[0].x==apple[0] and snake.body[0].y==apple[1]:
                snake.body[0].length+=1
                if modeNum!=3:
                    stats["eaten_apples"]+=1
                appleList.remove(apple)
                placeApple()
                apple_detected=True
        if apple_detected==False:
            for part in snake.body:
                if part.type=="Tail":
                    part.life-=1
    for part in snake.body:
        if part.type=="Tail" and part.life==0:
            snake.body.remove(part)

diffNum=0
diffList=["Easy","Normal","Hard","Insane","Nightmare","Hell"]

wallList=[]

def canPlaceWall(wallX,wallY):
        for part in snake.body:
            if part.x==wallX and part.y==wallY:
                return False
        for apple in appleList:
            if apple[0]==wallX and apple[1]==wallY:
                return False
        for wall in wallList:
            if wall[0]==wallX and wall[1]==wallY:
                return False
        if (snake.body[0].x-2==wallX and snake.body[0].y==wallY) or (snake.body[0].x-1==wallX and snake.body[0].y==wallY) or (snake.body[0].x-3==wallX and snake.body[0].y==wallY):
            return False
        if (snake.body[0].x+2==wallX and snake.body[0].y==wallY) or (snake.body[0].x+1==wallX and snake.body[0].y==wallY) or (snake.body[0].x+3==wallX and snake.body[0].y==wallY):
            return False
        if (snake.body[0].x==wallX and snake.body[0].y-2==wallY) or (snake.body[0].x==wallX and snake.body[0].y-1==wallY) or (snake.body[0].x==wallX and snake.body[0].y-3==wallY):
            return False
        if (snake.body[0].x==wallX and snake.body[0].y+2==wallY) or (snake.body[0].x==wallX and snake.body[0].y+1==wallY) or (snake.body[0].x==wallX and snake.body[0].y+3==wallY):
            return False
        return True

def placeWall():
    global wallList
    while True:
        wallX=randint(0,19)
        wallY=randint(0,19)
        if canPlaceWall(wallX,wallY)==True:
            wallList.append((wallX,wallY))
            break

def square_outline(surface,color,topLeft,bottomRight,width =1):
    draw.line(surface,color,(topLeft[0],topLeft[1]),(bottomRight[0],topLeft[1]),width)
    draw.line(surface,color,(topLeft[0],topLeft[1]),(topLeft[0],bottomRight[1]),width)
    draw.line(surface,color,(bottomRight[0],bottomRight[1]),(topLeft[0],bottomRight[1]),width)
    draw.line(surface,color,(bottomRight[0],bottomRight[1]),(bottomRight[0],topLeft[1]),width)

def mouseHitbox(mouseCoords,topLeft,bottomRight):
    if mouseCoords[0]>topLeft[0] and mouseCoords[0]<bottomRight[0] and mouseCoords[1]>topLeft[1]and mouseCoords[1]<bottomRight[1]:
        return True
    return False

def draw_check(pos):
    draw.line(screen,(0,255,0),(pos[0]+10,pos[1]+40),(pos[0]+30,pos[1]+65),6)
    draw.line(screen,(0,255,0),(pos[0]+30,pos[1]+65),(pos[0]+65,pos[1]+10),6)

#Game loop
def game():
    global snake
    global dead
    global appleList
    global selectedOption
    global modeNum
    global wallList
    global rainbow
    global monochrome
    appleList=[]
    dead=False
    snake=Snake([Head(),Tail(2,(1,9)),Tail(1,(0,9))])
    startingTime=round(clock(),0)
    rainbowState=0
    monochromeValue=4
    monochromeDirection=1
    startFrame=clock()
    paused=False
    enterPressed=False
    showPause=False

    placeApple()
    if modeNum==1:
        placeApple()
        placeApple()
    wallList=[]

    while True:
        for events in event.get():
            if events.type==QUIT:
                json.dump(stats,open("stats.json","w"))
                quit()
                exit()
            if events.type==KEYDOWN:
                if events.key==K_ESCAPE:
                    return None
                if (events.key==K_w or events.key==K_UP) and not snake.body[0].forbidden_orientation==1:
                    snake.body[0].orientation=1
                if (events.key==K_a or events.key==K_LEFT) and not snake.body[0].forbidden_orientation==0:
                    snake.body[0].orientation=0
                if (events.key==K_s or events.key==K_DOWN) and not snake.body[0].forbidden_orientation==3:
                    snake.body[0].orientation=3
                if (events.key==K_d or events.key==K_RIGHT) and not snake.body[0].forbidden_orientation==2:
                    snake.body[0].orientation=2
                if events.key==K_RETURN and paused==False and enterPressed==False:
                    paused=True
                    enterPressed=True
                if events.key==K_RETURN and paused==True and enterPressed==False:
                    paused=False
                    enterPressed=True
                    showPause=False
            if events.type==KEYUP and events.key==K_RETURN:
                enterPressed=False
        #Rainbow
        rainbowValue=colorsys.hsv_to_rgb(rainbowState,1,1)
        rainbow=[0,0,0]
        rainbow[0]=rainbowValue[0]*255
        rainbow[1]=rainbowValue[1]*255
        rainbow[2]=rainbowValue[2]*255
        rainbowState+=3/255
        rainbowState=rainbowState%1
        #Monochrome
        monochromeValue+=4*monochromeDirection
        if monochromeValue==0 or monochromeValue>=252:
            monochromeDirection*=-1
        monochrome=[monochromeValue for k in range(3)]
        #Updates and drawing
        if dead==False:
            screen.fill(stats["bg_color"])
            if stats["show_grid"]=="True":
                drawmap()
            if clock()-startFrame>=tickcooldown:
                if paused==False:
                    update_snake()
                if paused==False:
                    update_forbidden()
                else:
                    showPause=True
                startFrame=clock()
            drawApple()
            drawWall()
            drawSnake()
        #Death screen
        if dead==True:
            screen.fill((0,0,0))
            screen.blit(font.SysFont("Comic Sans MS",100).render("You lost!",1,(255,0,0)),Rect(210,280,300,100))
            screen.blit(font.SysFont("Comic Sans MS",50).render("Your score: {0}".format(snake.body[0].length-3),1,(255,0,0)),Rect(250,380,300,100))
            if modeNum==0:
                currentModeID=0
            elif modeNum==2:
                currentModeID=1
            else:
                currentModeID=2
            if snake.body[0].length-3>stats["best_score"][currentModeID] and not (modeNum==3 or modeNum==1):
                if modeNum==0:
                    stats["best_score"][0]=snake.body[0].length-3
                else:
                    stats["best_score"][1]=snake.body[0].length-3
                if stats["best_score"][0]>stats["best_score"][1]:
                    stats["best_score"][2]=stats["best_score"][0]
                else:
                    stats["best_score"][2]=stats["best_score"][1]
                screen.blit(font.SysFont("Comic Sans MS",50).render("New best!",1,(255,255,255)),Rect(300,580,300,100))
            if modeNum==0:
                stats["games_played"][0]+=1
            elif modeNum==2:
                stats["games_played"][1]+=1
            else:
                stats["games_played"][3]+=1
            stats["games_played"][2]=stats["games_played"][0]+stats["games_played"][1]+stats["games_played"][3]
            if not modeNum==3:
                stats["registered_scores"][currentModeID].append(snake.body[0].length-3)
            temp=0
            for x in range(3):
                for k in range(len(stats["registered_scores"][x])):
                    temp+=stats["registered_scores"][x][k]
                if len(stats["registered_scores"][x])!=0:
                    stats["average_score"][x]=temp/len(stats["registered_scores"][x])
            temp=0
            lenTemp=0
            for tab in stats["registered_scores"]:
                lenTemp+=len(tab)
                for element in tab:
                    temp+=element
            stats["average_score"][2]=temp/lenTemp
            stats["time_played"][currentModeID]+=(round(clock(),0)-startingTime)
            stats["time_played"][3]=stats["time_played"][0]+stats["time_played"][1]+stats["time_played"][2]
            #Achievements
            if "First game" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("First game")
            if stats["games_played"][2]>=10 and "Time to play again!" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("Time to play again!")
            if stats["games_played"][2]>=50 and "My favourite game" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("My favourite game")
            if stats["eaten_apples"]>=50 and "My beautiful garden" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("My beautiful garden")
            if stats["eaten_apples"]>=100 and "Serial eater" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("Serial eater")
            if stats["eaten_apples"]>=1000 and "This is never enough" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("This is never enough")
            if stats["time_played"][3]>=1800 and "Time eater" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("Time eater")
            if stats["time_played"][3]>=3600 and "Addict" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("Addict")
            if stats["best_score"][2]>=10 and "New best!" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("New best!")
            if stats["best_score"][2]>=30 and "Snake expert" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("Snake expert")
            if stats["best_score"][2]>=50 and "Veteran" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("Veteran")
            if stats["best_score"][2]>=100 and "Best player in the world" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("Best player in the world")
            if snake.body[0].length-3>=30 and tickcooldown==0.05 and modeNum!=3 and "This is just a dream" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("This is just a dream")
            if tickcooldown==0.03 and "Now this is hard" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("Now this is hard")
            if snake.body[0].length-3>=5 and stats["head_color"]==stats["bg_color"] and stats["color1"]==stats["bg_color"] and stats["color2"]==stats["bg_color"] and stats["color3"]==stats["bg_color"] and modeNum!=3 and "Ninja skills" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("Ninja skills")
            if len(stats["achievements_unlocked"])>=17 and "Snake master" not in stats["achievements_unlocked"]:
                stats["achievements_unlocked"].append("Snake master")
            display.flip()
            sleep(5)
            selectedOption=0
            screen.fill(stats["bg_color"])
            display.flip()
            temp=event.get()
            break
        if showPause==True:
            screen.blit(font.SysFont("Comic Sans MS",100).render("Paused",1,inverted_bg_color),Rect(230,280,300,100))
        display.flip()
        tickManager.tick(60)

#Stats screen
def stats_screen():
    global selectedOption
    global stats
    global diffNum
    easter_egg=0
    easter_egg_text=0
    statsSelectedMode=0
    statsModesList=["Normal mode","Walls mode","All modes"]
    while True:
        for events in event.get():
            if events.type==QUIT:
                json.dump(stats,open("stats.json","w"))
                quit()
                exit()
            if events.type==KEYDOWN and events.key==K_ESCAPE:
                selectedOption=0
                return None
            if events.type==KEYDOWN and (events.key==K_d or events.key==K_RIGHT) and statsSelectedMode<2:
                statsSelectedMode+=1
            if events.type==KEYDOWN and (events.key==K_a or events.key==K_LEFT) and statsSelectedMode>0:
                statsSelectedMode-=1
            if events.type==KEYDOWN and events.key==K_BACKSPACE:
                stats={"registered_scores": [[], [], []], "best_score": [0, 0, 0], "head_color": [0,150,0], "games_played": [0, 0, 0, 0], "average_score": [0, 0, 0, 0, 0], "color3": [0, 255, 0], "eaten_apples": 0, "color1": [255, 200, 0], "color2": [255,100,0], "show_grid": "False", "bg_color": [30, 30, 30], "time_played": [0, 0, 0, 0], "achievements_unlocked":[]}
            if easter_egg==0 and events.type==KEYDOWN and events.key==K_h:
                easter_egg=1
            if easter_egg==1 and events.type==KEYDOWN and events.key==K_e:
                easter_egg=2
            if (easter_egg==2 or easter_egg==3) and events.type==KEYDOWN and events.key==K_l:
                easter_egg+=1
        if easter_egg==4:
            diffNum=5
            easter_egg=0
            easter_egg_text=500
        screen.fill(stats["bg_color"])
        screen.blit(font.SysFont("Comic Sans MS",20).render("Press ESCAPE to exit",1,inverted_bg_color),Rect(10,10,50,30))
        screen.blit(font.SysFont("Comic Sans MS",20).render("Press BACKSPACE to reset stats",1,inverted_bg_color),Rect(490,770,50,30))
        screen.blit(font.SysFont("Comic Sans MS",40).render("Best score: {0}".format(stats["best_score"][statsSelectedMode]),1,inverted_bg_color),Rect(10,100,100,50))
        if statsSelectedMode<=1:
            screen.blit(font.SysFont("Comic Sans MS",40).render("Games played: {0}".format(stats["games_played"][statsSelectedMode]),1,inverted_bg_color),Rect(10,200,100,50))
        else:
            screen.blit(font.SysFont("Comic Sans MS",40).render("Games played: {0}".format(stats["games_played"][2]),1,inverted_bg_color),Rect(10,200,100,50))
        if statsSelectedMode<=1:
            temp=stats["time_played"][statsSelectedMode]
        else:
            temp=stats["time_played"][3]
        hours=int(temp//3600)
        minutes=int(temp//60-60*hours)
        seconds=int(temp-(60*minutes)-(3600*hours))
        if temp>=3600:
            screen.blit(font.SysFont("Comic Sans MS",40).render("Time played: {0} hours {1} minutes {2} seconds".format(hours,minutes,seconds),1,inverted_bg_color),Rect(10,300,100,50))
        elif temp>=60:
            screen.blit(font.SysFont("Comic Sans MS",40).render("Time played: {0} minutes {1} seconds".format(minutes,seconds),1,inverted_bg_color),Rect(10,300,100,50))
        else:
            screen.blit(font.SysFont("Comic Sans MS",40).render("Time played: {0} seconds".format(seconds),1,inverted_bg_color),Rect(10,300,100,50))
        screen.blit(font.SysFont("Comic Sans MS",40).render("Apples eaten: {0}".format(stats["eaten_apples"]),1,inverted_bg_color),Rect(10,500,100,50))
        if statsSelectedMode<=1:
            screen.blit(font.SysFont("Comic Sans MS",40).render("Average score: {0}".format(round(stats["average_score"][statsSelectedMode],2)),1,inverted_bg_color),Rect(10,400,100,50))
        else:
            screen.blit(font.SysFont("Comic Sans MS",40).render("Average score: {0}".format(round(stats["average_score"][2],2)),1,inverted_bg_color),Rect(10,400,100,50))
        if easter_egg_text>0:
            screen.blit(font.SysFont("Comic Sans MS",20).render("New difficulty unlocked!",1,inverted_bg_color),Rect(10,770,50,30))
            easter_egg_text-=1
        screen.blit(font.SysFont("Comic Sans MS",50).render(statsModesList[statsSelectedMode],1,inverted_bg_color),Rect(250,650,100,50))
        display.flip()

#Snake skins
def snake_skins():
    global selectedOption
    errorText=""
    errorTextLife=0
    achievementsList=[["This is just a dream","First game","Time to play again!","My favourite game","My beautiful garden","Serial eater"],["Now this is hard","This is never enough","","","",""],["Ninja skills","New best!","Snake expert","Veteran","Best player in the world","Snake master"]]
    rainbowState=0
    monochromeValue=4
    monochromeDirection=1
    mouse.set_visible(True)
    selectedSquare=3
    colorList=[[stats["bg_color"],(255,0,200),(90,20,160),(0,0,150),(0,0,255),(0,255,255)],[(100,0,0),(255,0,0),(255,100,0),(255,200,0),(0,255,0),(0,150,0)],[(0,0,0),(150,150,150),(75,75,75),(235,235,235),"monochrome","rainbow"]]
    skin={"head_color": stats["head_color"],"color1": stats["color1"],"color2":stats["color2"],"color3":stats["color3"]}
    while True:
        for events in event.get():
            if events.type==QUIT:
                stats["head_color"]=skin["head_color"]
                stats["color1"]=skin["color1"]
                stats["color2"]=skin["color2"]
                stats["color3"]=skin["color3"]
                json.dump(stats,open("stats.json","w"))
                quit()
                exit()
            if events.type==KEYDOWN and events.key==K_ESCAPE:
                stats["head_color"]=skin["head_color"]
                stats["color1"]=skin["color1"]
                stats["color2"]=skin["color2"]
                stats["color3"]=skin["color3"]
                selectedOption=0
                mouse.set_visible(False)
                return None
            if events.type==MOUSEBUTTONDOWN and events.button==1:
                if mouseHitbox(events.pos,(6*80,2*80),(6*80+78,2*80+78))==True:
                    selectedSquare=3
                if mouseHitbox(events.pos,(5*80,2*80),(5*80+78,2*80+78))==True:
                    selectedSquare=2
                if mouseHitbox(events.pos,(4*80,2*80),(4*80+78,2*80+78))==True:
                    selectedSquare=1
                if mouseHitbox(events.pos,(3*80,2*80),(3*80+78,2*80+78))==True:
                    selectedSquare=0
                #Color list hitbox
                for y in range(len(colorList)):
                    for x in range(len(colorList[y])):
                        if mouseHitbox(events.pos,((x+2)*80,(y+6)*80),((x+2)*80+78,(y+6)*80+78))==True:
                            if achievementsList[y][x]=="" or achievementsList[y][x] in stats["achievements_unlocked"]:
                                temp=colorList[y][x]
                                if selectedSquare==3:
                                    skin["head_color"]=temp
                                if selectedSquare==2:
                                    skin["color3"]=temp
                                if selectedSquare==1:
                                    skin["color1"]=temp
                                if selectedSquare==0:
                                    skin["color2"]=temp
                            else:
                                errorText="You need to complete the {0} achievement to unlock this!".format(achievementsList[y][x])
                                errorTextLife=200
        screen.blit(font.SysFont("Comic Sans MS",20).render("Press ESCAPE to exit",1,inverted_bg_color),Rect(10,10,50,30))
        #Rainbow
        rainbowValue=colorsys.hsv_to_rgb(rainbowState,1,1)
        rainbow=[0,0,0]
        rainbow[0]=rainbowValue[0]*255
        rainbow[1]=rainbowValue[1]*255
        rainbow[2]=rainbowValue[2]*255
        rainbowState+=3/255
        rainbowState=rainbowState%1
        #Monochrome
        monochromeValue+=4*monochromeDirection
        if monochromeValue==0 or monochromeValue>=252:
            monochromeDirection*=-1
        monochrome=[monochromeValue for k in range(3)]
        #Snake preview
        if skin["head_color"]!="rainbow" and skin["head_color"]!="monochrome":
            draw.rect(screen,skin["head_color"],Rect(6*80,2*80,78,78))
        elif skin["head_color"]=="rainbow":
            draw.rect(screen,rainbow,Rect(6*80,2*80,78,78))
        else:
            draw.rect(screen,monochrome,Rect(6*80,2*80,78,78))
        if skin["color3"]!="rainbow" and skin["color3"]!="monochrome":
            draw.rect(screen,skin["color3"],Rect(5*80,2*80,78,78))
        elif skin["color3"]=="rainbow":
            draw.rect(screen,rainbow,Rect(5*80,2*80,78,78))
        else:
            draw.rect(screen,monochrome,Rect(5*80,2*80,78,78))
        if skin["color1"]!="rainbow" and skin["color1"]!="monochrome":
            draw.rect(screen,skin["color1"],Rect(4*80,2*80,78,78))
        elif skin["color1"]=="rainbow":
            draw.rect(screen,rainbow,Rect(4*80,2*80,78,78))
        else:
            draw.rect(screen,monochrome,Rect(4*80,2*80,78,78))
        if skin["color2"]!="rainbow" and skin["color2"]!="monochrome":
            draw.rect(screen,skin["color2"],Rect(3*80,2*80,78,78))
        elif skin["color2"]=="rainbow":
            draw.rect(screen,rainbow,Rect(3*80,2*80,78,78))
        else:
            draw.rect(screen,monochrome,Rect(3*80,2*80,78,78))
        if selectedSquare==3:
            square_outline(screen,inverted_bg_color,(6*80-2,2*80-2),(7*80-2,3*80-2),3)
        if selectedSquare==2:
            square_outline(screen,inverted_bg_color,(5*80-2,2*80-2),(6*80-2,3*80-2),3)
        if selectedSquare==1:
            square_outline(screen,inverted_bg_color,(4*80-2,2*80-2),(5*80-2,3*80-2),3)
        if selectedSquare==0:
            square_outline(screen,inverted_bg_color,(3*80-2,2*80-2),(4*80-2,3*80-2),3)
        #Border
        square_outline(screen,inverted_bg_color,(2*80-2,6*80-2),(8*80-1,9*80-1),3)
        #Error text
        if errorTextLife>0:
            screen.blit(font.SysFont("Comic Sans MS",20).render(errorText,1,inverted_bg_color),Rect(30,400,100,50))
            errorTextLife-=1
        #Color list display
        for y in range(len(colorList)):
            for x in range(len(colorList[y])):
                if colorList[y][x]!="rainbow" and colorList[y][x]!="monochrome":
                    draw.rect(screen,colorList[y][x],Rect((x+2)*80,(y+6)*80,78,78))
                elif colorList[y][x]=="rainbow":
                    draw.rect(screen,rainbow,Rect((x+2)*80,(y+6)*80,78,78))
                else:
                    draw.rect(screen,monochrome,Rect((x+2)*80,(y+6)*80,78,78))
        display.flip()
        screen.fill(stats["bg_color"])
        tickManager.tick(60)

#Options menu
def options():
    global stats
    global inverted_bg_color
    selectedOption2=0
    mouse.set_visible(True)
    while True:
        for events in event.get():
            if events.type==QUIT:
                json.dump(stats,open("stats.json","w"))
                quit()
                exit()
            if events.type==KEYDOWN and events.key==K_ESCAPE:
                mouse.set_visible(False)
                return None
            if events.type==MOUSEBUTTONDOWN and events.button==1:
                if mouseHitbox(events.pos,(660,770),(800,800))==True:
                    webbrowser.open("stats.json")
                if mouseHitbox(events.pos,(495,110),(570,185))==True:
                    if stats["show_grid"]=="True":
                        stats["show_grid"]="False"
                    else:
                        stats["show_grid"]="True"
                if mouseHitbox(events.pos,(525,310),(600,385))==True:
                    if stats["bg_color"]==[255,255,255]:
                        inverted_bg_color=[255,255,255]
                        if stats["head_color"]==stats["bg_color"]:
                            stats["head_color"]=[30,30,30]
                        if stats["color1"]==stats["bg_color"]:
                            stats["color1"]=[30,30,30]
                        if stats["color2"]==stats["bg_color"]:
                            stats["color2"]=[30,30,30]
                        if stats["color3"]==stats["bg_color"]:
                            stats["color3"]=[30,30,30]
                        stats["bg_color"]=[30,30,30]
                    else:
                        if "Why would you do that?" not in stats["achievements_unlocked"]:
                            stats["achievements_unlocked"].append("Why would you do that?")
                        inverted_bg_color=[0,0,0]
                        if stats["head_color"]==stats["bg_color"]:
                            stats["head_color"]=[255,255,255]
                        if stats["color1"]==stats["bg_color"]:
                            stats["color1"]=[255,255,255]
                        if stats["color2"]==stats["bg_color"]:
                            stats["color2"]=[255,255,255]
                        if stats["color3"]==stats["bg_color"]:
                            stats["color3"]=[255,255,255]
                        stats["bg_color"]=[255,255,255]
        #Open save file
        screen.blit(font.SysFont("Comic Sans MS",20).render("Open save file",1,inverted_bg_color),Rect(660,770,50,30))
        #Show grid option
        screen.blit(font.SysFont("Comic Sans MS",60).render("Show grid",1,inverted_bg_color),Rect(200,100,100,50))
        if stats["show_grid"]=="True":
            draw_check((495,110))
        square_outline(screen,inverted_bg_color,(495,110),(570,185),3)
        #Light mode option
        screen.blit(font.SysFont("Comic Sans MS",60).render("Light mode",1,inverted_bg_color),Rect(200,300,100,50))
        if stats["bg_color"]==[255,255,255]:
            draw_check((525,310))
        square_outline(screen,inverted_bg_color,(525,310),(600,385),3)
        screen.blit(font.SysFont("Comic Sans MS",20).render("Press ESCAPE to exit",1,inverted_bg_color),Rect(10,10,50,30))
        display.flip()
        screen.fill(stats["bg_color"])

achievementsList=["First game"        ,"Time to play again!","My favourite game","My beautiful garden","Serial eater"  ,"This is never enough","Time eater"         ,"Addict"         ,"New best!"                      ,"Snake expert"                   ,"Veteran"                        ,"Best player in the world"         ,"This is just a dream"                           ,"Snek!","Now this is hard"                            ,"Ninja skills"                              ,"Why would you do that?","Snake master"             ]
achievementsDesc=["Just play the game","Play 10 times"      ,"Play 50 times"   ,"Eat 50 apples"      ,"Eat 100 apples","Eat 1000 apples"     ,"Play for 30 minutes","Play for 1 hour","Have a best score of 10 or more","Have a best score of 30 or more","Have a best score of 50 or more","Have a best score of 100 or more!","Reach a score of 30 in the nightmare difficulty","Snek ","Play in hell difficulty (hint: stats screen)","Reach a score of 5 with an invisible snake","Use light mode"        ,"Complete all achievements"]
if "This is just a dream" in stats["achievements_unlocked"]:
    achievementsDesc[14]="Play in hell difficulty (type hell in stats screen)"

def achievements():
    scrollPos=30
    while True:
        for events in event.get():
            if events.type==QUIT:
                json.dump(stats,open("stats.json","w"))
                quit()
                exit()
            if events.type==KEYDOWN and events.key==K_ESCAPE:
                return None
            if events.type==MOUSEBUTTONDOWN and events.button==4 and scrollPos<30:
                scrollPos+=30
            if events.type==MOUSEBUTTONDOWN and events.button==5 and scrollPos>-1860:
                scrollPos-=30
        for k in range(len(achievementsList)):
            screen.blit(font.SysFont("Comic Sans MS",40).render(achievementsList[k],1,inverted_bg_color),Rect(250,scrollPos+k*150,100,50))
            screen.blit(font.SysFont("Comic Sans MS",20).render(achievementsDesc[k],1,inverted_bg_color),Rect(250,scrollPos+k*150+55,100,50))
            square_outline(screen,inverted_bg_color,(700,scrollPos+k*150+10),(775,scrollPos+k*150+85),3)
            if achievementsList[k] in stats["achievements_unlocked"]:
                draw_check((700,scrollPos+k*150+10))
        screen.blit(font.SysFont("Comic Sans MS",20).render("Press ESCAPE to exit",1,inverted_bg_color),Rect(10,10,50,30))
        display.flip()
        screen.fill(stats["bg_color"])

#Main menu
if stats["bg_color"]==[255,255,255]:
    inverted_bg_color=[0,0,0]
else:
    inverted_bg_color=[255,255,255]
exitTime=0
exitPressed=False
selectedOption=0
modeNum=0
modeList=["Normal","Triple apple","Walls","No dying"]
pressed=0
dontSave=False
fullscreen=True
snek=False
def snekRand():
    global snek
    if randint(0,19)==1:
        snek=True
    else:
        snek=False
snekRand()

while True:
    for events in event.get():
        if events.type==QUIT:
            json.dump(stats,open("stats.json","w"))
            quit()
            exit()
        #Exit
        if events.type==KEYDOWN and events.key==K_ESCAPE:
            exitPressed=True
        if events.type==KEYUP and events.key==K_ESCAPE:
            exitPressed=False
            exitTime=0
        #Start
        if events.type==KEYDOWN and events.key==K_RETURN and selectedOption==0:
            #Game starting countdown
            screen.fill(stats["bg_color"])
            screen.blit(font.SysFont("Comic Sans MS",100).render("Starting in 3",1,inverted_bg_color),Rect(100,250,400,200))
            display.flip()
            screen.fill(stats["bg_color"])
            sleep(1)
            screen.blit(font.SysFont("Comic Sans MS",100).render("Starting in 2",1,inverted_bg_color),Rect(100,250,400,200))
            display.flip()
            screen.fill(stats["bg_color"])
            sleep(1)
            screen.blit(font.SysFont("Comic Sans MS",100).render("Starting in 1",1,inverted_bg_color),Rect(100,250,400,200))
            display.flip()
            screen.fill(stats["bg_color"])
            sleep(1)
            display.flip()
            game()
            selectedOption=0
            snekRand()
        #Options selection
        if events.type==KEYDOWN:
            if pressed==0:
                if (events.key==K_w or events.key==K_UP) and selectedOption>-1:
                        selectedOption-=1
                        pressed+=1
                if (events.key==K_s or events.key==K_DOWN) and selectedOption<5:
                    selectedOption+=1
                    pressed+=1
        #Reset pressed
        if events.type==KEYUP and (events.key==K_w or events.key==K_UP or events.key==K_s or events.key==K_DOWN or events.key==K_d or events.key==K_RIGHT or events.key==K_a or events.key==K_LEFT or events.key==K_f) and pressed>0:
            pressed-=1
        #Difficulty selection
        if events.type==KEYDOWN and selectedOption==1:
            if pressed==0:
                if (events.key==K_d or events.key==K_RIGHT) and diffNum<4:
                    diffNum+=1
                if(events.key==K_a or events.key==K_LEFT) and diffNum>0:
                    diffNum-=1
        #Achievements
        if events.type==KEYDOWN and events.key==K_RETURN and selectedOption==3:
            achievements()
            snekRand()
        #Mode selection
        if events.type==KEYDOWN and selectedOption==2:
            if pressed==0:
                if (events.key==K_d or events.key==K_RIGHT) and modeNum<3:
                    modeNum+=1
                if(events.key==K_a or events.key==K_LEFT) and modeNum>0:
                    modeNum-=1
        #Stats
        if events.type==KEYDOWN and events.key==K_RETURN and selectedOption==5:
            stats_screen()
            snekRand()
        #Don't save stats
        if events.type==KEYDOWN and (events.key==K_LSHIFT or events.key==K_RSHIFT):
            dontSave=True
        if events.type==KEYUP and (events.key==K_LSHIFT or events.key==K_RSHIFT):
            dontSave=False
        #Snake skins
        if events.type==KEYDOWN and events.key==K_RETURN and selectedOption==4:
            snake_skins()
            snekRand()
        #Toggle fullscreen
        if events.type==KEYDOWN and events.key==K_f and pressed==0:
            pressed+=1
            if fullscreen==True:
                screen=display.set_mode((800,800))
                fullscreen=False
            else:
                screen=display.set_mode((800,800),FULLSCREEN)
                fullscreen=True
        #Options menu
        if events.type==KEYDOWN and events.key==K_RETURN and selectedOption==-1:
            options()
            snekRand()
    #Exit management
    if exitPressed==True:
        exitTime+=4
        if exitTime>200:
            draw.rect(screen,inverted_bg_color,Rect(10,10,10,30))
        if exitTime>400:
            draw.rect(screen,inverted_bg_color,Rect(30,10,10,30))
        if exitTime>600:
            draw.rect(screen,inverted_bg_color,Rect(50,10,10,30))
        if exitTime>800:
            draw.rect(screen,inverted_bg_color,Rect(70,10,10,30))
    if exitTime>1000:
        if dontSave==False:
            json.dump(stats,open("stats.json","w"))
        quit()
        exit()
    if exitPressed==False:
        screen.blit(font.SysFont("Comic Sans MS",20).render("Hold ESCAPE to exit",1,inverted_bg_color),Rect(10,10,50,30))
    #Title
    if snek==False:
        screen.blit(font.SysFont("Comic Sans MS",100).render("Snake!",1,inverted_bg_color),Rect(250,50,400,200))
    else:
        screen.blit(font.SysFont("Comic Sans MS",100).render("Snek!",1,inverted_bg_color),Rect(270,50,400,200))
        if "Snek!" not in stats["achievements_unlocked"]:
            stats["achievements_unlocked"].append("Snek!")
    #Options
    if selectedOption==-1:
        screen.blit(font.SysFont("Comic Sans MS",40).render("Options",1,(150,150,150)),Rect(645,0,100,50))
    else:
        screen.blit(font.SysFont("Comic Sans MS",40).render("Options",1,inverted_bg_color),Rect(645,0,100,50))
    if selectedOption==0:
        screen.blit(font.SysFont("Comic Sans MS",40).render("Start",1,(150,150,150)),Rect(340,250,100,50))
    else:
        screen.blit(font.SysFont("Comic Sans MS",40).render("Start",1,inverted_bg_color),Rect(340,250,100,50))
    if selectedOption==1:
        screen.blit(font.SysFont("Comic Sans MS",40).render("Difficulty: {0}".format(diffList[diffNum]),1,(150,150,150)),Rect(240,350,100,50))
    else:
        screen.blit(font.SysFont("Comic Sans MS",40).render("Difficulty: {0}".format(diffList[diffNum]),1,inverted_bg_color),Rect(240,350,100,50))
    if selectedOption==2:
        screen.blit(font.SysFont("Comic Sans MS",40).render("Mode: {0}".format(modeList[modeNum]),1,(150,150,150)),Rect(260,450,100,50))
    else:
        screen.blit(font.SysFont("Comic Sans MS",40).render("Mode: {0}".format(modeList[modeNum]),1,inverted_bg_color),Rect(260,450,100,50))
    if selectedOption==3:
        screen.blit(font.SysFont("Comic Sans MS",40).render("Achievements",1,(150,150,150)),Rect(250,550,100,50))
    else:
        screen.blit(font.SysFont("Comic Sans MS",40).render("Achievements",1,inverted_bg_color),Rect(250,550,100,50))
    if selectedOption==4:
        screen.blit(font.SysFont("Comic Sans MS",40).render("Snake skins",1,(150,150,150)),Rect(280,650,100,50))
    else:
        screen.blit(font.SysFont("Comic Sans MS",40).render("Snake skins",1,inverted_bg_color),Rect(280,650,100,50))
    if selectedOption==5:
        screen.blit(font.SysFont("Comic Sans MS",40).render("Stats",1,(150,150,150)),Rect(685,740,100,50))
    else:
        screen.blit(font.SysFont("Comic Sans MS",40).render("Stats",1,inverted_bg_color),Rect(685,740,100,50))
    #Difficulty update
    difficulty=diffList[diffNum]
    if difficulty=="Easy":
        tickcooldown=0.45
    elif difficulty=="Normal":
        tickcooldown=0.35
    elif difficulty=="Hard":
        tickcooldown=0.25
    elif difficulty=="Insane":
        tickcooldown=0.10
    elif difficulty=="Nightmare":
        tickcooldown=0.05
    elif difficulty=="Hell":
        tickcooldown=0.03
    #Best score display
    screen.blit(font.SysFont("Comic Sans MS",30).render("Best score: {0}".format(stats["best_score"][2]),1,inverted_bg_color),Rect(10,750,100,50))
    #Update
    display.flip()
    screen.fill(stats["bg_color"])
