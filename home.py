from flask import Flask, render_template, redirect, request
from flask.ext.basicauth import BasicAuth
import requests
import sys, os
import json
import ConfigParser
app = Flask(__name__)

#############################
# Password Protection       #
#############################

app.config['BASIC_AUTH_USERNAME'] = 'ouss'
app.config['BASIC_AUTH_PASSWORD'] = 'pass'

basic_auth = BasicAuth(app)

@app.route('/')
@basic_auth.required
def secret_view():
    return redirect('/home', code=302)

#############################
# Home page / start / stop  #
#############################

def fail2banStatus():
  f = os.popen('service fail2ban status')
  status = f.read()
  if ("inactive" in status or "not running" in status):
    return "fail2ban is not running"
  elif ("active" in status or "is running" in status):
    return "fail2ban is running"


@app.route('/home', methods=['GET', 'POST'])
@basic_auth.required
def home():
  status = fail2banStatus()
  return render_template('index.html', status = status)

@app.route('/start', methods=['GET', 'POST'])
def start():
  s = os.popen('service fail2ban start')
  status = fail2banStatus()
  return redirect("/", code=302)

@app.route('/stop', methods=['GET', 'POST'])
def stop():
  s = os.popen('service fail2ban stop')
  status = fail2banStatus()
  return redirect("/", code=302)

##############################
# Config page                #
##############################

@app.route('/config', methods=['GET','POST'])
@basic_auth.required
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
# Filter page                #
##############################

@app.route('/display/<s>', methods=['GET','POST'])
@basic_auth.required
def filter(s):
  try:
    filt = s
    cp= ConfigParser.RawConfigParser()
    file = "/etc/fail2ban/filter.d/"+filt+".conf"
    h = open(file,'r')
    f = h.read()
  except IOError:
    return render_template('filter.html', f = "there is a problem with this filter")
  return render_template('filter.html', f = f, service = filt)


@app.route('/save/<s>', methods=['GET','POST'])
def save_filter(s):
  try:
    f = request.form['filter']
    filt = s
    file = "/etc/fail2ban/filter.d/"+filt+".conf"
    h = open(file,'w')
    h.write(f)
    h.close()
  except IOError:
    return render_template('filter.html', f = "there is a problem with this filter")
  return redirect('/config', code=302)



##############################
# Banned IP                  #
##############################

def getcountry(ip):
	r = requests.get('http://ip-api.com/json/'+ip)
	parsed_json=r.json()
	return parsed_json

@app.route('/banned', methods=['GET', 'POST'])
@basic_auth.required
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
  return render_template('banned.html', printList = printList, getcountry=getcountry)


##############################
# App launcher               #
##############################

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')

