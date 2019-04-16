#! /usr/bin/python
# -*- coding:utf-8 -*-

#Deuxième version toute simple du web service ressenti en mode asynchrone
zapli="\n\n demo1_async_ressenti.py   zf190415.1841 \n"
zusage="Usage: http://siipc6.epfl.ch:5050/url/http/z.zufferey.com\n\n"

#source: http://sdz.tdct.org/sdz/creez-vos-applications-web-avec-flask.html#Premierspas
#source: https://stackoverflow.com/questions/30554702/cant-connect-to-flask-web-service-connection-refused
#source: https://stackoverflow.com/questions/89228/calling-an-external-command-in-python
#source: https://openclassrooms.com/fr/courses/235344-apprenez-a-programmer-en-python/2235545-faites-de-la-programmation-parallele-avec-threading


import time
import os
import subprocess
import threading
#from threading import Thread
from flask import Flask, redirect, url_for, request

app = Flask(__name__)
zstack = []


class zget_time(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while str(threading.enumerate()[0]).find("started") > 0 :
            while len(zstack) > 0 :
                print("zstack: " + str(zstack))
                zurl = zstack[0]
                print("je mesure: " + zurl)
                time.sleep(3)               #je vais mesurer l'url :-)
                print("url retiree: " + zstack.pop(0))        #je retire l'url du fifo
            time.sleep(2)
            print("je boucle :-)")
            print("len of stack: " + str(len(zstack)))
            print("thread.enumerate: " + str(str(threading.enumerate()[0]).find("started")))






@app.route('/toto')
def toto():
    zurl = request.args.get('url')
    print("url: " + zurl)
    zstack.append(zurl)
    print(zstack)

    return "c'est ok !"









@app.route('/')
def index():
    zurl = request.args.get('url')
    print("url: " + zurl)
    zimg = zurl.replace('http://', '')  ;  zimg = zimg.replace('https://', '')  ;  zimg = zimg.replace('/', '_')
    print("img: " + zimg)

    start = time.time()
#    cmd = "timeout 31 firefox -headless -screenshot toto.png " + proto + "://" + url + " 2>/dev/null"
    cmd = "docker exec -it docker-ressenti /bin/bash /root/work/screenshot.sh  " + zurl + " " + zimg
    os.system(cmd)
    end = time.time()
    result = str(end-start)
    return zapli + "<br><br>ça a tourné en " + result + " secondes" 


if __name__ == '__main__':
    print (zapli)
    print(zusage)

    thread_1 = zget_time()
    thread_1.start()
    app.run(host='0.0.0.0',port=5000, debug=True, use_reloader=False)



