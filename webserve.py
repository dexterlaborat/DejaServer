import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random
import cgi 
import json
import os
import pandas as pd
from matplotlib import pyplot as plt
port_num=8080
hostName="localhost"

class DejaServer(BaseHTTPRequestHandler):
    #def __init__(self):
            #if os.system('ls | grep "temp.csv"') == 0 : 
               # os.system('rm -rf temp.csv')

    def add_response(self,query=None):
        recieve_time = time.time()
        time.sleep(random.random() * 10)
        processing_time = round(time.time() - recieve_time,3)
        if query is None:
            query=''
        data='{"path":"%s", "Method":"%s", "ReceivedTime":"%s","Processing Time": "%s sec","query":"%s"}' % (self.path,self.command,time.asctime(),processing_time,query)
        dt=json.loads(data)
        return dt

    def add_headers(self):
        #self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.send_header('X-Frame-Options','DENY')
        self.send_header('Cache-Control','no-cache')
    
    def log_requests(self,data):
        with open('temp.csv','a') as w:
#            import pdb;pdb.set_trace()
           # print("{} {} {}".format(data['path'],data['Method'],data['ReceivedTime'],data['Processing Time'],data['query']))
            w.write("{},{},{},{}\n".format(data['path'],data['Method'],data['ReceivedTime'],data['Processing Time'],data['query']))
   
    def ge_stats(self):
        df=pd.read_csv('temp.csv')
        import pdb;pdb.set_trace()
        
    def handler404(self):
        self.send_response(404)
        #print('s')
        #self.send_header('Content-Type')
        self.add_headers()
        self.end_headers()
        data=self.add_response()
        self.wfile.write(bytes(str(data), 'utf-8'))
        #self.wfile.write(b'''<html>Error!!!</html>''')
    
    def do_GET(self):
        if self.path == '/process':
            self.send_response(200)
            self.add_headers()
            #self.send_header('Content-Type','text/html')
            self.end_headers()
            data = self.add_response()
            self.wfile.write(bytes(str(data), 'utf-8'))
            self.log_requests(data)
           #self.wfile.write(bytes(str(self.path), 'utf-8'))
        elif self.path == '/stats':
            self.send_response(200)
            self.add_headers()
            self.end_headers()
            self.get_stats()
            self.wfile.write(bytes(str(data), 'utf-8'))
        else:
            self.handler404()

    def do_POST(self):
        self.send_response(200)
        self.add_headers()
        self.end_headers()
        form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD': 'POST'})
        query = form.getvalue("data")
 #       self.wfile.write(b'<html>POST_req</html>')
        data=self.add_response(query)
     #   dt=json.loads(data)
    #iprint(dt)
        self.wfile.write(bytes(str(data), 'utf-8'))
        self.log_requests(data)

    def do_PUT(self):
        self.wfile.write(b'PUT_req')

if __name__=='__main__':
    #dejaSer = DejaServer()
    #dejaSer.buildnew()
    mServer = HTTPServer((hostName,port_num),DejaServer)
    print(time.asctime(), "Server started as  %s:%s" % (hostName,port_num))

    try:
        mServer.serve_forever()
    except KeyboardInterrupt:
        mServer.server_close();



