from flask import Flask, render_template
import os
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
  return render_template('index.html', status = status)
  
@app.route('/stop', methods=['GET', 'POST'])
def stop():
  s = os.popen('service fail2ban stop')
  f = os.popen('service fail2ban status')
  status = f.read()
  return render_template('index.html', status = status)
  
##############################
# Config page                #
##############################

@app.route('/config', methods=['GET','POST'])
def config():
  return null

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0')

