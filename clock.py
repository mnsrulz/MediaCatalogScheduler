import sys
import os

from apscheduler.schedulers.blocking import BlockingScheduler
import drivewrapper as dw
import peliculasgoogledrive as peculasscraper
blockingScheduler = BlockingScheduler()


@blockingScheduler.scheduled_job('interval', minutes=5)
def google_drive_import_media_job():
    print('Executing google drive media import job.')
    dw.execute()


@blockingScheduler.scheduled_job('interval', days=1)
def peculas_scraper_job():
    print('Executing peculas scraper job.')
    peculasscraper.execute()


if os.environ['INITIATE_INSTANTLY'] == '1':
    google_drive_import_media_job()
    peculas_scraper_job()


# @blockingScheduler.scheduled_job('cron', day_of_week='mon-fri', hour=17)
# def scheduled_job():
#    print('This job is run every weekday at 5pm.')


blockingScheduler.start()

