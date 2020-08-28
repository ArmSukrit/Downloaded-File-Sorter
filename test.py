from datetime import datetime
import os
import base64
from PIL import Image
import requests
from bs4 import BeautifulSoup
import json


with open('common temporary file extensions.json') as f:
    data = json.load(f)
    common_ext = [each['extension'] for each in data['common extensions']]

with open('common temporary file extensions as list.txt', 'w') as wf:
    wf.write(f'{common_ext}')



