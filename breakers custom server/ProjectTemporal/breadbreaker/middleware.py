from time import time
from wsgiref.handlers import format_date_time

#TODO: check if this is actually neccessary

class HeaderOrderMiddleWare:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        #delete added stuff
        del response['vary'] 
        #delete stuff to read in order
        del response['content-type']
        del response['content-length'] 
        
        
        #set header order
        response['server'] = "nginx"
        response['date'] = format_date_time(time())
        response['content-type'] = "application/x-messagepack; charset=utf-8"
        response['content-length'] = len(response.content)
        response['Access-Control-Allow-Origin'] = "*"
        response['via'] = "1.1 google"
        response['Alt-Svc'] = 'h3=":443"; ma=2592000,h3-29=":443"; ma=2592000' 
        

        return response