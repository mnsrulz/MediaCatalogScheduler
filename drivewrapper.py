import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import persistence
import codecs

SCOPES = ['https://www.googleapis.com/auth/drive']
ignore_folder_id = os.environ['GDRIVE_IGNORE_FOLDER']
processed_folder_id = os.environ['GDRIVE_PROCESSED_FOLDER']
persistence.initialize()


def execute():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    # if not os.path.exists('token.pickle'):
    pickled = persistence.read_gdrive_auth_token()
    if pickled is not None:
        print('found a token from the persistence')
        creds = pickle.loads(codecs.decode(pickled.encode(), "base64"))

    # if os.path.exists('token.pickle'):
    #     with open('token.pickle', 'rb') as token:
    # creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        print('cred not valid or empty')
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                with open('credentials.json', 'w') as text_file:
                    gdrive_credentials = os.environ['GDRIVE_CREDENTIALS']
                    text_file.write(gdrive_credentials)
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_console()
        # Save the credentials for the next run
        pickled = codecs.encode(pickle.dumps(creds), "base64").decode()
        persistence.persist_gdrive_auth_token(pickled)

        # with open('token.pickle', 'wb') as token:
        #   print(creds)
        #   pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    next_page_token = ''
    query = f"""not '{ignore_folder_id}' in parents
              and mimeType!='audio/mp3'and mimeType!='image/jpeg'
              and mimeType!='audio/x-m4a'
              and mimeType!='image/png' and mimeType!='application/x-subrip'
              and mimeType!='text/plain' and mimeType!='application/pdf'
              and mimeType!='application/zip' and mimeType!='text/x-url'
              and mimeType!='application/x-rar' and mimeType!='application/rar'
              and not mimeType contains 'application/vnd' and mimeType!='application/json'
              and mimeType!='video/mp2p' and mimeType!='application/octet-stream' """
    if os.environ['GDRIVE_QUICK_SCAN'] == '1':
        query = f"{query} and not '{processed_folder_id}' in parents"
    while True:
        # Call the Drive v3 API
        results = service.files().list(
            pageSize=100,
            pageToken=next_page_token,
            fields='*',
            supportsAllDrives=1,
            includeItemsFromAllDrives=1,
            q=query
        ).execute()
        items = results.get('files', [])
        next_page_token = results.get('nextPageToken')
        if not items:
            print('No files found.')
        else:
            print(f'Found {len(items)} items...')
            for media_item in items:
                persistence.persist_google_drive_item(media_item)
                print('Calling add parent for google drive file: ' + media_item['id'])
                service.files().update(
                    fileId=media_item['id'],
                    addParents=processed_folder_id,
                ).execute()
            print('Finished processing the records')

        if not next_page_token:
            print('No more page to process... exiting...')
            break

