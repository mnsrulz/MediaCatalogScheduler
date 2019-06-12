import os.path
import requests
import re
import drivewrapper as dw
from bs4 import BeautifulSoup

peliculas_folder_id = os.environ['GDRIVE_PELICULAS_FOLDER']

user_agent = 'Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.3; Win64; x64)'


def execute():
    page_link = 'https://peliculasgoogledrive.com/movies/show-girl/'
    admin_ajax_url = 'https://peliculasgoogledrive.com/wp-admin/admin-ajax.php'
    print('peliculasgoogledrive scraping started')
    while True:
        try:
            page_response = requests.get(page_link, timeout=5, headers={'User-Agent': user_agent})
        except AssertionError as error:
            print(error)
            print('An exception occurred')
        page_content = BeautifulSoup(page_response.content, "html.parser")
        allContent = page_content.findAll('li', attrs={"class": "dooplay_player_option"})

        for content in allContent:
            data_post = content["data-post"]
            data_nume = content["data-nume"]
            print(f'content-data-post: {data_post} ; content-data-num: {data_nume}')
            payload = {'action': 'doo_player_ajax', 'post': data_post, 'nume': data_nume, 'type': 'movie'}
            admin_response = requests.post(admin_ajax_url, payload)
            admin_response_soup = BeautifulSoup(admin_response.content, "html.parser")
            iframe_src = admin_response_soup.findAll('iframe')[0]['src']
            print(admin_response)
            m = re.search('(?<=google.com\/file\/d\/)[^\/]*', iframe_src)
            if m:
                google_drive_id = m.group(0)
                dw.addToDrive(google_drive_id, peliculas_folder_id)
                print(google_drive_id)

        next_link = page_content.findAll('link', attrs={'rel': 'next'})
        if next_link:
            page_link = next_link[0]["href"]
        else:
            break
    print('peliculasgoogledrive scraping ended')


