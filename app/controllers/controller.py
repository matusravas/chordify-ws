from flask import Response, jsonify, request, render_template_string
from typing import List
import requests
from bs4 import BeautifulSoup
import json
from app import app
from app.dtos import SearchMatch
from app.dtos.dtos import SongMetaData
import re


BASE_URL = 'https://tabs.ultimate-guitar.com'
BASE_URL_TAB = 'https://tabs.ultimate-guitar.com/tab/'


@app.route("/api", methods=['GET'])
def hello_world():
    return "<p>Hello, World!</p>"


def sort_fun(e):
    if 'votes' in e and 'rating' in e:
        return e['votes'] * e['rating']
    else:  
        return -1
    

@app.route('/songs')
def search():
    # SEARCH_PHRASE = 'viva la vida'
    # TYPES = {'chords': 300, 'tabs': 200}
    # TYPE = 300
    # PAGE = 1
    
    SEARCH_PHRASE = request.args.get('query', '')
    TYPES = {'chords': 300, 'tabs': 200}
    TYPE = request.args.get('type', 300)
    PAGE = request.args.get('page', 1)
    SORT = request.args.get('sort', 'desc')


    path_search = f'https://www.ultimate-guitar.com/search.php?title={SEARCH_PHRASE}&type={TYPE}&page={PAGE}'
    page = requests.get(path_search)

    # print(page.content)
    soup = BeautifulSoup(page.text, 'html.parser')
    div = soup.find("div", {'class': 'js-store'})
    s_content = div['data-content']
    results = json.loads(s_content)['store']['page']['data']['results']
    results_sorted = sorted(results, key = sort_fun, reverse=True if SORT == 'desc' else False)
    search_matches: List[SearchMatch] = []
    for result in results_sorted:
        result_type = result.get('type', None)
        if not result_type: 
            continue
        
        artist_name = result.get('artist_name', 'N/A')
        song_name = result.get('song_name', 'N/A')
        artist_url = result.get('artist_url', 'N/A')
        tab_url = result.get('tab_url', None)
        full_link = result.get('tab_url', None)
        
        rating = result.get('rating', None)
        votes = result.get('votes', None)
        metadata = SongMetaData(votes, rating)
        
        if tab_url:
            tab_url = tab_url.split('.com')[1][5:]
        else: tab_url = 'N/A'
        
        match = SearchMatch(artist_name, song_name, tab_url, full_link, result_type, metadata)
        search_matches.append(match)
        # print(match)
    
    response = jsonify({'ok': True, 'data':[match.serialize() for match in search_matches]})
    response.status_code = 200
    return response
    
    
@app.route('/chords', methods=['GET'])
def search_chords():
    TAB_URL = request.args.get('tab', None)
    if not TAB_URL:
        response = jsonify({'ok': False, 'message': 'Invalid tab url'})
        response.status_code = 400
        return response
    
    path_chords = f'{BASE_URL_TAB}/{TAB_URL}'
    page = requests.get(path_chords)

    soup = BeautifulSoup(page.text, 'html.parser')

    div = soup.find("div", {'class': 'js-store'})
    s_content = div['data-content']
    result = json.loads(s_content)['store']['page']['data']['tab_view']['wiki_tab']['content']
    
    body = re.sub(r'(\r\n)+', '<br>', result)
    regex = re.compile(r'(\[tab\])|(\[/tab\])', re.I)
    body = regex.sub(r'', body)
    html_page = f'''
                <!DOCTYPE html>
                <html>
                <body>
                {body}
                </body>
                </html>
                '''
    return render_template_string(html_page)


