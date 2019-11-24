import json
import subprocess

def get_clients():
  raw_json = subprocess.run(
    [
      'ndsctl',
      'json'
    ],
    stdout=subprocess.PIPE
    ).stdout.decode('utf-8')
  return json.loads(raw_json)

def get_client_by(val):
  '''
    val can either be the client's ip, the client's mac or the client's token
  '''
  raw_json = subprocess.run(
    [
      'ndsctl',
      'json',
      val
    ],
    stdout=subprocess.PIPE
    ).stdout.decode('utf-8')
  parsed_json = json.loads(raw_json)
  return None if parsed_json == {} else parsed_json

def authenticate(val):
  '''
    val can either be the client's ip, the client's mac or the client's token
  '''
  output = subprocess.run(
    [
      'ndsctl',
      'auth',
      val
    ],
    stdout=subprocess.PIPE
    ).stdout.decode('utf-8')

  if 'Failed' in output:
    raise AuthenticateException()

class AuthenticateException(Exception):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)