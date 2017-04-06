"""
Le premier prgramme en Python
* utilisation des arguments de la lignne de commande
* les processus
* le logger
@author Dragos STOICA
@modifié par Ciobanu Alin
@version 0.6
@date 17.feb.2014
"""

import sys
import socket
import select
 
def chat_client():
    if(len(sys.argv) < 3) :
        print "La commande n'est pas valide. Tu as besoin d'une connectione:  python chat_client.py hostname port"
        sys.exit()

    host = sys.argv[1] #On lit la premiere commande (nom de host)
    port = int(sys.argv[2]) #On lit la deuxieme commande (nombre de port)

    #on a besoin d'un conteur pour le nombre des clients qui se connectes
    #clients_conteur = 0
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    #La connection a host
    try :
        s.connect((host, port))
        ##clients_counter = 1 on a notre premier client
    except :
        print 'Connexion impossible'
        sys.exit()
     
    
    print 'la connection a ete etabli'
    sys.stdout.write('[Moi] '); sys.stdout.flush()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        #La liste de sockets disponibles
        ready_to_read,ready_to_write,in_error = select.select(socket_list , [], [])

        for sock in ready_to_read:             
            if sock == s:
                #La data de server
                data = sock.recv(1024)
                    
                if not data :
                    print '\nDisconnected'
                    sys.exit()
                else :
                    #Afficher le message
                    sys.stdout.write(data)
                    sys.stdout.write('[Moi] '); sys.stdout.flush()     
                
            else :
                #L'utilisateur courrant a envoie un message/le programme marche
                msg = sys.stdin.readline()
                s.send(msg)
                sys.stdout.write('[Moi] '); sys.stdout.flush() 
        
if __name__ == "__main__":

    sys.exit(chat_client())