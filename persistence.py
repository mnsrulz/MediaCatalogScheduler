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
db_gdrive_auth_token = None


def initialize():
    global db_log_client, db_media_client, db_log, db_media_catalog, db_gdrive_auth_token
    db_log_client = pymongo.MongoClient(db_conn_log)
    db_media_client = pymongo.MongoClient(db_conn_media_catalog)
    db_log = db_log_client.get_database()['logs']
    db_media_catalog = db_media_client.get_database()['media_catalog']
    db_gdrive_auth_token = db_media_client.get_database()['gdrive_auth_token']


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


def persist_gdrive_auth_token(auth_token):
    # idea is to keep only one latest token whichever is being saved here
    print('saving the gdrive auth token')
    db_gdrive_auth_token.delete_many({})
    db_gdrive_auth_token.insert({
        'ts': datetime.utcnow(),
        'auth_token': auth_token
    })
    print('google drive auth token persisted successfully')


def read_gdrive_auth_token():
    print('reading the gdrive auth token')
    query_result = db_gdrive_auth_token.find_one()
    return None if query_result is None else query_result['auth_token']




