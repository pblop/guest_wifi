from flask import Flask, request, redirect, abort, jsonify, send_from_directory
from waitress import serve
from threading import Thread, Event
import time
from random import randint
import ndsctl
from lcd import LCD
import json

app = Flask(__name__)
lcd = LCD()

stop_event = Event()
auth_number = None

def gen_number():
  return ''.join([str(randint(0, 9)) for _ in range(6)])

@app.route("/check")
def check():
  code = request.args.get('code')
  ip = request.remote_addr

  client = ndsctl.get_client_by(ip)
  if client['state'] == 'Authenticated':
    return redirect('https://google.es', code=302)

  if code == auth_number:
    try:
      ndsctl.authenticate(ip)
      return redirect('https://google.es', code=302)
    except ndsctl.AuthenticateException:
      print(f'Error authenticating {ip}')
      print('Client: ' + json.dumps(client))
      return abort(f'/', code=500)
  else:
    return redirect('https://google.es', code=302)

@app.route("/checkjson", methods=['POST'])
def checkjson():
  json = request.get_json()
  if json == None:
    return abort(f'/', code=400)

  ip = request.remote_addr

  client = ndsctl.get_client_by(ip)
  if client['state'] == 'Authenticated':
    return jsonify({
        'status': 'connected'
        })

  code = json['code']
  if code == auth_number:
      try:
        ndsctl.authenticate(ip)
        return jsonify({
          'status': 'connected'
          })
      except ndsctl.AuthenticateException:
        print(f'Error authenticating {ip}')
        print('Client: ' + json.dumps(client))
        return jsonify({
          'status': 'not connected'
          })
  else:
    return jsonify({
          'status': 'not connected'
          })

@app.route("/num")
def num():
  return "Number: " + auth_number


## begin JUST SERVE THE APP ALREADY
@app.route('/<path:filename>')
def download_file(filename):
    return send_from_directory('public',filename)

# TODO: SWITCH FLASK
# i hate flask, i have to do this just to be able to get files from /public/static
@app.route('/static/<path:folder>/<path:filename>')
def download_file2(filename, folder):
  if folder == 'js':
    return send_from_directory('public/static/js',filename)
  elif folder == 'css':
    return send_from_directory('public/static/css',filename)
  else:
    return abort(404)

@app.route('/')
def main():
    return send_from_directory('public','index.html')

## end JUST SERVE THE APP ALREADY

def gen_numbers_worker():
  """generates random numbers each minute"""
  while True:
    if stop_event.is_set():
      break
    global auth_number
    auth_number = gen_number()
    for i in range(16):
      lcd.write(code=auth_number, seconds_remaining=(16-i))
      time.sleep(1)

def flask_worker():
  serve(app, host='0.0.0.0', port='5000')

if __name__ == "__main__":
  gen_numbers_t = Thread(target=gen_numbers_worker, args=())
  flask_t = Thread(target=flask_worker, args=())
  gen_numbers_t.start()
  flask_t.start()
  # app.run()