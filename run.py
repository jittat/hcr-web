from datetime import datetime

from flask import Flask
from flask import request
from flask import render_template, redirect, url_for, flash, get_flashed_messages

from models import Job

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           queue_size=Job.queue_size())


if __name__ == '__main__':
    app.run()
