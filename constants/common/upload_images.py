import requests
from artistx import settings

def upload(file):
  try:
    url = settings.IMAGE_UPLOAD_URL
    key = settings.IMAGE_UPLOAD_KEY
    res = requests.post(url=url, data={"key" : key}, files={"media" : file})
    return res
  except:
    return None