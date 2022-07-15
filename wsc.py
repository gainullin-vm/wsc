#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import subprocess
import json
import getpass
import re
import os
import time
import requests
from datetime import datetime

# author @Lani_Ka_Nani

proxies = {
    "http": "htttp://",
    "https": "http://",
}

timecount = str(time.strftime("%b_%d"))
os.system('sudo touch /home/v.gaynullin/okko-events_' + timecount + '.json')
os.system('sudo chmod 666 /home/v.gaynullin/okko-events_' + timecount + '.json')

sendFile = '/home/v.gaynullin/okko-events_' + timecount + '.json'
msg = 'Hi, please look at file with hls links bellow:'

def telega_msg(file, proxies):
    bot_tokken = ''
    data1 = {'chat_id': '-', 'text':msg}
    files = {'document': file}
    data2 = {'chat_id': '-'}
    req1 = requests.post('https://api.telegram.org/bot' + bot_tokken + '/sendMessage', data=data1, proxies=proxies)
#    print(req1)
    req2 = requests.post('https://api.telegram.org/bot' + bot_tokken + '/sendDocument', data=data2, files=files, proxies=proxies)
#    print(req2)



file = open(sendFile, "w")


# Login
login = input('Enter login: ')

# Password
password = getpass.getpass(prompt='Enter your password: ')

# Stream ID
streamID = input('Enter stream ID: ')


def get_links(login, password, streamID):
    shellCommand1 = "curl --silent -u " + login + ":" + password + " http://" + streamID + "/streams"
    a = subprocess.check_output(shellCommand1, shell=True)
    shellCommand3 = "curl --silent -u " + login + ":" + password + " http://" + streamID
    b = subprocess.check_output(shellCommand3, shell=True)
    result1 = a.decode("utf-8")
    result3 = b.decode("utf-8")
    # Преобразование текста в json
    mainObj = json.loads(result1)
    secondObj = json.loads(result3)
    hls_nodrm_links = []
    # Выбор типа ДРМ и работа с фильтром
    selectedDRM = 'NO_DRM'
    selectedLINK = 'HLS'
    # Элемент
    for element in mainObj:
        if (element['drmType'] == selectedDRM) & (element['type'] == selectedLINK):
            hls_nodrm_links.append(element)
#    print("{")
    simbol = "{"
    file.write(simbol + "\n")
#    print("\"name\":" + "\"" + secondObj['name'] + "\",")
    simbol = "\"name\":" + "\"" + secondObj['name'] + "\","
    file.write(simbol + "\n")
#    print("\"id\":" + "\"" + secondObj['id'] + "\",")
    simbol = "\"id\":" + "\"" + secondObj['id'] + "\","
    file.write(simbol + "\n")
#    print("\"startDate\":" + "\"" + secondObj['startDate'] + "\",")
    simbol = "\"startDate\":" + "\"" + secondObj['startDate'] + "\","
    file.write(simbol + "\n")
    length = len(hls_nodrm_links)
    length_check = 1
    for element in hls_nodrm_links:
        if (element['drmType'] == selectedDRM) & (element['type'] == selectedLINK):
            # Записываем переменные num и folder
            foundElement = re.findall(r'^\D+(\d+)[\w\.]+\/\w+\/u\/(\w+\/[\w-]+)\/(.*)', element['url'])
            # Преобразование выбранных ссылок
            # Ввод переменных
            userid = ''
            salt = ''
            secure_link_expires = str(int(time.time() + 604800))
            pre = foundElement[0]
            num = pre[0]
            folder = pre[1]
            lastfolder = pre[2]
            prefolder = re.findall(r'(/[\w-]+)', folder)
            folder2 = str(prefolder[0])
            # Формирование подписи
            shellCommand2 = "echo -n " + salt + userid + secure_link_expires + '/' + num + '/' + folder + " | openssl md5 -binary | openssl base64 | tr +/ -_ | tr -d ="
            b = subprocess.check_output(shellCommand2, shell=True)
            result2 = b.decode("utf-8")
            # Формирование финальной ссылки
            finalLink = "https://" + userid + "-" + secure_link_expires + "-" + result2 + "/" + num + "/" + folder + "/" + lastfolder
            # Вывод ссылок
            FPS = str(int(element['video']['frameRate']))
            vivod = re.findall(r'([^\s]+)', finalLink)
            if length_check == length:
#               print("\"hlsUrl{}fps\"".format(FPS) + ":\"" + vivod[0] + vivod[1] + "\"")
                simbol = "\"hlsUrl{}fps\"".format(FPS) + ":\"" + vivod[0] + vivod[1] + "\""
                file.write(simbol + "\n")
            else:
#               print("\"hlsUrl{}fps\"".format(FPS) + ":\"" + vivod[0] + vivod[1] + "\",")
                simbol = "\"hlsUrl{}fps\"".format(FPS) + ":\"" + vivod[0] + vivod[1] + "\","
                file.write(simbol + "\n")
            length_check += 1
#   print("},")
    simbol = "},"
    file.write(simbol + "\n")


if streamID == "":
    shellCommand4 = "curl --silent -u " + login + ":" + password + " http://"
    c = subprocess.check_output(shellCommand4, shell=True)
    result4 = c.decode("utf-8")
    broadcastsObj = json.loads(result4)
#    print("[")
    simbol = "["
    file.write(simbol + "\n")
    for element in broadcastsObj:
        if element['type'] == "SPORT_EVENT":
            if element['id'] != "" or element['id'] != "":
                if re.findall(r'^\d+\-\d+\-\d+', str(element['startDate']))[0] >= str(datetime.date(datetime.now())):
                    streamID = element['id']
                    get_links(login, password, streamID)
#   print("]")
    simbol = "]"
    file.write(simbol + "\n")
else:
#    print("[")
    simbol = "["
    file.write(simbol + "\n")
    get_links(login, password, streamID)
#    print("]")
    simbol = "]"
    file.write(simbol + "\n")

file.close()
file = open(sendFile, "r")
telega_msg(file, proxies)

os.system('sudo rm /home/v.gaynullin/okko-events_' + timecount + '.json')
print('json file okko-events_' + timecount + '.json was sent successfully')
