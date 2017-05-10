# overhead2


What is this?
-----------

Overhead2 is a python script that performs a DoS by overloading a web server with GET petitions. Also it can perform a DoS with
POST requests and you can inject data (by defaul 100 characters are generated).
In order to use all the power of the tool you should look for a GET petition that is heavy or takes some time to load, or find an unfiltred form that allow you to inject data.

__Currently the proxy option isn't working and POST isn't finished at all__

<img class="emoji" title=":exclamation:" alt=":exclamation:" height="20" width="20" src="https://assets-cdn.github.com/images/icons/emoji/unicode/2757.png"></g-emoji> Requeriments
-----------
* Linux system
* Python 3.x
* Requests library

Installation
-----------
> Install Python3
$ pip install requests
$ git clone https://github.com/hacknation-anonops/Overhead2.git

How it works
----------

__GET__

$ python overhead2.py -u target.com --get

$ python overhead2.py -u target.com -t 50 -p tor --get

__POST__

$ python overhead2.py -u target.com/?data= --threads 120 -p 44.44.44.44:80 --post
