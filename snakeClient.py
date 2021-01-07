import socket
import curses
import sys
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '172.20.10.6'
port = 8989

print("Waiting for connection...")
print("Connecting with server {host}:{port} \n")
try:
   clientSock.connect((host,port))
   print("Connection to server successful!\n")
except socket.error as e:
   print(str(e))

msg = clientSock.recv(1024)
print(msg.decode('utf-8'))

#msg2 = "Player already connected and ready to play!\n"
#clientSock.send(msg2.encode())

#print("[1] Play game\n")
#print("[2] See Scoreboard\n")

#opt = input("Pick your selection: ")
#if opt == '1':
#   snake()
#else:
#   print("Unrecognize option")

# SNAKES GAME
# Use ARROW KEYS to play, SPACE BAR for pausing/resuming and Esc Key for exiting
def snake():
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

   win.addch(food[0], food[1], '*')                                   # Prints the food

   while key != 27:                                                   # While Esc key is not pressed
       win.border(0)
       win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score' and
       win.addstr(0, 27, ' SNAKE ')                                   # 'SNAKE' strings
       win.timeout(int(100 - (len(snake)/5 + len(snake)/10)%100))     # Increases the speed of Snake as its length i>

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
       snake.insert(0, [snake[0][0] + (key == KEY_DOWN and 1) + (key == KEY_UP and -1), snake[0][1] + (key == KEY_LE>

       # If snake crosses the boundaries, make it enter from the other side
       if snake[0][0] == 0: snake[0][0] = 18
       if snake[0][1] == 0: snake[0][1] = 58
       if snake[0][0] == 19: snake[0][0] = 1
       if snake[0][1] == 59: snake[0][1] = 1

       # Exit if snake crosses the boundaries (Uncomment to enable)
       #if snake[0][0] == 0 or snake[0][0] == 19 or snake[0][1] == 0 or snake[0][1] == 59: break

       # If snake runs over itself
       if snake[0] in snake[1:]: break


       if snake[0] == food:                                            # When snake eats the food
           food = []
           score += 1
           while food == []:
               food = [randint(1, 18), randint(1, 58)]                 # Calculating next food's coordinates
               if food in snake: food = []
           win.addch(food[0], food[1], '*')
       else:
           last = snake.pop()                                          # [1] If it does not eat the food, length dec>
           win.addch(last[0], last[1], ' ')
       win.addch(snake[0][0], snake[0][1], '#')

   curses.endwin()
   print("\nScore - " + str(score))
   points = str(score)
   print("Points: " + points)
   clientSock.send(str.encode(opt))
   clientSock.send(points.encode())
   print("http://bitemelater.in\n")


while True:
   print("[1] Play game\n")
   print("[2] See Scoreboard\n")

   opt = input("Pick your selection: ")
   if opt == '1':
      snake()
#      clientSock.send(str.encode(opt))

   elif opt == '2':
      clientSock.send(str.encode(opt))
      BUFFER_SIZE = 4096
      SEPERATOR = "<SEPERATOR>"

      received = clientSock.recv(BUFFER_SIZE).decode()
      filename, filesize = received.split(SEPERATOR)
      filename = os.path.basename(filename)
      filesize = int(filesize)

      progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit = "B", unit_scale = True, unit_divisor = 1>
      with open(filename, "wb") as f:
         for _ in progress:
            bytes_read = clientSock.recv(BUFFER_SIZE)
            if not bytes_read:
               break

            f.write(bytes_read)
            progress.update(len(bytes_read))
         print("Successful")

#      dataS = clientSock.recv(1024)
#      dataS = dataS.decode('utf-8')
#      dataJ = json.loads(dataS)
#      print(type(dataJ))
#      print(dataJ)
#      score = []
#      score.append(dataS)
#      print(dataS)

#      fname = clientSock.recv(1024)
#      file = open(fname, 'wb')


#      msg = 'hello'
#      clientSock.send(msg.encode('utf-8'))

#      recvData = clientSock.recv(1024)
#      while recvData:
#         file.write(recvData)
#         recvData = clientSock.recv(1024)

#      file.close()

#      if not fname:
#         break

   elif opt == 'q':
      clientSock.close()
      sys.exit()
   else:
      print("Unrecognize option")
