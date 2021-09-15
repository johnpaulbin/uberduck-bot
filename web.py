from flask import Flask
from threading import Thread

"""
for repl.it
"""

app = Flask('')

@app.route('/')
def home():
    return "HEYO!!!!! this is meant to keep the bot alive!!!"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()