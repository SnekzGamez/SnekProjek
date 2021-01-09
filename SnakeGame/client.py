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



# Use ARROW KEYS to play, SPACE BAR for pausing/resuming and Esc Key for exiting
# Function for snake game difficulty normal mode
def snakeN():
   curses.initscr()
   win = curses.newwin(20, 60, 0, 0)
   win.keypad(1)
   curses.noecho()
   curses.curs_set(0)
   win.border(0)
   win.nodelay(1)

   key = KEY_RIGHT                                                    # Initializing values
   score = 0

   snake = [[4,10], [4,9], [4,8]]                                     # Initial snake co-ordinates
   food = [10,20]                                                     # First food co-ordinates

   win.addch(food[0], food[1], 'o')                                   # Prints the food

   while key != 27:                                                   # While Esc key is not pressed
       win.border(0)
       win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score' and
       win.addstr(0, 27, ' SNAKE ')                                   # 'SNAKE' strings
       win.timeout(int(100 - (len(snake)/5 + len(snake)/10)%100))     # Increases the speed of Snake as its length increases

       prevKey = key                                                  # Previous key pressed
       event = win.getch()
       key = key if event == -1 else event


       if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
           key = -1                                                   # one (Pause/Resume)
           while key != ord(' '):
               key = win.getch()
           key = prevKey
           continue

       if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
           key = prevKey

       # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
       # This is taken care of later at [1].
       snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

       # If snake crosses the boundaries, make it enter from the other side
       if snake[0][0] == 0: snake[0][0] = 18
       if snake[0][1] == 0: snake[0][1] = 58
       if snake[0][0] == 19: snake[0][0] = 1
       if snake[0][1] == 59: snake[0][1] = 1

       # If snake runs over itself, game over
       if snake[0] in snake[1:]: break


       if snake[0] == food:                                            # When snake eats the food, snake becomes longer
           food = []
           score += 10
           while food == []:
               food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
               if food in snake: food = []
           win.addch(food[0], food[1], 'o')
       else:
           last = snake.pop()                                          # [1] If it does not eat the food, length decreases
           win.addch(last[0], last[1], ' ')
       win.addch(snake[0][0], snake[0][1], '0')

   curses.endwin()
   print("\n\t\tScore - " + str(score)) #show score of the game
   points = int(score) #change score to int
   clientSock.send(str.encode(opt)) #send option to server
   clientSock.send(str(points).encode('utf-8')) #send score to server

   #will exit system for option [n], continue game if option [y], and loop back to question if option not valid
   while True:
      cnt = input("\t\tDo you want to continue playing? [y:Yes / n: No]: ")
      if cnt == 'n':
         print("\t\tThank you! Arcade is shutting down...")
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

   key = KEY_RIGHT                                                    # Initializing values
   score = 0

   snake = [[4,10], [4,9], [4,8]]                                     # Initial snake co-ordinates
   food = [10,20]                                                     # First food co-ordinates

   win.addch(food[0], food[1], 'o')                                   # Prints the food

   while key != 27:                                                   # While Esc key is not pressed
       win.border(0)
       win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score' and
       win.addstr(0, 27, ' SNAKE ')                                   # 'SNAKE' strings
       win.timeout(int(50 - (len(snake)/5 + len(snake)/10)%50))       # Increases the speed of Snake as its length increases

       prevKey = key                                                  # Previous key pressed
       event = win.getch()
       key = key if event == -1 else event


       if key == ord(' '):                                            # If SPACE BAR is pressed, wait for another
           key = -1                                                   # one (Pause/Resume)
           while key != ord(' '):
               key = win.getch()
           key = prevKey
           continue

       if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:     # If an invalid key is pressed
           key = prevKey

       # Calculates the new coordinates of the head of the snake. NOTE: len(snake) increases.
       # This is taken care of later at [1].
       snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LEFT and -1) + (key == KEY_RIGHT and 1)])

       # Exit if snake crosses the boundaries (Uncomment to enable)
       if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: break

       # If snake runs over itself
       if snake[0] in snake[1:]: break

       if snake[0] == food:                                            # When snake eats the food
           food = []
           score += 10
           while food == []:
               food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
               if food in snake: food = []
           win.addch(food[0], food[1], 'o')
       else:
           last = snake.pop()                                          # [1] If it does not eat the food, length decreases
           win.addch(last[0], last[1], ' ')
       win.addch(snake[0][0], snake[0][1], '0')

   curses.endwin()
   print("\n\t\tScore - " + str(score)) #show latest score of snake game
   points = int(score) #change points into int
   clientSock.send(str.encode(opt)) #send option number to server
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
def show_score():
   print("\t\t******Scoreboard for Snake******\n")
   i = 1
   for x in board:
      print("\t\t\t    ",i,":",x)
      i += 1

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
   print("\t\t\t [1] NORMAL")
   print("\t\t\t [2] HARD")

while True:
   menu()
   opt = input("\n\t\t\tPick your selection: ")
   ### option 1 will ask player to choose difficulty mode (normal/hard)
   if opt == '1':
      difclty()
      difcl = input("\n\t\t\tEnter your difficulty option: ")
      if difcl == '1': #option 1 for normal mode
         snakeN()

      elif difcl == '2': #option 2 for hard mode
         snakeH()

      else:
         print("Unrecognize option!") #will output if unrecognize option entered

   ### option 2 will show all the score in the scoreboard from the highest to lowest
   elif opt == '2':
      os.system('clear')
      clientSock.send(str.encode(opt)) # send option number to server

      #receive scoreboard text file sent from server and write it into a text file name score.txt
      fname = 'score.txt'
      file = open(fname, 'wb')
      file_data = clientSock.recv(1024)
      file.write(file_data)
      file.close()
      print("\n\n")

      score = [] #initialize empty array so that score can be append in the empty array

      # open back the file that have been write and read the file
      with open('score.txt', 'r') as filehandle:
         filecontents = filehandle.readlines()
         for line in filecontents: #for loop to read one by one score in the file
            current_place = line[:-1]
            score.append(current_place) #append all the score in the text file into the empty array (score = [])

         # change the score that have been append to the array from string to integer
         for i in range(0, len(score)):
            score[i] = int(score[i])

         # sort all the score in the  array from highest to lowest
         board = sorted(score, reverse=True)
      show_score() #display the scoreboard
      input("Press Enter to continue...") #press enter to go back to menu()

   elif opt == 'q':
      clientSock.send(str.encode(opt))
      clientSock.close()
      sys.exit()

   # option to close and exit the program
   elif opt == '3':
      print("Thank you for playing! Arcade is shutting down...")
      clientSock.send(str.encode(opt))
      clientSock.close()
      sys.exit()

   # option if player enter unrecognizeable option, will loopback to menu()
   else:
      print("\n\t\tUnrecognize option")
      input("\t\tPress Enter to try again...")
