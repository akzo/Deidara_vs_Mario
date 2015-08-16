import pygame;
import pyganim;
import random;
import sys;
from pygame.locals import *;

#inicializaciya
pygame.init();
myfont = pygame.font.SysFont("Verdana", 55);
menu_font =  pygame.font.SysFont("Verdana", 45);
score_font =  pygame.font.SysFont("Verdana", 35);
window=pygame.display.set_mode((600, 500));
pygame.display.set_caption("Deidara!");
screen=pygame.Surface((600,500));
Menu = pygame.Surface((600,500));

#zagrujaem muziku i zvuki
vzriv = pygame.mixer.Sound("AtomicBomb.wav");
pygame.mixer.music.load("Super Mario Bros. medley.mp3")

def menu():
    play_g = True;
    color_q = (20,30,40);
    color_p = (10,200,10);
    cikl = True;
    while cikl:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit();
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    color_p=(20,30,40);
                    color_q = (10,200,10);
                    play_g = False;
                elif event.key == pygame.K_UP :
                    color_q = (20,30,40);
                    color_p = (10,200,10);
                    play_g = True;
                elif event.key == pygame.K_RETURN :
                    if play_g == True:
                        cikl = False;
                        pygame.time.delay(250);
                        break;
                    elif play_g == False:
                        sys.exit();


        quit = menu_font.render("Quit", 1, color_q);
        play = menu_font.render("Play", 1, color_p);
        Menu.fill((0,0,139));
        window.blit(Menu,(0,0));
        window.blit(play,(250,180));
        window.blit(quit,(245,280));
        pygame.display.flip();
        pygame.time.delay(10);
menu();

#Zagrujaem izobrajeniya
Ogon = pyganim.PygAnimation([("ogon1.png", 0.3),
                             ("ogon2.png", 0.3),
                             ("ogon3.png", 0.3),
                             ("ogon4.png", 0.3)])

Mario = pyganim.PygAnimation([("Mario.png", 0.7),
                              ("Mario1.png",0.5),
                              ("Mario2.png",0.5),
                              ("Mario3.png",0.8)])

Deidara = pyganim.PygAnimation([("Deidara.gif", 0.3),
                                ("Deidara2.gif",0.2)])

Oblako =  pyganim.PygAnimation([("oblako.gif", 1)])

#sprite
class Hero():
    def __init__(self,x, y, character):
        self.x = x;
        self.y = y;
        self.character = character;

    def show(self):
        (self.character).blit(screen,(self.x,self.y));

    def move(self,x,y):
        self.x+=x;
        self.y+=y;

    def play(self,bool):
        if bool == True:
            (self.character).play();
        elif bool == False:
            (self.character).stop();


#obyekti
deidara = Hero(100,250, Deidara);
oblako = Hero(100,0,Oblako);
mario = Hero(140,10, Mario);

oblako.go_Right = True;
mario.go_down = False;
deidara.killed = False;

deidara.play(True);
oblako.play(True);
#posledni koordinati deidari :(
d_x=0;
d_y=0;

label = myfont.render("", 1, (25,255,12))
rnd = random.randint(1, 460);
pygame.key.set_repeat(1, 1);

Score = 0;

pygame.mixer.music.play(-1);

loop = True;
while loop:
    score = score_font.render("Your score: "+str(Score), 1 , (25,255,12));


    #proveraem sobitiya
    for event in pygame.event.get():

        if event.type == pygame.QUIT: #Vixod
            loop = False;

        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_LEFT and deidara.x > 0:
                deidara.move(-8,0);

            if event.key==pygame.K_RIGHT and deidara.x<480:
                deidara.move(8,0);


    #peredvijenie oblaka
    if oblako.go_Right == True:
        oblako.move(10,0);
    elif oblako.go_Right == False:
        oblako.move(-10,0);

    if oblako.x==460:
        oblako.go_Right = False;
    elif oblako.x == 0:
        oblako.go_Right = True;


    #peredvijenie mario
    if oblako.x >= rnd-10 and oblako.x <= rnd+10: # esli oblako.x=slu4aynomu 4islu zapuskaem Mario
         mario.go_down = True;
         rnd = random.randint(1, 460);


    if mario.go_down == True and deidara.killed == False :
        mario.play(True);
        if mario.y >= 300:
            mario.go_down = False;
            Score += 1;
            mario.play(False);
            mario.y = 10;
        elif mario.y >= 250 and (mario.x > deidara.x-20) and (mario.x<deidara.x+80):
            d_x = deidara.x;
            d_y = deidara.y;
            deidara.play(False);
            mario.play(False);
            vzriv.play();
            Ogon.play();
            oblako.play(False);
            deidara.killed = True;
            label = myfont.render("GAME OVER!", 1, (25,255,12));

        else:

            mario.move(0,15);

    else:
        mario.move((oblako.x-mario.x),0)



    #otobrajenie
    screen.fill((25,103,255));
    Ogon.blit(screen,(d_x,d_y));
    screen.blit(label, (130, 200));
    screen.blit(score, (340, 420));
    mario.show();
    deidara.show();
    oblako.show();

    window.blit(screen,(0,0));
    pygame.display.flip();

    pygame.time.delay(100);
