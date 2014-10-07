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

def extract_rate(rstr):
    return float(rstr[0].strip())

def create_network_file(net_filename, options):
    f = open(net_filename,'w')

    if 'rate-rail-road' in options:
        rr_rate = extract_rate(options['rate-rail-road'])
    else:
        rr_rate = None

    if 'rate-canal-road' in options:
        cr_rate = extract_rate(options['rate-canal-road'])
    else:
        cr_rate = None

    net_files = ['bts', 'mrt',
                 'chaophraya',
                 'bangkoknoi', 'bangsue', 'omnon',
                 'ladprao', 'saensap', 'phasicharoen']
    rail_files = set(['bts','mrt'])
    for n in net_files:
        net_key = 'net-%s' % n

        if net_key in options:
            cmd = ['network','../../../data/%s.csv' % n]
        
            if n not in rail_files:
                cmd.append('color:blue')
                if cr_rate:
                    cmd.append('adv_factor:%f' % cr_rate)
            else:
                if rr_rate:
                    cmd.append('adv_factor:%f' % rr_rate)

            print >> f, ' '.join(cmd)
    if 'max-walk-distance' in options:
        max_walk_distance = float(options['max-walk-distance'][0].strip())
        if max_walk_distance > 0:
            print >> f, 'max-walk-distance', max_walk_distance
    f.close()

def work(job):
    job_dir = tempfile.mkdtemp(dir=JOB_DIR)

    net_filename = os.path.join(job_dir, 'network.cfg')
    trip_filename = os.path.join(job_dir, '../../../test/trip-u3000.txt')
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
    
