import RPi.GPIO as GPIO
import time
import BaseHTTPServer
import urlparse
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

html = '''
<html>
<head>
<title>Remote Light Control</title>
<link rel="apple-touch-icon" href="/bulb.png">
<meta name="apple-mobile-web-app-title" content="DeckLights">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black">
<style>
@font-face{ font-family: fontawesome; src: url(http://uselesstrash.com/fa-regular-400.ttf); }
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
        pin = 17
    elif cmd== "off":
        pin = 18
    else:
        print "Command '{}' is invalid.".format(cmd)
        return

    GPIO.setup(pin,GPIO.OUT)
    #print "'{}' button press".format(cmd)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(0.2)
    #print "'{}' button release".format(cmd)
    GPIO.output(pin,GPIO.LOW)

class Server(BaseHTTPServer.BaseHTTPRequestHandler):
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
        
httpd = BaseHTTPServer.HTTPServer( ('', 80), Server)
httpd.serve_forever()

