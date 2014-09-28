from flask import Flask, render_template, redirect
import os
import sys
import ConfigParser
app = Flask(__name__)

#############################
# Home page / start / stop  #
#############################

@app.route('/', methods=['GET', 'POST'])
def home():
  f = os.popen('service fail2ban status')
  status = f.read()
  return render_template('index.html', status = status)
  
@app.route('/start', methods=['GET', 'POST'])
def start():
  s = os.popen('service fail2ban start')
  f = os.popen('service fail2ban status')
  status = f.read()
  return redirect("/", code=302)

@app.route('/stop', methods=['GET', 'POST'])  
def stop():
  s = os.popen('service fail2ban stop')
  f = os.popen('service fail2ban status')
  status = f.read()
  return redirect("/", code=302)
  
##############################
# Config page                #
##############################

@app.route('/config', methods=['GET','POST'])
def config():
  cp= ConfigParser.RawConfigParser()
  cp.read( r"/etc/fail2ban/jail.conf" )
  services = cp.sections()
  return render_template('config.html', cp = cp, services = services)
  
@app.route('/enable/<s>', methods=['GET','POST'])  
def enable(s=None):
  cp= ConfigParser.RawConfigParser()
  cp.read(r'/etc/fail2ban/jail.conf')
  cp.set(s, 'enabled', 'true')
  with open('/etc/fail2ban/jail.conf', 'w') as configfile:
    cp.write(configfile)
  f = os.popen('service fail2ban restart')
  services = cp.sections()
  return redirect("/config", code=302)
  
@app.route('/disable/<s>', methods=['GET','POST'])  
def disable(s=None):
  cp= ConfigParser.RawConfigParser()
  cp.read(r'/etc/fail2ban/jail.conf')
  cp.set(s, 'enabled', 'false')
  with open('/etc/fail2ban/jail.conf', 'w') as configfile:
    cp.write(configfile)
  f = os.popen('service fail2ban restart')
  services = cp.sections()
  return redirect("/config", code=302)
  
##############################
# Banned IP                  #
##############################

@app.route('/banned', methods=['GET', 'POST'])
def banned():
  f = os.popen("cat /var/log/fail2ban.log | grep Ban | awk '{print $7}'")
  banned = f.read()
  
  
  theFile = open('/var/log/fail2ban.log','r')
  FILE = theFile.readlines()
  theFile.close()
  printList = []
  for line in FILE:
    if ('Ban' in line):
      printList.append(line)
  return render_template('banned.html', printList = printList)  
  
  
##############################
# App launcher               #
############################## 

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')

