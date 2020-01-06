import socket
import os

connections = []
totalConnections = 0


def newConnection(sock):
    """
    creates new connection between client and server
    :params data: socket
    """
    while True:
        print('Waiting for a connection ... ')
        clientSocket, clientAddress = sock.accept()
        print('Connected by', clientAddress)
        try:
            sock.settimeout(1)
            msg = clientSocket.recv(1024)  
            # Look for the end of the header 
            pos = msg.find(b'\r\n\r\n')

            root = os.getcwd()            
            top_dir = [dirs[0] for dirs in os.walk(root) if not '.' in dirs[0]] 

            dir_ext = search(msg[:pos])
            file_dir = top_dir[1]+'/'+ dir_ext 
            #file_dir = root+'/files'+ dir_ext

            if dir_ext == '/':
               file_dir = top_dir[1]+'/'+'index.html'
               #file_dir = file_dir +'index.html'
               do_GET(file_dir, 'r', clientSocket)  


            elif os.path.isfile(file_dir): 
                _, file_extension = os.path.splitext(file_dir)

                if file_extension == '.jpg' or file_extension == '.ico':   
                   do_GET(file_dir, 'rb', clientSocket)

                else:  
                   do_GET(file_dir, 'r', clientSocket)
           
            elif not os.path.isfile(file_dir):

               dir = top_dir[1]+'/'+ file_dir  
               #dir = os.getcwd()+'/files'+ file_dir
               if os.path.isfile(dir):

                   _, file_extension = os.path.splitext(dir)

                   if file_extension == '.jpg' or file_extension == '.ico':   
                     do_GET(file_dir, 'rb', clientSocket)

                   else:   
                     do_GET(file_dir, 'r', clientSocket)
               
               else:
                   header = 'HTTP/1.1 404 Not Found\n\n'
                   clientSocket.sendall(header.encode('utf-8'))
                   clientSocket.close()
   
        except sock.timeout as e:
             print(e)             

        finally:
            print('Closing current connection')
            clientSocket.close()


def do_GET(file_dir, mode, clientSocket):
  
    with  open(file_dir,mode) as img_file:

       if mode == 'rb':
          data = img_file.read() 
          HTTP_RESPONSE = b'\r\n'.join([
              b"HTTP/1.1 200 OK",
              b"Connection: close",
              bytes("Content-Length: %s" % len(data),'utf-8'),
              b'', data 
          ] )  
       
       if mode == 'r':
          data = img_file.read().encode('utf-8')  
          HTTP_RESPONSE = b'\r\n'.join([
              b"HTTP/1.1 200 OK",
              b"Connection: close",
              bytes("Content-Length: %s" % len(data),'utf-8'),
              b'',data
          ] )   

       clientSocket.sendall(HTTP_RESPONSE)  
       img_file.close()     



def search(data):
    """
    """
    data_ = str(data).replace("b'",'')
    splited_data = [s for s in list(''.join((data_.split('GET '))).split(' HTTP/1.1'))]
    return splited_data[0]


if __name__ == "__main__":
    #Get host and port
    host = 'localhost' 
    port = int(input("Port: "))

    #Create new server socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(1)
    newConnection(sock)
