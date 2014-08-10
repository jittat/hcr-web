from datetime import datetime
from pymongo import MongoClient, ASCENDING

from bson.objectid import ObjectId

mongo_client = MongoClient()
db = mongo_client.hcr_db

class Job:
    jobs = db.jobs
    jobs.create_index([('timestamp', ASCENDING)])
                       
    @staticmethod
    def create(options):
        new_job = { 'options': options,
                    'is_done': False,
                    'timestamp': datetime.now() }
        job_id = Job.jobs.insert(new_job)
        return job_id

    @staticmethod
    def queue_size():
        return Job.jobs.find({'is_done': False}).count()

    @staticmethod
    def get(_id):
        job_id = ObjectId(_id)
        j = Job.jobs.find_one({'_id': job_id})
        return j

    @staticmethod
    def is_done(_id):
        j = Job.get(_id)
        return j and j['is_done']

    @staticmethod
    def save(job):
        Job.jobs.save(job)



