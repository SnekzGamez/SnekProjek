import socket
import sys
import time
import os
import json
import tqdm
from _thread import*
#import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created sucessfully!")

port = 8989
host = ''
threadCount = 0

try:
   s.bind((host,port))
   print("Socket successfully bind at port: " + str(port) + "\n")
except socket.error as e:
   print(str(e))

print("Waiting for client to connect..")
s.listen(5)

def threaded_client(conn):
   conn.send(("\n\t\t Dear gamers, ready to play?").encode('utf-8'))
   while True:
      #data = conn.recv(2048)
      #print(data.decode('utf-8'))
      print("Hello")
#      data = conn.recv(1024)
#      points = data.decode()
#      print("Bye")
#      score = []

#      with open('scoreboard.txt' , 'r') as filehandle:
#         for line in filehandle:
#            currentPlace = line[:-1]
#            score.append(currentPlace)

#      with open('scoreboard.txt', 'r') as filehandle:
#         filecontents = filehandle.readlines()
#         for line in filecontents:
#            current_place = line[:-1]
#            score.append(current_place)

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
         points = data.decode()
         score.append(points)
         print(score)
         print('Bye')

         with open('scoreboard.txt' , 'w') as filehandle:
            filehandle.writelines("%s\n" % place for place in score)

      elif opt == '2':
         SEPERATOR = "<SEPERATOR>"
         BUFFER_SIZE = 4096

         try:
            filename = "scoreboard.txt"
            filesize = os.path.getsize(filename)
            s.send(f"{filename}{SEPERATOR}{filesize}".encode())

            progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale = True, unit_divisor = 1024)
            with open(filename, "rb") as f:
               for _ in progress:
                  bytes_read = f.read(BUFFER_SIZE)
                  if not bytes_read:
                     break

                  s.sendall(bytes_read)
                  progress.update(len(bytes_read))

         except BrokenPipeError:
            pass


#         fname = 'scoreboard.txt'
#         file = open(fname, 'rb')
#         sendData = file.read(2048)
#         s.send(fname.encode('utf-8'))
#
#         while sendData:
#            print("Received File!\n" , s.recv(1024).decode('utf-8'))
#            s.send(sendData)
#            sendData = file.read(1024)
#         file.close()

#         sendData = json.dumps({score})
#         huhu = json.dumps({score})
#         s.send(huhu.encode())
#         for elmt in score:
#            send_str = "%s," % int(elmt)

#         while send_str:
#            chars_sent = s.send(send_str.encode())
#            send_str = send_str[chars_sent:]

      else:
         break

#      with open('scoreboard.txt', 'w') as filehandle:
#         for listitem in points:
#            filehandle.write('%s\n' % listitem)

#      with open('scoreboard.txt' , 'w') as filehandle:
#         filehandle.writelines("%s\n" % place for place in score)

#      if not data:
#         break
#   conn.close()
      #if not data:
      #   break
      #conn.sendall(str.encode(response))
   #conn.close()


while True:
   client, addr = s.accept()
   print("Connected to: " + addr[0] + ':' + str(addr[1]))
   start_new_thread(threaded_client, (client, ))
   threadCount += 1
   print('Number of Client Connected to Server: ' + str (threadCount))
s.close()
