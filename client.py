import ssl
import socket
import sys
import threading
import json
import base64
import time
import string
from random import *
import os
import subprocess
import readline 
import rlcompleter 
import atexit 

readline.parse_and_bind('tab: complete') 
histfile = os.path.join(os.environ['HOME'], '.pythonhistory') 
try: 
    readline.read_history_file(histfile) 
except IOError: 
    pass 

atexit.register(readline.write_history_file, histfile) 


if not os.path.exists("temp"):
    os.makedirs("temp")
allchar = string.ascii_letters + string.digits

messages = {}

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_NONE
RECV_BUFFER_SIZE=1024
fn = [True,]


def get_local_ip():
    """Return my local ip if nat otherwise ipv4."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com", 80))
        ip = (s.getsockname()[0])
        s.close()
        return ip
    except:
        return None



def logo():
    print"   ______                 ____                          ______                                           "
    print" .~      ~.  |`````````, |            |..          |  .~      ~. |         |       .'.       `````|````` "
    print"|          | |'''''''''  |______      |  ``..      | |           |_________|     .''```.          |      "
    print"|          | |           |            |      ``..  | |           |         |   .'       `.        |      "
    print" `.______.'  |           |___________ |          ``|  `.______.' |         | .'           `.      |      "
    print"                                                                                                         "   
    print"                               Secure      Private      Intelligent                  "
    print"\033[1;32m                                        "+get_local_ip()+":"+sys.argv[1]+"\033[1,22m"
    print 
    rdy = raw_input("  Press any button")


logo()


def send_message(ip,port,message,context):
    ssock = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=ip)
    server_address = (ip, int(port))
    ssock.connect(server_address)
    message = {"ip":get_local_ip(),"port":str(sys.argv[1]),"type":"M","message":message}
    message_str = json.dumps(message)
    ssock.sendall(str(message_str))


def send_frame(ip,port,message,file,context):
    ssock = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=ip)
    server_address = (ip, int(port))
    ssock.connect(server_address)
    message = {"ip":get_local_ip(),"port":str(sys.argv[1]),"type":"F","message":message,"name":file}
    message_str = json.dumps(message)
    ssock.sendall(str(message_str))


def send_file(ip,port,file,context):
    name = "".join(choice(allchar) for x in range(15))
    f = open(file)
    l=f.read(650)
    while(l):
        send_frame(ip,port,base64.b64encode(l),name+file,context)
        l = f.read(650)
     
def handle_message(connstream):
    
    data = json.loads(connstream.recv(RECV_BUFFER_SIZE))
    if(data['type']=='F'):
        try:
            if not({"type":"F","MESSAGE":"temp/"+data['name']} in messages[data['ip'],data['port']]):
                messages[data['ip'],data['port']].append({"type":"F","MESSAGE":"temp/"+data['name']})
        except:
                messages[data['ip'],data['port']]=[{"type":"F","MESSAGE":"temp/"+data['name']}]

        new_data = base64.b64decode(data['message'])
        with open("temp/"+data['name'], 'a') as f:
            f.write(new_data)
    else:
        try:
            messages[data['ip'],data['port']].append({"type":"M","MESSAGE":data['message']})
        except:
            messages[data['ip'],data['port']]= [{"type":"M","MESSAGE":data['message']}]



def response(port,pp):
    data = ''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', int(port))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(server_address)
    sock.listen(25)

    while pp[0] is True:
        newsocket, fromaddr = sock.accept()
        connstream = ssl.wrap_socket(newsocket,
                                server_side = True,
                                certfile = "cert.pem",
                                keyfile = "key.pem",
                                ssl_version = ssl.PROTOCOL_SSLv23)

        temp =threading.Thread(target=handle_message, args=(connstream,))
        temp.start()


t =threading.Thread(target=response, args=(int(sys.argv[1]),fn,))
t.start()



while True:
    try:
        subprocess.Popen(["clear"])

        print"\033[1;32m                                        "+get_local_ip()+":"+sys.argv[1]+"\033[1,22m"

        input = raw_input("\033[1;32mCommand: \033[1,22m")
        print ("\033[1,0m")
        input = input.split("::")
        if (input[0] == "inbox"):
            if (input[1] == "list"):
                if len(messages)==0:
                    print "     empty"
                for i in messages:
                    print "     "+i[0]+":"+i[1]+"  ["+str(len(messages[i[0],i[1]]))+"]"
                print 
                rdy_ = raw_input("Ready?")
            else:
                input = input[1]
                input = input.split(":")
                ip = input[0]
                port = input[1]
                for i in messages[ip,port]:
                    if(i['type']=='M'):
                        print "     "+i['MESSAGE']
                        print
                    else:
                        file_type = i['MESSAGE'].split('.')[-1]
                        if(file_type=='png' or file_type=='jpeg' or file_type=='gif'):
                            try:
                                print "     Filename:",i['MESSAGE']
                                subprocess.check_output(["tycat","-g","50x50",i['MESSAGE']])
                            except:
                                pass
                        else:
                            print "     Filename:",i['MESSAGE']
                            subprocess.Popen(["cat",i['MESSAGE']])
                        print
                rdy_ = raw_input("Ready?")

                for i in messages[ip,port]:
                    if(i['type']=='F'):
                        os.remove(i['MESSAGE'])
     
                messages[ip,port]=[]


        elif (input[0] == "send"):
            ip = input[1].split(":")[0]
            port = input[1].split(":")[1]
            if(input[2] == "M"):
                message = raw_input("Message: ").decode(sys.stdin.encoding)
                send_message(ip,int(port),message,context)
            elif(input[2] == "F"):
                file = raw_input("Path: ").decode(sys.stdin.encoding)
                send_file(ip,int(port),file,context)
            else:
                print "not valid command"
                continue

    except:
        print
        fn[0] = False
        send_message(get_local_ip(),int(sys.argv[1]),"xxx",context)
        #os.remove("temp/*")
        break