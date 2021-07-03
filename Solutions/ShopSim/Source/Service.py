import socket
import threading
import time
import json
import abc
import requests
import random
import hashlib
import string

class Service(metaclass=abc.ABCMeta):
    def __init__(self, name, thisPort):
        self.thisPort = thisPort
        self.name = name
        self.running = True

    @abc.abstractmethod
    def Execute(self, parameterMap):
        return None
    
    def _Parse(self, data, parameterMap):
        if parameterMap.get('length') == None:

            if data.find('Content-Length:') == -1:
                return False

            # get mode and url by HTTP mark
            httpEndPos = data.find('\r\n')
            httpString = data[0 : httpEndPos]
            items = httpString.split(' ')
            if parameterMap.get('mode') == None:
                parameterMap['mode'] = items[0]
            if parameterMap.get('url') == None:
                parameterMap['url'] = items[1]

            # get length by Content-Length mark
            lengthPos = data.find('Content-Length:')
            lengthEndPos = data.find('\r\n', lengthPos)
            lengthString = data[lengthPos : lengthEndPos]
            items = lengthString.split(' ')
            parameterMap['length'] = items[1]

            # get content
            contextStartPos = data.find('\r\n\r\n') + 4
            parameterMap['content'] = data[contextStartPos : len(data)]

        else:
            parameterMap['content'] = parameterMap['content'] + data
            
        if len(parameterMap['content']) >= int(parameterMap['length']):
            return True
        else:
            return False

    def HttpThread(self, clientSocket, clientAddress):
        parameterMap = {}
        while True:
            data = clientSocket.recv(1024).decode()
            done = self._Parse(data, parameterMap)
            if done == True:
                break

        got = {}
        got["SUCCEED"] = True
        got["DATA"] = self.Execute(parameterMap)

        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n'
        body = json.dumps(got)
        clientSocket.send((header + body).encode())
        clientSocket.close()

    def Run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', int(self.thisPort)))
        s.listen(5)
        while True:
            clientSocket, clientAddress = s.accept()
            if clientAddress[0] != '127.0.0.1':
                continue

            if self.running == False:
                break
            
            httpThread = threading.Thread(target = self.HttpThread, args = (clientSocket, clientAddress))
            httpThread.start()

    