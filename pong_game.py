import pygame 
from pygame.locals import * # import everything we need for this game 

pygame.init() # initialize pygame

# set up the window
screen_width = 600
screen_height = 500 

fpsClock=pygame.time.Clock() #create a clock object


#to create a display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Ping Pong Game')

#Define font 
font = pygame.font.SysFont('Constantia', 30)
#Define game variables
live_ball=False 
margin=50
cpu_score=0
player_score=0
fps=60
winner=0
speed_increase = 0


#Define Colors 
bg=(50,25,50)
white=(255,255,255)

def draw_board():
    screen.fill(bg)
    pygame.draw.line(screen,white,(0,margin),(screen_width,margin),5)

def draw_text(text,font,color,x,y):#x and y is the position of the text
    img=font.render(text,True,color) #render the text #turn that text into an image 
    screen.blit(img,(x,y)) #draw the image on the screen 

class paddle():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.rect=Rect(self.x,self.y,20,100)
        self.speed=5 
    def move(self):
        key=pygame.key.get_pressed() #get the key that is pressed
        if key[pygame.K_UP] and self.rect.top>margin: #if the key is up and the top of the paddle is greater than the margin
            self.rect.move_ip(0,-self.speed) #move the paddle up
        if key[pygame.K_DOWN] and self.rect.bottom<screen_height: #if the key is down and the bottom of the paddle is less than the screen height
            self.rect.move_ip(0,self.speed) #move the paddle down
    def ai(self):
        #ai to move the paddle automatically
        #move down 
        if self.rect.centery < pong.rect.top and self.rect.bottom<screen_height: #if the center of the paddle is less than the top of the ball and the bottom of the paddle is less than the screen height
            self.rect.move_ip(0,self.speed) #move in place to the center of the paddle
        #move up
        if self.rect.centery > pong.rect.bottom and self.rect.top>margin: #if the center of the paddle is greater than the bottom of the ball and the top of the paddle is greater than the margin
            self.rect.move_ip(0,-1*self.speed) #move in place to the center of the paddle in a negative direction
    def draw(self): #to show the paddles 
        pygame.draw.rect(screen,white,self.rect)

class ball():
    def __init__(self,x,y):
        self.reset(x,y)
        
    def move(self):
        #add collision detection 
        #check collision with top margin 
        if self.rect.top<margin: #if the top of the ball is less than the margin #speed_y is negative so it will go up
            self.speed_y*=-1 #reverse the direction of the ball
        if self.rect.bottom>screen_height: #if the bottom of the ball is less than the margin #speed_y is positive so it will go down
            self.speed_y*=-1 #reverse the direction of the ball
        #check collision with paddles
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle): #if the ball collides with the player or cpu paddle
            self.speed_x*=-1 #reverse the direction of the ball
        #check for out of the bounds 
        if self.rect.left<0: #if the ball goes out of the left side of the screen
            self.winner=1 #the player has won
        if self.rect.right>screen_width: #if the ball goes out of the right side of the screen
            self.winner=-1 #the cpu has won

        #update the position of the ball
        self.rect.x+=self.speed_x
        self.rect.y+=self.speed_y
        #check if the ball has hit the top or bottom of the screen

        return self.winner

    def draw(self):
        pygame.draw.circle(screen,white,(self.rect.x +self.ball_rad,self.rect.y+self.ball_rad),self.ball_rad) #draw the ball

    def reset(self,x,y): #to reset the ball #to set the ball to orginal values
        self.x=x
        self.y=y
        self.ball_rad=8
        self.rect=Rect(self.x,self.y,self.ball_rad*2,self.ball_rad*2) #create a rectangle around the ball
        self.speed_x=-4 #speed of the ball in the x direction
        self.speed_y=4 #speed of the ball in the y direction
        self.winner=0 #0 if no one has won yet, 1 if the player has won, -1 if the cpu has won

#create a paddle object
player_paddle=paddle(screen_width-40,screen_height//2) #not going to get a decimal)
cpu_paddle=paddle(20,screen_height//2)

#create a ball object
pong=ball(screen_width-60,screen_height//2 +50)


run = True
while run:
    fpsClock.tick(fps) #limit how quickly the the paddle runs 
    draw_board()
    draw_text('CPU:' + str(cpu_score),font,white,20,15)
    draw_text('P1:' + str(player_score),font,white,screen_width-100,15)
    draw_text('BALL SPEED: ' + str(abs(pong.speed_x)),font,white,screen_width//2-100,15) #abs is absolute value #to get the absolute value of the speed of the ball

    #draw paddle 
    player_paddle.draw() #draw the player paddle
    cpu_paddle.draw() #draw the cpu paddle

    if live_ball ==True:
        speed_increase += 1 #increase the speed of the ball
        winner=pong.move() #move the ball
        if winner == 0: #if no one has won yet, continue the game
            #move paddle
            player_paddle.move() #move the player paddle
            cpu_paddle.ai() #move the cpu paddle
            #draw ball
            pong.draw()
        else:
            live_ball=False
            if winner==1:
                player_score+=1
            elif winner == -1:
                cpu_score+=1

    #print player instructions
    if live_ball==False: #if the ball is not live
        if winner ==0:
            draw_text('CLICK ANYWHERE TO START',font,white,100,screen_height//2-100)
        if winner ==1:
            draw_text('YOU SCORED!',font,white,220,screen_height//2-100)
            draw_text('CLICK ANYWHERE TO START',font,white,100,screen_height//2-50)
        if winner ==-1:
            draw_text('CPU SCORED!',font,white,200,screen_height//2-100)
            draw_text('CLICK ANYWHERE TO START',font,white,100,screen_height//2-50)

    for event in pygame.event.get(): #get every event from pygame 
        if event.type == pygame.QUIT: #when click on the close button
            run = False #stop the game
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball==False: #when click on the down button and the ball is not live
            live_ball=True #the ball is live
            pong.reset(screen_width-60,screen_height//2+50)
    
    if speed_increase > 500:
        speed_increase = 0
        if pong.speed_x < 0:
            pong.speed_x -= 1 #decrease the speed of the ball
        if pong.speed_x > 0:
            pong.speed_x += 1#increase the speed of the ball
        if pong.speed_y < 0:
            pong.speed_y -= 1
        if pong.speed_y > 0:
            pong.speed_y += 1

    pygame.display.update() #always update the display

pygame.quit()
