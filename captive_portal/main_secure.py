from flask import Flask, request, redirect, abort, jsonify
from waitress import serve
from threading import Thread, Event
import time
from random import randint
import ndsctl
from lcd import LCD
import json
# import serial

app = Flask(__name__, static_folder='./static')
# ser = serial.Serial('/dev/ttyACM0')
lcd = LCD()

stop_event = Event()
auth_number = None

def gen_number():
  return ''.join([str(randint(0, 9)) for _ in range(6)])

@app.route("/")
def main():
  return app.send_static_file('./index.html')

@app.route("/check")
def check():
  code = request.args.get('code')
  ip = request.remote_addr

  client = ndsctl.get_client_by(ip)
  if client['state'] != 'Authenticated':
    return redirect(f'/', code=302)

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

@app.route("/checkjson")
def check():
  json = request.get_json()
  if json == None:
    return abort(f'/', code=400)

  ip = request.remote_addr

  client = ndsctl.get_client_by(ip)
  if client['state'] != 'Authenticated':
    return jsonify({
        "connected": True
        })

  code = json['code']
  if code == auth_number:
      try:
        ndsctl.authenticate(ip)
        return jsonify({
          "connected": True
          })
      except ndsctl.AuthenticateException:
        print(f'Error authenticating {ip}')
        print('Client: ' + json.dumps(client))
        return jsonify({
          "connected": False
          })
  else:
    return jsonify({
          "connected": False
          })

@app.route("/num")
def num():
  return "Number: " + auth_number

def gen_numbers_worker():
  """generates random numbers each minute"""
  while True:
    if stop_event.is_set():
      break
    global auth_number
    auth_number = gen_number()
    for i in range(16):
      print(f'Number: {auth_number}. {16-i}/16')
      lcd.write(code=auth_number, seconds_remaining=(16-i))
      # ser.write(f'code={auth_number};seconds={16-i};'.encode('utf-8'))
      time.sleep(1)

def flask_worker():
  serve(app, host='0.0.0.0', port='5000')
  # app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
  gen_numbers_t = Thread(target=gen_numbers_worker, args=())
  flask_t = Thread(target=flask_worker, args=())
  gen_numbers_t.start()
  flask_t.start()
  # app.run()