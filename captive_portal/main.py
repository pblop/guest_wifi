# Only works without security (fas_secure=0)
from flask import Flask, request, redirect, abort
from waitress import serve
from threading import Thread, Event
import time
from random import randint

nodogsplash_ip = '192.168.10.1'
nodogsplash_port = '2050'

app = Flask(__name__, static_folder='./static')

stop_event = Event()
auth_number = None

def gen_number():
  return ''.join([str(randint(0, 9)) for _ in range(6)])

user_info = {}

@app.route("/")
def main():
  tok = request.args.get('tok')
  redir = request.args.get('redir')
  ip = request.remote_addr

  print(tok)
  print(redir)

  if tok == None or redir == None:
    return redirect(f'/', code=302)
  else:
    user_info[ip] = (tok, redir)
    return app.send_static_file('./index.html')

@app.route("/check")
def check():
  code = request.args.get('code')
  ip = request.remote_addr

  if code == auth_number:
    (tok, redir) = user_info[ip]
    return redirect(f'http://{nodogsplash_ip}:{nodogsplash_port}/nodogsplash_auth/?tok={tok}&redir={redir}', code=302)
  else:
    return redirect(f'/', code=302)

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
    print('New number: ' + auth_number)
    time.sleep(10)

def flask_worker():
  serve(app, host='0.0.0.0', port='5000')
  # app.run(debug=False, use_reloader=False)

if __name__ == "__main__":
  gen_numbers_t = Thread(target=gen_numbers_worker, args=())
  flask_t = Thread(target=flask_worker, args=())
  gen_numbers_t.start()
  flask_t.start()
  # app.run()