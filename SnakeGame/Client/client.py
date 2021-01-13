import socket
import curses
import sys
import os
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
host = '172.20.10.6' #server host
port = 8989 #port that will be use

print("Waiting for connection...")
print("Connecting with server {host}:{port} \n")

try:
   clientSock.connect((host,port))
   print("Connection to server successful!\n")
except socket.error as e:
   print(str(e))

msg = clientSock.recv(1024) #receive opening message from server
print(msg.decode('utf-8'))  #decode the message

# snake ascii in menu
def ascii():
   print("\n\n")
   print("\t\t\t    Y")
   print("\t\t\t  .-^-.")
   print("\t\t\t /     \      .- ~ ~ -.")
   print("\t\t\t()     ()    /   _ _   `.                     _ _ _")
   print("\t\t\t \_   _/    /  /     \   \                . ~  _ _  ~ .")
   print("\t\t\t   | |     /  /       \   \             .' .~       ~-. `.")
   print("\t\t\t   | |    /  /         )   )           /  /             `.`.")
   print("\t\t\t   \ \_ _/  /         /   /           /  /                `'")
   print("\t\t\t    \_ _ _.'         /   /           (  (")
   print("\t\t\t                    /   /             \  \ ")
   print("\t\t\t                   /   /               \  \ ")
   print("\t\t\t                  /   /                 )  )")
   print("\t\t\t                 (   (                 /  /")
   print("\t\t\t                  `.  `.             .'  /")
   print("\t\t\t                    `.   ~ - - - - ~   .'")
   print("\t\t\t                       ~ . _ _ _ _ . ~")



# Using import curses package to move snake with arrow keys, pause with space bar and exit using esc button
# Function for snake game difficulty normal mode
def snakeN():
   curses.initscr()
   win = curses.newwin(20, 60, 0, 0)
   win.keypad(1)
   curses.noecho()
   curses.curs_set(0)
   win.border(0)
   win.nodelay(1)

   btn = KEY_RIGHT                                                    # initialize btn as value
   score = 0

   snek = [[4,10], [4,9], [4,8]]                                     # Initialize the snake coordinates
   food = [10,20]                                                     # for the first snake food coordinate

   win.addch(food[0], food[1], 'o')                                   # printing 'o' as the food of the snake

   while btn != 27:                                                   # while esc button did not press
       win.border(0)
       win.addstr(0, 2, 'SCORE : ' + str(score) + ' ')                # will output score at the top
       win.addstr(0, 27, ' SNAKE GAME ')                              # will output SNAKE at the top
       win.timeout(int(100 - (len(snek)/5 + len(snek)/10)%100))     # speed is normal kept at 100

       prevBtn = btn                                                  # Previous button pressed
       event = win.getch()
       btn = btn if event == -1 else event


       if btn == ord(' '):                                            # will pause if space bar is press
           btn = -1                                                   # press space bar again to resume
           while btn != ord(' '):
               btn = win.getch()
           btn = prevBtn
           continue

       if btn not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # if unrecognize input is press
           btn = prevBtn

       # if lenght of the snake increase, it will calculate the next coordinate for the snake head
       # This is taken care of later at [1].
       snek.insert(0, [snek[0][0] + (btn == KEY_DOWN and 1) + (btn == KEY_UP and -1), snek[0][1] + (btn == KEY_LEFT and -1) + (btn == KEY_RIGHT and 1)])

       # In normal mode, snake can cross the border and appear at the other side of the border
       if snek[0][0] == 0: snek[0][0] = 18
       if snek[0][1] == 0: snek[0][1] = 58
       if snek[0][0] == 19: snek[0][0] = 1
       if snek[0][1] == 59: snek[0][1] = 1

       # game will break if snake run over itself
       if snek[0] in snek[1:]: break


       if snek[0] == food:                                            # snake will become longer as it eats food
           food = []
           score += 10
           while food == []:
               food = [randint(1, 18), randint(1, 58)]                 # output the next coordinate of the snake food
               if food in snek: food = []
           win.addch(food[0], food[1], 'o')
       else:
           last = snek.pop()                                          # [1] if snake does not eat, length will not increase
           win.addch(last[0], last[1], ' ')
       win.addch(snek[0][0], snek[0][1], '0')

   curses.endwin()
   print("\n\t\tScore - " + str(score)) #show score of the game
   points = int(score) #change score to int
   clientSock.send(str(points).encode('utf-8')) #send score to server

   #will exit system for option [n], continue game if option [y], and loop back to question if option not valid
   while True:
      cnt = input("\t\tDo you want to continue playing? [y:Yes / n: No]: ")
      if cnt == 'n':
         print("\t\tThank you for playing! Arcade is shutting down...")
         sys.exit()
      elif cnt == 'y':
         menu()
         break
      else:
         print("Option is not valid! Please try again!")

# function for snake game difficulty hard mode
def snakeH():
   curses.initscr()
   win = curses.newwin(20, 60, 0, 0)
   win.keypad(1)
   curses.noecho()
   curses.curs_set(0)
   win.border(0)
   win.nodelay(1)

   btn = KEY_RIGHT                                                    # Initialize btn as value
   score = 0

   snek = [[4,10], [4,9], [4,8]]                                     # Initilize the snake coordinates
   food = [10,20]                                                     # for the first snake food coordinate

   win.addch(food[0], food[1], 'o')                                   # Printing 'o' as the food of the snake

   while btn != 27:                                                   # while esc button did not press
       win.border(0)
       win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # will output score at the top
       win.addstr(0, 27, ' SNAKE ')                                   # will output SNAKE at the top
       win.timeout(int(50 - (len(snek)/5 + len(snek)/10)%50))       # speed increase for hard mode kept at 50

       prevBtn = btn                                                  # Previous key pressed
       event = win.getch()
       btn = btn if event == -1 else event


       if btn == ord(' '):                                            # will pause if space bar is press
           btn = -1                                                   # press space bar again to resume
           while btn != ord(' '):
               btn = win.getch()
           btn = prevBtn
           continue

       if btn not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If unrecognize input is press
           key = prevKey

       # if length of the snake increase, it will calculate the next coordinate for the snake head
       # This is taken care of later at [1].
       snek.insert(0, [snek[0][0] + (btn == KEY_DOWN and 1) + (btn == KEY_UP and -1), snek[0][1] + (btn == KEY_LEFT and -1) + (btn == KEY_RIGHT and 1)])

       # in hard mode snake cannot pass through border or it will break
       if snek[0][0] == 0 or snek[0][0] == 19 or snek[0][1] == 0 or snek[0][1] == 59: break

       # game will break if snake run over itself
       if snek[0] in snek[1:]: break

       if snek[0] == food:                                            # snake will become longer as it eats the food
           food = []
           score += 10
           while food == []:
               food = [randint(1, 18), randint(1, 58)]                 # output the next coordinate of the snake food
               if food in snek: food = []
           win.addch(food[0], food[1], 'o')
       else:
           last = snek.pop()                                          # [1] if snake does not eat, length will not increase
           win.addch(last[0], last[1], ' ')
       win.addch(snek[0][0], snek[0][1], '0')

   curses.endwin()
   print("\n\t\tScore - " + str(score)) #show latest score of snake game
   points = int(score) #change points into int
   #clientSock.send(str.encode(opt)) #send option number to server
   clientSock.send(str(points).encode('utf-8')) #send points to server

   #will exit system for option [n], continue game if option [y], and loop back to question if option not valid
   while True:
      cnt = input("\t\tDo you want to continue playing? [y:Yes / n: No]: ")
      if cnt == 'n':
         print("\t\tThank you for playing! Arcade is shutting down...")
         sys.exit()
      elif cnt == 'y':
         menu()
         break
      else:
         print("Option is not valid! Please try again!")





# function to show all score that have been kept in text
def show_scoreN(board):

   os.system('clear')
   ascii()
   print("\n\n\t\t\t\t******SCOREBOARD SNEKGAMEZ ARCADE (NORMAL)******\n")
   i = 1
   for x in board:
      print("\t\t\t\t\t        ",i,":",x        )
      i += 1
      print("\t\t\t\t_______________________________________")
      if i == 11:
         break


# function to show all score that have been kept in text
def show_scoreH(board):

   os.system('clear')
   ascii()
   print("\n\n\t\t\t\t******SCOREBOARD SNEKGAMEZ ARCADE (HARD)******\n")
   i = 1
   for x in board:
      print("\t\t\t\t\t        ",i,":",x        )
      i += 1
      print("\t\t\t\t_______________________________________")
      if i == 11:
         break





# main menu
def menu():
   os.system('clear')
   ascii()
   print("\n\n\t\t**********************WELCOME TO SNEKGAMEZ ARCADE**************************")

   print("\t\t\t[1] PLAY SNAKE GAME")
   print("\t\t\t[2] VIEW SCOREBOARD")
   print("\t\t\t[3] QUIT GAME")

   print("\t\t***************************************************************************")





# players can choos difficulty mode
def difclty():
   print("\n\t\t\tDIFFICULTY OPTION")
   print("\t\t\t [a] NORMAL")
   print("\t\t\t [b] HARD")





#### MAIN ####

while True:
   menu()
   opt = input("\n\t\t\tPick your selection: ")
   ### option 1 will ask player to choose difficulty mode (normal/hard)
   if opt == '1':
      clientSock.send(str.encode(opt))
      difclty()
      difcl = input("\n\t\t\tEnter your difficulty option: ")
      if difcl == 'a': #option 1 for normal mode
         clientSock.send(str.encode(difcl))
         snakeN()

      elif difcl == 'b': #option 2 for hard mode
         clientSock.send(str.encode(difcl))
         snakeH()

      else:
         print("\t\t\tUnrecognize option!") #will output if unrecognize option entered
         input("\t\t\tPress Enter to continue...")

   ### option 2 will show all the score in the scoreboard from the highest to lowest
   elif opt == '2':
      clientSock.send(str.encode(opt))
      opt2 = input("\t\t\tChoose Scoreboard option - [1:Normal | 2: Hard]: ")
      clientSock.send(str.encode(opt2)) # send option number to server

      if opt2 == '1':

      #receive scoreboard text file sent from server and write it into a text file name score.txt
         fname = 'scoreN.txt'
         file = open(fname, 'wb')
         file_data = clientSock.recv(1024)
         file.write(file_data)
         file.close()
         print("\n\n")

         score = [] #initialize empty array so that score can be append in the empty array

         # open back the file that have been write and read the file
         with open('scoreN.txt', 'r') as filehandle:
            filecontents = filehandle.readlines()
            for line in filecontents: #for loop to read one by one score in the file
               current_place = line[:-1]
               score.append(current_place) #append all the score in the text file into the empty array (score = [])

            # change the score that have been append to the array from string to integer
            for i in range(0, len(score)):
               score[i] = int(score[i])

            # sort all the score in the  array from highest to lowest
            board = sorted(score, reverse=True)
         show_scoreN(board) #display the scoreboard
         input("\t\t\tPress Enter to continue...") #press enter to go back to menu()

      elif opt2 == '2':
         fname = 'scoreH.txt'
         file = open(fname, 'wb')
         file_data = clientSock.recv(1024)
         file.write(file_data)
         file.close()
         print("\n\n")

         score = [] #initialize empty array so that score can be append in the empty array

         # open back the file that have been write and read the file
         with open('scoreH.txt', 'r') as filehandle:
            filecontents = filehandle.readlines()
            for line in filecontents: #for loop to read one by one score in the file
               current_place = line[:-1]
               score.append(current_place) #append all the score in the text file into the empty array (score = [])

            # change the score that have been append to the array from string to integer
            for i in range(0, len(score)):
               score[i] = int(score[i])

            # sort all the score in the  array from highest to lowest
            board = sorted(score, reverse=True)
         show_scoreH(board) #display the scoreboard
         input("\t\t\tPress Enter to continue...") #press enter to go back to menu()

      else:
         print("\t\t\tInvalid input! Please try again")
         input("\t\t\tPress Enter to continue...")


   # option to close and exit the program
   elif opt == '3':
      print("\t\t\tThank you for playing! Arcade is shutting down...")
      clientSock.send(str.encode(opt))
      clientSock.close()
      sys.exit()

   # option if player enter unrecognizeable option, will loopback to menu()
   else:
      print("\n\t\tInvalid input")
      input("\t\tPress Enter to try again...")
