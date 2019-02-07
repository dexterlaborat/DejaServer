from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import random
import cgi 
import json
import os
import datetime
import operator
import pandas as pd

port_num=8080
hostName="localhost"

class DejaServer(BaseHTTPRequestHandler):

    def add_response(self,query=None):
        recieve_time = time.time()
        time.sleep(random.random() * 10)
        processing_time = round(time.time() - recieve_time,3)
        if query is None:
            query=''
        data='{"path":"%s", "Method":"%s", "ReceivedTime":"%s","Processing Time": "%s sec","query":"%s"}' % (self.path,self.command,time.asctime(),processing_time,query)
        dt=json.loads(data)
        return dt

    def resp_calc(self, s):
            return s.replace('sec','')
    
    def last_hour(self, log_date):
            current=datetime.datetime.today()
            last_hour=current-datetime.timedelta(hours=1)
            return operator.ge(log_date,last_hour)

    def last_minute(self, log_minute):
            current=datetime.datetime.today()
            last_minute=current-datetime.timedelta(minutes=1)
            return operator.ge(log_minute,last_minute)
    
    def add_headers(self):
        self.send_header('Content-Type','application/json')
        self.send_header('X-Frame-Options','DENY')
        self.send_header('Cache-Control','no-cache')
    
    def log_requests(self,data):
        with open('temp.csv','a') as w:
            w.write("{},{},{},{}\n".format(data['path'],data['Method'],data['ReceivedTime'],data['Processing Time'],data['query']))
   
    def get_stats(self):
        try:
            df=pd.read_csv('temp.csv')
            column=['path','method','receiving_date','processing_time']
            df.columns=column
            current_date=datetime.datetime.now()
            df['receiving_date'] = pd.to_datetime(df['receiving_date'])
            process_time=list(map(self.resp_calc,df['processing_time']))
            df['processing_time']=pd.Series(map(float,process_time))
            avg_response=sum(df['processing_time'])/len(df['processing_time'])
            _hours=list(map(self.last_hour,df['receiving_date']))
            _minutes=list(map(self.last_minute,df['receiving_date']))
            total_request=len(df['method']) 
            total_get_req=len(df[df['method'] == 'GET'])
            total_post_req=len(df[df['method'] == 'POST'])
            total_put_req=len(df[df['method'] == 'PUT'])
            total_del_req=len(df[df['method'] == 'DELETE'])
            return '{"Total" : "%s", "GET" : "%s", "POST" : "%s", "PUT" : "%s", "DELETE" : "%s", "Average Response" : "%s", "Last Hour" : "%s", "Last Minute" : "%s"}' % (total_request,total_get_req,total_post_req,total_put_req,total_del_req,round(avg_response,2),len(df[_hours]),len(df[_minutes]))
        except pd.errors.EmptyDataError:
            self.wfile.write(b'No Logs To Make Stats. Try to make some request for real time stats')
        except Exception as e:
            self.wfile.write(b'Unexpected Error Occured!!!')
        
    def handler404(self):
        self.send_response(404)
        self.add_headers()
        self.end_headers()
        data=self.add_response()
        self.wfile.write(bytes(str(data), 'utf-8'))
        self.log_requests(data)
    
    def do_GET(self):
        if self.path == '/process':
            self.send_response(200)
            self.add_headers()
            self.end_headers()
            data = self.add_response()
            self.wfile.write(bytes(str(data), 'utf-8'))
            self.log_requests(data)
        elif self.path == '/stats':
            self.send_response(200)
            self.add_headers()
            self.end_headers()
            time.sleep(random.random() * 10) 
            data = self.get_stats()
            if data is not None:
                self.wfile.write(bytes(str(data), 'utf-8'))
        else:
            self.handler404()

    def do_POST(self):
        self.send_response(200)
        self.add_headers()
        self.end_headers()
        form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD': 'POST'})
        if form.getvalue("data"):
            query = form.getvalue("data")
        else:
            pass
            #import pdb;pdb.set_trace();
            query = ''
        data=self.add_response(query)
        self.wfile.write(bytes(str(data), 'utf-8'))
        self.log_requests(data)

    def do_PUT(self):
        self.send_response(200)
        self.add_headers()
        self.end_headers()
        form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD': 'PUT'}) 
        query = form.getvalue("data")
        data = self.add_response(query)
        self.wfile.write(bytes(str(data), 'utf-8' ))
        self.log_requests(data)


    def do_DELETE(self):
        self.send_response(301)
        self.add_headers()
        self.end_headers()
        form = cgi.FieldStorage(fp=self.rfile,headers=self.headers,environ={'REQUEST_METHOD': 'DELETE'})
        query = form.getvalue('data')
        data = self.add_response(query)
        self.wfile.write(bytes(str(data), 'utf-8' ))
        self.log_requests(data)

if __name__=='__main__':
    if os.system('ls | grep "temp.csv"') == 0:
        #import pdb;pdb.set_trace();
        os.system('rm -rf "temp.csv"')
        os.system('touch temp.csv')
    else:
        os.system('touch temp.csv')
    mServer = HTTPServer((hostName,port_num),DejaServer)
    print(time.asctime(), "Server started as  %s:%s" % (hostName,port_num))

    try:
        mServer.serve_forever()
    except KeyboardInterrupt:
        mServer.server_close();



