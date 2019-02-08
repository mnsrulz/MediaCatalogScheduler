import os
import pymongo
from datetime import datetime

db_conn_log = os.environ['DB_CONN_LOG']
db_conn_media_catalog = os.environ['DB_CONN_MEDIA_CATALOG']

# Mongo db connection reference
db_log_client = None
db_media_client = None

# collection reference
db_log = None
db_media_catalog = None


def initialize():
    global db_log_client, db_media_client, db_log, db_media_catalog
    db_log_client = pymongo.MongoClient(db_conn_log)
    db_media_client = pymongo.MongoClient(db_conn_media_catalog)
    db_log = db_log_client.get_database()['logs']
    db_media_catalog = db_media_client.get_database()['media_catalog']


def finalize():
    global db_log_client, db_media_client
    db_log_client.close()
    db_media_client.close()


def persist_google_drive_item(media_item):
    print('saving the item')
    db_media_catalog.insert({
        'ts': datetime.utcnow(),
        'source': 'google-drive',
        'media_document': media_item
    })
    print('google drive item persisted successfully')


def persist_google_drive_items(media_items):
    print('saving the items')
    for media_item in media_items:
        persist_google_drive_item(media_item)
    print('items saved successfully')
