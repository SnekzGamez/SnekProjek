import socket
import sys
import time
import os
import json
import tqdm
from _thread import*

os.system('clear') #to clear screen
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating socket
print("\t\t[+]Socket created sucessfully!")

port = 8989
host = ''
threadCount = 0

#connecting to server
try:
   s.bind((host,port))
   print("\n\t\t[+]Socket successfully bind at port: " + str(port) + "\n")
except socket.error as e:
   print(str(e))

print("\t\t>> Waiting for player to connect..")
s.listen(5)


# function execute everytime it received  option number from client
def threaded_client(conn):
   conn.send(("\n\t\t Dear gamers, ready to play?").encode('utf-8')) #send opening message to client
   while True:


      dataO = conn.recv(1024)
      opt = str(dataO.decode()) #received option number from client
      if opt == '1':
         dataH = conn.recv(1024)
         optH = str(dataH.decode())



         if optH == 'a': #normal difficulty
            score = [] #initialize empty array so that new score from text file can be append in score = []

            # will read score gather from client in the textfile (scoreboard.txt)
            with open('scoreboardN.txt', 'r') as filehandle:
               filecontents = filehandle.readlines()
               for line in filecontents: #loop to read every single line of the points in the text file
                  current_place = line[:-1]
                  score.append(current_place) #append the score in score = []

            data = conn.recv(1024)
            points = data.decode('utf-8') #receive the points from clients and decode it

            scor = int(points) #convert the point received from client from string to integer
            score.append(scor) #append the points that have been converted to integer into score = []

            # convert all points in the array from string to integer
            for i in range(0, len(score)):
               score[i] = int(score[i])

            board = [] #initialize new array to append the new points that have been converted to integer into board = []

            # will check and loop and ignore any integer that have the same number in the array board = [] so that there will have no duplicate points in the array 
            for i in score:
               if i not in board:
                  board.append(i)

            print("\t\tScoreboard for Normal Difficulty: ",board) #print all the points in the board array


            # will overwrite the new score receive from client into the scoreboard.txt
            with open('scoreboardN.txt' , 'w') as filehandle:
               filehandle.writelines("%s\n" % place for place in board)





         elif optH == 'b': # hard difficulty
            score = [] #initialize empty array so that new score from text file can be append in score = []

            # will read score gather from client in the textfile (scoreboard.txt)
            with open('scoreboardH.txt', 'r') as filehandle:
               filecontents = filehandle.readlines()
               for line in filecontents: #loop to read every single line of the points in the text file
                  current_place = line[:-1]
                  score.append(current_place) #append the score in score = []

            data = conn.recv(1024)
            points = data.decode('utf-8') #receive the points from clients and decode it

            scor = int(points) #convert the point received from client from string to integer
            score.append(scor) #append the points that have been converted to integer into score = []

            # convert all points in the array from string to integer
            for i in range(0, len(score)):
               score[i] = int(score[i])

            board = [] #initialize new array to append the new points that have been converted to integer into board>

            # will check and loop and ignore any integer that have the same number in the array board = [] so that t>
            for i in score:
               if i not in board:
                  board.append(i)

            print("\t\tScoreboard for Normal Difficulty: ",board) #print all the points in the board array


            # will overwrite the new score receive from client into the scoreboard.txt
            with open('scoreboardH.txt' , 'w') as filehandle:
               filehandle.writelines("%s\n" % place for place in board)




      elif opt == '2': # view scoreboard
         dataD = conn.recv(1024)
         optD = str(dataD.decode())
         if optD == '1':
            fname = 'scoreboardN.txt'
            file = open(fname, 'rb')
            file_data = file.read(1024) # will read the score in the text and save it in file_ data
            conn.send(file_data) # send the file_data file to client so that client can view the scoreboard
            print("\t\tFile has been sent!")

         elif optD == '2':
            fname = 'scoreboardH.txt'
            file = open(fname, 'rb')
            file_data = file.read(1024) # will read the score in the text and save it in file_ data
            conn.send(file_data) # send the file_data file to client so that client can view the scoreboard
            print("\t\tFile has been sent!")

   conn.close()


# threading method so that many client can connect to the server
while True:
   client, addr = s.accept()
   print("\n\t\tConnected to: " + addr[0] + ':' + str(addr[1]))
   start_new_thread(threaded_client, (client, ))
   threadCount += 1
   print('\t\tNumber of Players that have been Connected to Server: ' + str (threadCount))
s.close()
