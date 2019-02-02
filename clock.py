import sys
import os
import pymongo
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

sched = BlockingScheduler()

# Standard URI format: mongodb://[dbuser:dbpassword@]host:port/dbname

uri = os.environ['DB_CONN_LOG']

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every one minutes.')
    client = pymongo.MongoClient(uri)
    db = client.get_database()
    logs = db['logs']
    logs.insert({
        'ts': datetime.utcnow(),
        'desc': 'Running media scheduler cron'
    })
    client.close()


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()