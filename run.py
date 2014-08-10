from datetime import datetime

from flask import Flask
from flask import request
from flask import render_template
from flask import redirect, url_for
from flask import flash, get_flashed_messages
from flask import jsonify

from models import Job

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           queue_size=Job.queue_size())


@app.route('/submit', methods=['POST'])
def submit():
    options = request.form
    j_id = Job.create(options)
    return jsonify(jobid=str(j_id),
                   qsize=Job.queue_size())
                   

@app.route('/status/<job_id>')
def status(job_id):
    job = Job.get(job_id)
    if not job or not job['is_done']:
        return 'false'
    else:
        return 'true'

    
@app.route('/result/<job_id>')
def result(job_id):
    job = Job.get(job_id)
    if not job or not job['is_done']:
        return 'Not found', 404
    temp_dir = job['temp_dir']
    data = open(temp_dir + '/result.txt').read()
    return data


if __name__ == '__main__':
    app.debug = True
    app.run()
