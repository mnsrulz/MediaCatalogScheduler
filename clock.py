import sys

from apscheduler.schedulers.blocking import BlockingScheduler
import drivewrapper as dw
blockingScheduler = BlockingScheduler()


@blockingScheduler.scheduled_job('interval', minutes=5)
def google_drive_import_media_job():
    print('Executing google drive media import job.')
    dw.execute()


# @blockingScheduler.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#    print('This job is run every weekday at 5pm.')


blockingScheduler.start()

