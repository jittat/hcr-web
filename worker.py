import time
import tempfile
import os
import os.path

from models import Job

POLL_TIME = 0.1

SCRIPT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                          '../scripts'))
JOB_DIR =  os.path.join(os.path.abspath(os.path.dirname(__file__)),
                        'jobs')

def create_network_file(net_filename, options):
    f = open(net_filename,'w')
    net_files = ['bts', 'mrt',
                 'bangkoknoi', 'bangsue', 'ladprao', 'saensap']
    for n in net_files:
        net_key = 'net-%s' % n
        if net_key in options:
            print >> f, 'network ../../../data/%s.csv' % n
    f.close()

def work(job):
    job_dir = tempfile.mkdtemp(dir=JOB_DIR)

    net_filename = os.path.join(job_dir, 'network.cfg')
    trip_filename = os.path.join(job_dir, '../../../test/trip-u5000.txt')
    result_filename = os.path.join(job_dir, 'result.txt')

    create_network_file(net_filename, job['options'])

    cwd = os.getcwd()
    os.chdir(job_dir)
    cmd = 'python %s/gentripstat.py %s %s > %s' % (SCRIPT_DIR,
                                                   net_filename,
                                                   trip_filename,
                                                   result_filename)
    os.system(cmd)

    job['temp_dir'] = job_dir
    
def main():
    while True:
        job = Job.get_queue()
        if job:
            print 'Working on',job['_id']
            work(job)
            job['is_done'] = True
            Job.save(job)
            print 'Done'
        else:
            time.sleep(POLL_TIME)

if __name__ == '__main__':
    main()
    
