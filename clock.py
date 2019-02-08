import sys

from apscheduler.schedulers.blocking import BlockingScheduler
import drivewrapper as dw

blockingScheduler = BlockingScheduler()
dw.execute()


@blockingScheduler.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every one minutes.')


@blockingScheduler.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')


blockingScheduler.start()

