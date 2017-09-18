#!/usr/bin/python
import sqlite3
import sys
import socket
import threading
import logging
RECV_BUFFER_SIZE = 1024


def get_your_ip():
    """Return my ip."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com", 80))
        res = (s.getsockname()[0])
        s.close()
        return str(res)
    except:
        return None


def create_nodes_database():
    """Create database for connected nodes."""
    try:
        conn = sqlite3.connect('.c_nodes.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS nodes_table(ip VARCHAR,port INTEGER,ping REAL, rtt INTEGER)")
        c.close()
        conn.close()
        return True
    except:
        return False


def add_node_to_database(ip, port):
    """Add (ip, port) to nodes database."""
    try:
        conn_ = sqlite3.connect('.c_nodes.db')
        c = conn_.cursor()
        c.execute('INSERT INTO nodes_table VALUES("{}",{},0,0)'.format(str(ip), str(port)))
        conn_.commit()
        c.close()
        conn_.close()
    except Exception as e:
        print e


def connect_to(ip, port, message):
    """Connect to node (ip, port)."""
    data = ''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, int(port))
        sock.connect(server_address)
        sock.sendall(str(message))
        data = sock.recv(RECV_BUFFER_SIZE)
        sock.close()
        if(data == "TRUE"):
            add_node_to_database(ip, port)
            return True
        else:
            return False
    except:
        return False


def new_connection_hander(conn, c_add):
    """Handle a connection."""
    try:
        while True:
            data = conn.recv(RECV_BUFFER_SIZE)
            if data:
                data = data.split("::")
                if data[0] == "CONNECTION":
                    parameters = data[1].split(":")
                    print parameters
                    add_node_to_database(parameters[0], parameters[1])
                    conn.sendall("TRUE")
            else:
                break
    except:
        print "ERROR : newSocket"
    finally:
        conn.close()
create_nodes_database()
if(len(sys.argv) > 2):
    connect_to(sys.argv[2], sys.argv[3], "CONNECTION::{}:{}".format(get_your_ip(), sys.argv[1]))

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('', int(sys.argv[1]))
    sock.bind(server_address)
    sock.listen(5)
    while True:
        connection, client_address = sock.accept()
        t = threading.Thread(target=new_connection_hander, args=(connection, client_address,))
        t.start()
except:
    print "error"
