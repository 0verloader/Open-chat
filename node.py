#!/usr/bin/python
import sqlite3
import sys
import socket
import threading
import logging
import time
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
        c.execute("CREATE TABLE IF NOT EXISTS nodes_table(ip VARCHAR,port INTEGER,ping REAL, rtt INTEGER, PRIMARY KEY (ip, port))")
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
    except:
        print "error"


def remove_node_from_database(ip,port):
    """Remove (ip,port) from nodes database."""
    try:
        conn_ = sqlite3.connect('.c_nodes.db')
        c = conn_.cursor()
        c.execute('DELETE FROM nodes_table WHERE ip="{}" and port={}'.format(ip,port))
        conn_.commit()
        c.close()
        conn_.close()
    except:
        print "ERROR: remove_entry"


def connect_to(ip, port, message, reply):
    """Connect to node (ip, port)."""
    data = ''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        server_address = (ip, int(port))
        sock.connect(server_address)
        sock.sendall(str(message))
        data = sock.recv(RECV_BUFFER_SIZE)
        sock.close()
        if(data == reply):
            if message.split("::")[0] == "CONNECTION":
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
                elif data[0] == "TEST":
                    conn.sendall("OK")
            else:
                break
    except:
        print "ERROR : newSocket"
    finally:
        conn.close()


def recover_db():
    """Return database."""
    try:
        conn = sqlite3.connect('.c_nodes.db')
        c = conn.cursor()
        c.execute('SELECT * FROM nodes_table')
        res = c.fetchall()
        conn.commit()
        c.close()
        return res
    except:
        print "errror recover"


def check_nodes():
    """Check all attached nodes to see if they are alive."""
    db = recover_db()
    print db
    for data in db:
        if not connect_to(data[0], data[1], "TEST::", "OK"):
            remove_node_from_database(data[0], data[1])


def check_nodes_t():
    while(True):
        time.sleep(5)
        check_nodes()



def listener():
    """Listen to new connections."""
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


if __name__ == '__main__':
    create_nodes_database()
    print get_your_ip(), sys.argv[1]
    if(len(sys.argv) > 2 and len(sys.argv) % 2 == 0):
        j = 2
        while(j < len(sys.argv)):
            connect_to(sys.argv[j], sys.argv[j + 1], "CONNECTION::{}:{}".format(get_your_ip(), sys.argv[1]),"TRUE")
            j = j + 2
    t = threading.Thread(target=listener, args=())
    t.start()
    t1 = threading.Thread(target=check_nodes_t, args=())
    t1.start()
    print recover_db()
