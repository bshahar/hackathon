from socket import *
import struct
import time
import getch
import threading
from scapy.all import get_if_addr
import ipaddress

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

while 1: #choose network to run on s
    time.sleep(0.0001)
    state_network = input("plese enter 1 if you want eth1 or 2 for eth2\n")
    if state_network == '1': 
        eth = get_if_addr("eth1") +"/16"
        break
    elif state_network == '2':
        eth = get_if_addr("eth2")+"/16" 
        break
    else:
        time.sleep(0.0001)
        pass

my_host_for_broadcast = str(ipaddress.ip_network(eth,False).broadcast_address) #get host broadcast

MY_PORT = 13117
DURATION_TIME_PLAY = 10
BUFFER_SIZE = 2048
FORMAT = '!IBH'

while 1:#so the program will run forever

    print(bcolors.UNDERLINE+bcolors.HEADER+"Client started, listening for offer requests..."+bcolors.ENDC)
    while 1:
        try:     
            client = socket(AF_INET, SOCK_DGRAM) # UDP
            client.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
            client.bind((my_host_for_broadcast, MY_PORT))
            data, addr = client.recvfrom(BUFFER_SIZE)
            client.close()
            (cookie, mytype, port) = struct.unpack(FORMAT, data) #get the port from the broadcast message
            if cookie!=0xfeedbeef or mytype!=2:
                raise Exception
            break
        except:
            time.sleep(1)
            pass    
    print( bcolors.OKGREEN+"Received offer from " +  addr[0] + " attempting to connect..." + bcolors.ENDC)

    try:
        host = addr[0]
        team_name = "shem_mekori"
        tcpClient = socket(AF_INET, SOCK_STREAM) 
        tcpClient.connect((host, port))
        tcpClient.send(team_name.encode())#send message to the server with the group name

        global run_
        run_ = True
        def press_keys(socket_tcp): #this func send chars to the server
            try: 
                ten_seconds = time.time() + DURATION_TIME_PLAY
                while time.time()<ten_seconds: 
                    ch = getch.getch().encode()
                    if run_:
                        socket_tcp.send(ch)
            except:
                pass

        data = tcpClient.recv(BUFFER_SIZE)
        print(bcolors.OKCYAN+data.decode()+bcolors.ENDC)

        game_th = threading.Thread(target=press_keys, args=(tcpClient,)) #create thread for the game so just when the game start it will send chars

        game_th.start()
        
        try:
            game_over = tcpClient.recv(BUFFER_SIZE) #get a message about the result of the game
            run_ = False
            game_th.join()
            print(bcolors.OKBLUE+game_over.decode()+bcolors.ENDC)
        except:
            run_ = False
            game_th.join()

        print(bcolors.WARNING+"server disconnected, listening for offer request..." + bcolors.ENDC)
    except:
        time.sleep(1)
        pass
    
