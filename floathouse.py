#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import BaseHTTPServer
import ssl
import urlparse
import os, sys
import socket

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

html = '''
<html>
<head>
<title>Remote Light Control</title>
<link rel="apple-touch-icon" href="/bulb.png">
<meta name="apple-mobile-web-app-title" content="FloatHouse">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<style>
@font-face{ font-family: fontawesome; src: url(/fa-regular-400.ttf); }
p{ font-size: 50vh; font-family: fontawesome; margin:0; }
a{ text-decoration:none; }
</style>
<script type="text/javascript">
var xhttp = new XMLHttpRequest();
function sendCmd(cmd){
    xhttp.open('GET', '?cmd='+cmd);
    xhttp.send();
}
</script>
</head>
<body style="text-align:center">
<p><a href="javascript:sendCmd('on')"  style="color: gold ">&#xf0eb;</a><br/>
<a href="javascript:sendCmd('off')" style="color: black">&#xf0eb;</a></p>
</body>
</html>
'''

'''
<p><a href="?cmd=on" style="color: yellow">&#xf0eb;</a><br/>
<a href="?cmd=off" style="color: black">&#xf0eb;</a></p>
'''

def execCmd(cmd):
    if cmd == "on":
        pin = 27
    elif cmd== "off":
        pin = 17 # 18
    else:
        print "Command '{}' is invalid.".format(cmd)
        return

    GPIO.setup(pin,GPIO.OUT)
    #print "'{}' button press".format(cmd)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(0.2)
    #print "'{}' button release".format(cmd)
    GPIO.output(pin,GPIO.LOW)

keyfile="/home/pi/floathouse.local.key"
certfile="/home/pi/floathouse.local.crt"

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        if self.path == "/bulb.png":
            self.send_header("Content-type", "image/png")
        else:
            self.send_header("Content-type", "text/html")
    def do_GET(self):
        if self.path == "/bulb.png":
            icon = open("/usr/local/share/bulb.png",'r')
            self.send_response(200)
            self.send_header("Content-type", "image/png")
            self.end_headers()
            self.wfile.write(icon.read())
            icon.close()
        elif self.path == "/fa-regular-400.ttf":
            icon = open("/usr/local/share/fonts/fa-regular-400.ttf",'r')
            self.send_response(200)
            self.send_header("Content-type", "application/octet-stream")
            self.end_headers()
            self.wfile.write(icon.read())
            icon.close()
        else:
            #print self.path
            params = urlparse.parse_qs(self.path[2:])
            #print params
            if "cmd" in params and (params["cmd"][0] == "on" or params["cmd"][0] == "off"):
                execCmd(params["cmd"][0])
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html)

class Server(BaseHTTPServer.HTTPServer):
    def __init__(self, handler):
        BaseHTTPServer.HTTPServer.__init__(self, ('',0), handler, bind_and_activate=False)
        sock = socket.fromfd(3, self.address_family, self.socket_type)
        self.socket = socket.socket(_sock=sock)
        
    def _get_request(self):
        newsocket, fromaddr = self.socket.accept()
        connstream = ssl.wrap_socket(newsocket,
                                     server_side=True,
                                     certfile = certfile,
                                     keyfile = keyfile,
				     ssl_version = ssl.PROTOCOL_TLSv1,
                                     do_handshake_on_connect=False
                                     )
        return connstream, fromaddr

httpd = Server(Handler)
httpd.serve_forever()
