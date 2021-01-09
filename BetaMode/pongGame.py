import pygame
import sys
import random


# Initial Conditions.

white=(255,255,255)
black=(0,0,0)
green=(0,255,0)
red=(255,0,0)
blue=(0,0,255)
gray=(128,128,128)
size=[1000,600]
ball_centre_y=150
ball_centre_x=(int((random.random()*100000)%(size[0]-200)))+100
ball_radius=25
ball_direction='UP_LEFT'
ball_speed=10          # Ball speed.
hit_bar_speed=18       # Hit Bar Speed.
hit_bar_length=100
hit_bar_height=25
hit_bar_left=int(size[0]/2)-int(hit_bar_length/2)
time1=pygame.time.get_ticks()
can_accel_left=False
can_accel_right=False
game_over=False
paused_game=False
score=0






# Function to reset the game.

def reset_game() :
        global ball_centre_y
        global ball_centre_x
        global ball_direction
        global hit_bar_left
        global time1
        global can_accel_left
        global can_accel_right
        global game_over
        global paused_game
        global score
        ball_centre_y=150
        ball_centre_x=(int((random.random()*100000)%(size[0]-200)))+100
        ball_direction='UP_LEFT'
        hit_bar_left=int(size[0]/2)-int(hit_bar_length/2)
        time1=pygame.time.get_ticks()
        can_accel_left=False
        can_accel_right=False
        game_over=False
        paused_game=False
        score=0



# Function to Draw Initial Screen.

def draw_initial_screen() :
        play()
        draw_screen()
        font=pygame.font.Font(None,220)
        gameText = font.render("Nithin's", True, white)
        overText = font.render('Pong', True, white)
        over1Text = font.render('Game', True, white)
        gameRect = gameText.get_rect()
        overRect = overText.get_rect()
        over1Rect = over1Text.get_rect()
        gameRect.centerx=(size[0]/2)
        gameRect.centery=(size[1]/2)-150
        overRect.centerx=(size[0]/2)
        overRect.centery=(size[1]/2)
        over1Rect.centerx=(size[0]/2)
        over1Rect.centery=(size[1]/2+150)
        screen.blit(gameText, gameRect)
        screen.blit(overText, overRect)
        screen.blit(over1Text, over1Rect)
        print_press_any_key()
        pygame.display.update()







# Function to wait for any key press.

def wait_for_any_key() :
        while True :
                for event in pygame.event.get() :
                        if event.type==pygame.QUIT :
                                sys.exit()
                                pygame.quit()
                        if event.type == pygame.KEYDOWN :
                                return True








# Function to print Game Over.

def print_game_over() :
        font=pygame.font.Font(None,260)
        font1=pygame.font.Font(None,50)
        gameText = font.render('Game', True, white)
        overText = font.render('Over', True, white)
        sc="Your Score : "+str(score)
        scoreText = font1.render(sc, True, white)
        gameRect = gameText.get_rect()
        overRect = overText.get_rect()
        scoreRect = scoreText.get_rect()
        gameRect.centerx=(size[0]/2)
        gameRect.centery=(size[1]/2)-150
        overRect.centerx=(size[0]/2)
        overRect.centery=(size[1]/2)
        scoreRect.centerx=(size[0]/2)
        scoreRect.centery=(size[1]/2)+120
        screen.blit(gameText, gameRect)
        screen.blit(overText, overRect)
        screen.blit(scoreText, scoreRect)










# Function to print paused game.

def print_paused_game() :
        font=pygame.font.Font(None,230)
        overText = font.render('Paused', True, white)
        overRect = overText.get_rect()
        overRect.centerx=(size[0]/2)
        overRect.centery=(size[1]/2)
        screen.blit(overText, overRect)
        print_press_any_key()







# Function to print press any key.

def print_press_any_key() :
        global paused_game
        font=pygame.font.Font(None,30)
        if paused_game :
                text = font.render("Press Escape key to continue", True, gray)
        else :
                text = font.render("Press any key to continue", True, gray)
        rect = text.get_rect()
        rect.centerx=size[0]-150
        rect.centery=size[1]-50
        screen.blit(text, rect)

# Function to draw screen.

def draw_screen() :
        screen.fill(black)
        font=pygame.font.Font(None,100)
        scoreText = font.render(str(score), True, white)
        scoreRect = scoreText.get_rect()
        scoreRect.centerx=size[0]-100
        scoreRect.centery=100
        screen.blit(scoreText,scoreRect)
        pygame.draw.circle(screen,red,(ball_centre_x,ball_centre_y),ball_radius)
        pygame.draw.rect(screen,blue,(hit_bar_left,(size[1]-hit_bar_height),hit_bar_length,hit_bar_height))
        pygame.display.update()







# Main Game Play Function.

def play() :
        global hit_bar_left
        global time1
        global ball_direction
        global ball_centre_x
        global ball_centre_y
        global score
        global game_over
        if pygame.time.get_ticks() > (time1+11) :
                # Code to control movement of ball.
                if ball_direction=='UP_LEFT' :
                        if (ball_centre_x-ball_speed)>ball_radius and (ball_centre_y-ball_speed)>ball_radius :
                                ball_centre_x-=ball_speed
                                ball_centre_y-=ball_speed
                        elif (ball_centre_y-ball_speed)>ball_radius :      # Ball exceeds left side of screen.
                                ball_direction='UP_RIGHT'
                        elif (ball_centre_x-ball_speed)>ball_radius :      # Ball exceeds top of screen.
                                ball_direction='DOWN_LEFT'
                        else :                                             # Ball exceeds both left and top of screen.
                                ball_direction='DOWN_RIGHT'
                if ball_direction=='UP_RIGHT' :
                        if (ball_centre_x+ball_speed)<(size[0]-ball_radius) and (ball_centre_y-ball_speed)>ball_radius :
                                ball_centre_x+=ball_speed
                                ball_centre_y-=ball_speed
                        elif (ball_centre_y-ball_speed)>ball_radius :      # Ball exceeds right side of screen.
                                ball_direction='UP_LEFT'
                        elif (ball_centre_x+ball_speed)<(size[0]-ball_radius)  :  # Ball exceeds bottom of screen.
                                ball_direction='DOWN_RIGHT'
                        else :                                             # Ball exceeds both right side and bottom of screen.
                                ball_direction='DOWN_LEFT'
                if ball_direction=='DOWN_LEFT' :
                        if (ball_centre_x-ball_speed)>ball_radius and (ball_centre_y+ball_speed)<(size[1]-ball_radius) :
                                if (ball_centre_x+ball_radius)>=hit_bar_left and (ball_centre_x-ball_radius)<=(hit_bar_left+hit_bar_length) :
                                        if (ball_centre_y+ball_speed)<(size[1]-(ball_radius+hit_bar_height)) :
                                                ball_centre_x-=ball_speed
                                                ball_centre_y+=ball_speed
                                        else :                             # Condition of scoring.
                                                ball_direction='UP_LEFT'
                        elif  (ball_centre_y+ball_speed)<(size[1]-ball_radius) :
                                ball_direction='DOWN_RIGHT'
                        else :
                                direction='UP_RIGHT'
                if ball_direction=='DOWN_RIGHT' :
                        if (ball_centre_x+ball_speed)<(size[0]-ball_radius) and (ball_centre_y+ball_speed)<(size[1]-ball_radius) :
                                if (ball_centre_x+ball_radius)>=hit_bar_left and (ball_centre_x-ball_radius)<=(hit_bar_left+hit_bar_length) :
                                        if (ball_centre_y+ball_speed)<(size[1]-(ball_radius+hit_bar_height)) :
                                                ball_centre_x+=ball_speed
                                                ball_centre_y+=ball_speed
                                        else :                                 # Condition of scoring.
                                                ball_direction='UP_RIGHT'
                                                score+=1
                                elif ((ball_centre_x+ball_radius)<hit_bar_left or (ball_centre_x-ball_radius)>(hit_bar_left+hit_bar_length)) :
                                        if (ball_centre_y+ball_radius)>(size[1]-hit_bar_height) :      # Condition of game over.
                                                ball_centre_y=size[1]-ball_radius
                                                game_over=True
                                        else :
                                                ball_centre_x+=ball_speed
                                                ball_centre_y+=ball_speed
                                else :
                                        ball_centre_x+=ball_speed
                                        ball_centre_y+=ball_speed
                        elif (ball_centre_x+ball_speed)<(size[0]-ball_radius) :
                                ball_direction='UP_RIGHT'
                        elif  (ball_centre_y+ball_speed)<(size[1]-ball_radius) :
                                ball_direction='DOWN_LEFT'
                        else :
                                direction='UP_LEFT'
                # Code to control Hit Bar Position.

                if can_accel_left :
                        if (hit_bar_left-hit_bar_speed)>=0 :
                                hit_bar_left-=hit_bar_speed
                if can_accel_right :
                        if (hit_bar_left+hit_bar_length+hit_bar_speed)<=size[0] :
                                hit_bar_left+=hit_bar_speed

                time1=pygame.time.get_ticks()









# Initial screen.

pygame.init()
screen=pygame.display.set_mode(size,0,32)
pygame.display.set_caption("Wan Jago Game")
draw_initial_screen()
while True :
        if wait_for_any_key() :
                break

# Main game loop

while True :
        for event in pygame.event.get() :
                if event.type==pygame.QUIT :
                        if paused_game :
                                sys.exit()
                                pygame.quit()
                        game_over=True
                        print_game_over()
                        pygame.display.update()
                        time3=pygame.time.get_ticks()
                        while pygame.time.get_ticks() < (time3+1000) :
                                pygame.time.get_ticks()
                        sys.exit()
                        pygame.quit()
                if event.type == pygame.KEYDOWN :
                        if event.key == pygame.K_ESCAPE :
                                if paused_game==False :
                                        paused_game=True
                                        print_paused_game()
                                        pygame.display.update()
                                else :
                                        paused_game=False
                        if event.key == pygame.K_LEFT :
                                 can_accel_left=True
                        if event.key == pygame.K_RIGHT :
                                 can_accel_right=True
                if event.type == pygame.KEYUP :
                        if event.key == pygame.K_LEFT :
                                 can_accel_left=False
                        if event.key == pygame.K_RIGHT :
                                 can_accel_right=False
        if paused_game==False :
                play()
                draw_screen()
        if game_over :
                print_game_over()
                print_press_any_key()
                pygame.display.update()
                if wait_for_any_key() :
                        reset_game()
