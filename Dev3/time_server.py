import sys
import socket
import select
import time

HOST = '' 
SOCKET_LIST = []
RECV_BUFFER = 1024 
PORT = 6666

def chat_server():

    #Le server est cree / j'ai regarde quelques tutorials sur youtube
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))

    #j'ai choisi un maximum de 3 personnes, les autres doivent attendre
    server_socket.listen(3)
 

    SOCKET_LIST.append(server_socket)
 
    currentTime = time.ctime(time.time()) + "\r\n"
    print "chat client-server a commence au port  " + str(PORT) + "\nDate et heure: " + currentTime 
 
    while 1:

        # On choisi la liste disponible
        ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
        
        for sock in ready_to_read:
            
            #on accepte une nouveau connection
            if sock == server_socket: 
                sockfd, addr = server_socket.accept()
                SOCKET_LIST.append(sockfd)
                print "Le client (%s, %s) a ete conecte" % addr + "\nDate et heure: " + currentTime
                 
                broadcast(server_socket, sockfd, "[%s:%s]  logged in" % addr)
             
            else:
                
                #le server utilise le data des clients
                try:
                    
                    #<1024kb
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        
                        #il y a des information dans le soket
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                    else:
                        
                        #on jete le soket qui n'est pas utilise   
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        #s'il n'y a plus de data, nous interrompons la connection et on envoie un message aux autres
                        broadcast(server_socket, sock, " Le client (%s, %s) a ete deconecte" % addr) 

                except:
                    broadcast(server_socket, sock, "Le client (%s, %s) a ete deconecte" % addr)
                    continue

    server_socket.close()
    
#On voie le message
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        
      
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                
                socket.close()
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(chat_server())
