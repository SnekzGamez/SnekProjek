import socket
import sys
import time
import os
import json
import tqdm
from _thread import*

os.system('clear')
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("\t\t[+]Socket created sucessfully!")

port = 8989
host = ''
threadCount = 0

try:
   s.bind((host,port))
   print("\n\t\t[+]Socket successfully bind at port: " + str(port) + "\n")
except socket.error as e:
   print(str(e))

print("\t\t>> Waiting for player to connect..")
s.listen(5)

def threaded_client(conn):
   conn.send(("\n\t\t Dear gamers, ready to play?").encode('utf-8'))
   while True:
#      print("Hello")

      dataO = conn.recv(1024)
      opt = str(dataO.decode())
      if opt == '1':

         score = []
         with open('scoreboard.txt', 'r') as filehandle:
            filecontents = filehandle.readlines()
            for line in filecontents:
               current_place = line[:-1]
               score.append(current_place)

         data = conn.recv(1024)
         points = data.decode('utf-8')

         scor = int(points)
         score.append(scor)

         for i in range(0, len(score)):
            score[i] = int (score[i])

         board = []
         for i in score:
            if i not in board:
               board.append(i)

         print("\t\tScoreboard: ",board)
#         print('Bye')

         with open('scoreboard.txt' , 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in board)

      elif opt == '2':
         fname = 'scoreboard.txt'
         file = open(fname, 'rb')
         file_data = file.read(1024)
         conn.send(file_data)
         print("File has been sent!")

      elif opt == 'q':
         print("bye")
         break

   conn.close()
   s.close
   sys.exit()
   sys.exit()

#      else:
#         break


while True:
   client, addr = s.accept()
   print("\n\t\tConnected to: " + addr[0] + ':' + str(addr[1]))
   start_new_thread(threaded_client, (client, ))
   threadCount += 1
   print('\t\tNumber of Players that have been Connected to Server: ' + str (threadCount))
s.close()
