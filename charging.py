#!/usr/bin/python
#-*- coding:utf-8 -*-
import socket
import json
from threading import Thread
#from encrypt import *
import time
from ctypes import *

Encrypt = cdll.LoadLibrary("./Encrypt_64.dll")

initip = 15 #起始ip
num = 105 #模拟数量
key = '1234567890abcdef' #密钥，位数必须是16的倍数
i = 0
t = []

config = {
    "essid": "XINGLUO_057575",
    "file": "/udata/config/system_config.ini",
    "password": "12345678",
    "cloud_server_address": "10.101.70.151",
    "cloud_server_port": 8100,
    "wifi_key": 1,
    "lora": 0
}

def sock_server(ip):
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((ip, 31001))
        print ip + '\n'
        sock.listen(5)
        conn, address = sock.accept()
        try:
            while True:
                encry_recv = conn.recv(256)
                recv = Encrypt.decrypt(key, encry_recv)
                recv = "".join(list((c_char*1024).from_address(recv))).split("\x00")[0]
                data = json.loads(recv)
                #print data
                #print "receive from " + ip
                if data["method"] == "device":
                    rep = {
                        "method": "device",
                        "status": 0,
                        "ip": ip,
                        "mac": "",
                        "device_name": ip,
                        "net": "eth0"
                    }
                elif data["method"] == "get":
                    if data["key"] == "cloud_server_address":
                        rep = {
                            "method": "get",
                            "status": 0,
                            "value": config["cloud_server_address"]
                        }
                    elif data["key"] == "cloud_server_port":
                        rep = {
                            "method": "get",
                            "status": 0,
                            "value": config["cloud_server_port"]
                        }
                    elif data["key"] == "essid":
                        rep = {
                            "method": "get",
                            "status": 0,
                            "value": config["essid"]
                        }
                    elif data["key"] == "password":
                        rep = {
                            "method": "get",
                            "status": 0,
                            "value": config["password"]
                        }
                    elif data["key"] == "method":
                        rep = {
                            "method": "get",
                            "status": 0,
                            "value": config["wifi_key"]
                        }
                    elif data["key"] == "enable":
                        rep = {
                            "method": "get",
                            "status": 0,
                            "value": config["lora"]
                        }
                elif data["method"] == "set":
                    # if data["key"] == "cloud_server_address":
                    #     config["cloud_server_address"] = data["value"]
                    # elif data["key"] == "cloud_server_port":
                    #     config["cloud_server_port"] = data["value"]
                    # elif data["key"] == "essid":
                    #     config["essid"] = data["value"]
                    # elif data["key"] == "password":
                    #     config["password"] = data["value"]
                    # elif data["key"] == "method":
                    #     config["wifi_key"] = data["value"]
                    # elif data["key"] == "enable":
                    #     config["lora"] = data["value"]
                    rep = {
                        "method": "set",
                        "status": 0
                    }
                elif data["method"] == "save":
                    rep = {
                        "method": "save",
                        "status": 0
                    }
                else:
                    print "recv error"
                rep = json.dumps(rep)
                #print rep
                encry_rep = Encrypt.encrypt(key, rep)
                encry_rep = "".join(list((c_char*1024).from_address(encry_rep))).split("\x00")[0]
                print type(encry_rep)
                conn.send(encry_rep)
                #print "send to " + ip + ":" + json.dumps(rep)
        except:
            print "input X to stop:"
            pass


while i < num:
    ip = "10.10.10." + str(initip)
    t.append(Thread(target=sock_server, args=(ip,)))
    t[i].daemon = True
    t[i].start()
    i += 1
    initip += 1

while True:
    time.sleep(1)
    Daemon = raw_input("input \"X\" to stop:")
    if Daemon == "X":
        break
    else:
        print "\n"
