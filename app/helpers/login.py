from functools import wraps
from flask import request


def check_user_logged_in(f):
  @wraps(f)
  def __decorated(*args, **kwargs):
      # just do here everything what you need
      print (request.get_json())
      result = f(*args, **kwargs)
      return result
  return __decorated
