import pygame
import os
import predict as pre

pygame.init()
win = pygame.display.set_mode((1200, 720)) # Display i 1200x720 pixels

# Setup images
bg = [pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\bg\\', 'bgs'+str(i)+'.png')) for i in range(0,6)]
cntDown_show = [pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\show\\', '3.png')), 
        pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\show\\', '2.png')),
        pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\show\\', '1.png')),
        pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\show\\', 'go.png'))]

red_show = [pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\show\\', 'redmove.png')),
            pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\show\\', 'redboost.png')),
            pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\show\\', 'redwin.png'))]

blue_show = [pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\show\\', 'bluemove.png')),
            pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\show\\', 'blueboost.png')),
            pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\show\\', 'bluewin.png'))]
tie_show = pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\show\\', 'tie.png'))

team_show = [pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\show\\', 'team_0.png')),
            pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\show\\', 'team_1.png'))]

left_show = pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\', 'ResultLeft.png'))

right_show = pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\', 'ResultRight.png'))

riding_1 = pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\Rider\\', 'p1_0.png'))
riding_2 =  pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\Rider\\', 'p2_0.png'))

wheelie_1 = [pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\Wheelie\\', 'p1_'+str(i)+'.png')) for i in range(30,46) ]
wheelie_2 = [pygame.image.load(os.path.join('C:\\Users\\Administrator\\RPS\\Game\\Wheelie\\', 'p2_'+str(i)+'.png')) for i in range(30,46) ]

riding_1 = pygame.transform.scale(riding_1, (riding_1.get_width()//10, riding_1.get_height()//10))
riding_2 = pygame.transform.scale(riding_2, (riding_2.get_width()//10, riding_2.get_height()//10))
for i in range(16):
    wheelie_1[i] = pygame.transform.scale(wheelie_1[i], (wheelie_1[i].get_width()//10, wheelie_1[i].get_height()//10))
    wheelie_2[i] = pygame.transform.scale(wheelie_2[i], (wheelie_2[i].get_width()//10, wheelie_2[i].get_height()//10))


class rider(object):
    def __init__(self, x, y, width, height, image, wheelie):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = image
        self.vel = 0
        self.wheeling = False
        self.wheelcnt = 16
        self.temp = image
        self.wheelie = wheelie
    
    def draw(self, win):
        self.autorun()
        win.blit(self.temp, (self.x, self.y+motor))

    def autorun(self):
        if self.x >= 950 and self.vel > 0:
            self.vel -= 1
        self.x += self.vel

    def wheeler(self):
        if self.wheelcnt < 15:
            self.wheelcnt += 1
        else:
            self.wheelcnt = 0

class background(object):
    def __init__(self, bgImage):
        self.daytime = 0
        self.bgImage = bgImage
        self.width = self.bgImage[0].get_width()
        self.bgX = 0
        self.bgX2 = self.bgImage[0].get_width()

        self.movingSpeed = 6

    def update(self):
        self.bgX -= self.movingSpeed
        self.bgX2 -= self.movingSpeed
        if self.bgX <= -self.width:
            self.bgX = self.width
        if self.bgX2 <= -self.width:
            self.bgX2 = self.width

    def render(self):
        self.update()
        win.blit(self.bgImage[(int)(self.daytime/500)], (self.bgX, 0))
        win.blit(self.bgImage[(int)(self.daytime/500)], (self.bgX2, 0))
   
class showText(object):
    def __init__(self):
        self.time = 0
        self.img_time = 0
        self.streak1 = False
        self.streak2 = False
        self.rider1_move = False
        self.rider2_move = False
        self.tie = False
        self.team = True
        self.finish = False
        self.left = False
        self.right = False
        
    def reset(self):
        self.time = 0
        self.img_time = 0
        self.streak1 = False
        self.streak2 = False
        self.rider1_move = False
        self.rider2_move = False
        self.tie = False
        self.team = True
        self.finish = False

# Instantiate
rider_1 = rider(50, 560, 50, 50, riding_1, wheelie_1) # blue
rider_2 = rider(50, 640, 50, 50, riding_2, wheelie_2) # red
run_camera = pre.Camera()
real_background = background(bg)
show = showText()

#Setting FPS
clock = pygame.time.Clock()

#Variables
black = ( 0, 0, 0)
daytime = 0
motor = -2
running = False
space = False
cooldown = 0
streak1 = 0
streak2 = 0
speed = 0

#Font
pygame.font.init() 
myfont = pygame.font.SysFont('Comic Sans MS', 76)
textLeft_R = myfont.render("Rock", False, (0, 0, 0))
textLeft_P = myfont.render("Paper", False, (0, 0, 0))
textLeft_S = myfont.render("Scissors", False, (0, 0, 0))
textRight_R = myfont.render("Rock", False, (0, 0, 0))
textRight_P = myfont.render("Paper", False, (0, 0, 0))
textRight_S = myfont.render("Scissors", False, (0, 0, 0))

def redrawGameWindow():
    global motor, running
    real_background.render()

    rider_1.draw(win)
    if( rider_1.vel > 0 ):
        rider_1.vel-=1

    rider_2.draw(win)
    if( rider_2.vel > 0 ):
        rider_2.vel-=1

    if real_background.daytime+1 > 2500:
        real_background.daytime = 0

    real_background.daytime += 1
    if( real_background.daytime % 2 == 0 ):
        motor *= -1

    if( rider_1.x > 950 ):
        show.rider1_move = False
        show.streak1 = False
        show.finish = True    
        win.blit(blue_show[2], (300, 250))
        
    elif ( rider_2.x > 950):
        show.rider2_move = False
        show.streak2 = False
        show.finish = True
        win.blit(red_show[2], (300, 250))
        
    # 3 2 1 GO 
    if( show.time > 2 and show.time < 8):
        show.img_time += 1/25
        if( show.img_time < 4 ):
            win.blit(cntDown_show[int(show.img_time)], (520, 200))
        elif( show.img_time > 4 ):    
            show.img_time = 0
    
    if ( show.rider1_move == True ):
        show.img_time += 1/25
        if( show.img_time < 2 ):
            win.blit(blue_show[0], (450, 250))
        elif ( show.img_time > 2 ):
            show.rider1_move = False
            show.img_time = 0
    
    if ( show.streak1 == True ):
        show.img_time += 1/25
        rider_1.wheeler()
        if( show.img_time < 2 ):
            win.blit(blue_show[1], (460, 180))
            rider_1.temp = wheelie_1[int(rider_1.wheelcnt)]
        elif ( show.img_time > 2 ):
            rider_1.temp = riding_1
            show.streak1 = False
            show.img_time = 0

    if ( show.rider2_move == True ):
        show.img_time += 1/25
        if( show.img_time < 2 ):
            win.blit(red_show[0], (460, 250))
        elif ( show.img_time > 2 ):
            show.rider2_move = False
            show.img_time = 0
    
    if ( show.streak2 == True ):
        show.img_time += 1/25
        rider_2.wheeler()
        if( show.img_time < 2 ):
            win.blit(red_show[1], (460, 180))
            rider_2.temp = wheelie_2[int(rider_2.wheelcnt)]
        elif ( show.img_time > 2 ):
            rider_2.temp = riding_2
            show.streak2 = False
            show.img_time = 0

    if ( show.tie == True ):
        show.img_time += 1/25
        if( show.img_time < 2 ):
            win.blit(tie_show, (300, 150))
        elif ( show.img_time > 2 ):
            show.tie = False
            show.img_time = 0

    if show.team:
        win.blit(team_show[real_background.daytime % 2], (0, 30))
    
    if run_camera.getLeft() == "Left_scissor":
        win.blit(textLeft_S, (50, 150))
    elif run_camera.getLeft() == "Left_paper":
        win.blit(textLeft_P, (100, 150))
    elif run_camera.getLeft() == "Left_rock":
        win.blit(textLeft_R, (100, 150))
    
    if run_camera.getRight() == "Right_scissor":
        win.blit(textLeft_S, (900, 150))
    elif run_camera.getRight() == "Right_paper":
        win.blit(textLeft_P, (950, 150))
    elif run_camera.getRight() == "Right_rock":
        win.blit(textLeft_R, (950, 150))


    pygame.display.update()

run = True
while run: 
    clock.tick(0)#FPS
    run_camera.run_camera()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()

    #Wait for the input
    if show.team == False:
        if (run_camera.getToggle() == -1 and not show.finish ):
            show.time += 1/25
            if ( int(show.time) == 6):
                run_camera.setLeft("")
                run_camera.setRight("")
                run_camera.setResult("")
                run_camera.setToggle(0)
                show.left = False
                show.right = False
                show.time = 0
                
        else:
            #win condition
            run_camera.whowin()
            if keys[pygame.K_x] or run_camera.getResult() == "Left_win": # blue win
                if( rider_1.x < 950):
                    if cooldown == 0:
                        speed = 15
                        streak1 += 1
                        if( streak1 > 2 ):
                            speed = 20
                            show.streak1 = True
                            rider_1.vel += speed
                        else:
                            streak2 = 0
                            show.rider1_move = True
                            rider_1.vel += speed
                        cooldown = 30  
                run_camera.setShowL(True)
                run_camera.setShowR(True)
                run_camera.setToggle(-1)  
                
            elif keys[pygame.K_c] or run_camera.getResult() == "Right_win": # red win
                if( rider_2.x < 950):
                    if cooldown == 0:
                        speed = 15
                        streak2 += 1
                        if( streak2 > 2 ):
                            speed = 20
                            show.streak2 = True
                            rider_2.vel += speed
                        else:
                            streak1 = 0
                            show.rider2_move = True
                            rider_2.vel += speed
                        cooldown = 30
                run_camera.setShowL(True)
                run_camera.setShowR(True)  
                run_camera.setToggle(-1) 
            
            elif run_camera.getResult() == "Tie":
                show.tie = True
                run_camera.setShowL(True)
                run_camera.setShowR(True) 
                run_camera.setToggle(-1) 
        
    if cooldown > 0:
        cooldown -= 1
        
    if keys[pygame.K_s]:
        show.team = False

    if keys[pygame.K_z]:
        rider_1.x = 50
        rider_2.x = 50
        rider_1.vel = 0
        rider_2.vel = 0
        show.reset()
        run_camera.setLeft("")
        run_camera.setRight("")
        run_camera.setShowL(True)
        run_camera.setShowR(True)  
        run_camera.setToggle(-1)
    
    redrawGameWindow()    

pygame.quit()
pre.capp.release()
pre.cv2.destroyAllWindows()