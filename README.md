        
```
                   ▒█████   ██▓███  ▓█████  ███▄    █  ▄████▄   ██░ ██  ▄▄▄     ▄▄▄█████▓
                  ▒██▒  ██▒▓██░  ██▒▓█   ▀  ██ ▀█   █ ▒██▀ ▀█  ▓██░ ██▒▒████▄   ▓  ██▒ ▓▒
                  ▒██░  ██▒▓██░ ██▓▒▒███   ▓██  ▀█ ██▒▒▓█    ▄ ▒██▀▀██░▒██  ▀█▄ ▒ ▓██░ ▒░
                  ▒██   ██░▒██▄█▓▒ ▒▒▓█  ▄ ▓██▒  ▐▌██▒▒▓▓▄ ▄██▒░▓█ ░██ ░██▄▄▄▄██░ ▓██▓ ░ 
                  ░ ████▓▒░▒██▒ ░  ░░▒████▒▒██░   ▓██░▒ ▓███▀ ░░▓█▒░██▓ ▓█   ▓██▒ ▒██▒ ░ 
                  ░ ▒░▒░▒░ ▒▓▒░ ░  ░░░ ▒░ ░░ ▒░   ▒ ▒ ░ ░▒ ▒  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒ ░░   
                    ░ ▒ ▒░ ░▒ ░      ░ ░  ░░ ░░   ░ ▒░  ░  ▒    ▒ ░▒░ ░  ▒   ▒▒ ░   ░    
                  ░ ░ ░ ▒  ░░          ░      ░   ░ ░ ░         ░  ░░ ░  ░   ▒    ░      
                      ░ ░              ░  ░         ░ ░ ░       ░  ░  ░      ░  ░        
                                                  ░ 
                                  Secure      Private      Intelligent                                 
```
***version 1.5.0***

What is OPENchat
---
OpenCHAT is a platform which provides a stable and secure point to point connection between two terminals. It is proposed to be run on Terminology <https://www.enlightenment.org/about-terminology> for better support. SSL has been used in order to implement secure tcp sockets.

---


Prerequisites
---
- Python 2.7
- OpenSSL
---


How to run OPENchat
---
- openssl req -new -x509 -nodes -out cert.pem -keyout key.pem (just once for each client to create key and cert)
- python client.py (port)
---

OPENchat commands
---
- send::(ip):(port)::(M for Message or F for file)  : send message or file
- inbox::list  : show inbox
- inbox::(ip):(port)  : show inbox from a specific (ip):(port)
---

Contributors
---
- 0verloader <https://github.com/0verloader>

  Please report bugs to <konstantinosarakadakis@gmail.com>

License & copyright
---
Licenced under the [MIT licence](LICENSE).
