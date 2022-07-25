from flask import Response, jsonify, request
from typing import List
import requests
from bs4 import BeautifulSoup
import json
from app import app
from app.dtos import SearchMatch
import re


BASE_URL = 'https://tabs.ultimate-guitar.com'


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


    path_search = f'https://www.ultimate-guitar.com/search.php?title={SEARCH_PHRASE}&type={TYPE}&page={PAGE}'
    page = requests.get(path_search)

    # print(page.content)
    soup = BeautifulSoup(page.text, 'html.parser')
    div = soup.find("div", {'class': 'js-store'})
    s_content = div['data-content']
    results = json.loads(s_content)['store']['page']['data']['results']
    results_sorted = sorted(results, key = sort_fun, reverse=True)
    search_matches: List[SearchMatch] = []
    for result in results_sorted:
        result_type = result.get('type', None)
        if not result_type: 
            continue
        
        artist_name = result.get('artist_name', 'N/A')
        song_name = result.get('song_name', 'N/A')
        artist_url = result.get('artist_url', 'N/A')
        song_url = result.get('tab_url', None)
        if song_url:
            song_url = song_url.split('.com')[1][1:]
        else: song_url = 'N/A'
        
        match = SearchMatch(artist_name, song_name, song_url, result_type)
        search_matches.append(match)
        # print(match)
    
    response = jsonify({'ok': True, 'data':[match.serialize() for match in search_matches]})
    response.status_code = 200
    return response
    
    
@app.route('/chords', methods=['GET'])
def search_chords():
    SONG_URL = request.args.get('url', None)
    if not SONG_URL:
        response = jsonify({'ok': False, 'message': 'Invalid chord url'})
        response.status_code = 400
        return response
    
    # path_chords = 'https://tabs.ultimate-guitar.com/tab/coldplay/yellow-chords-16492'
    path_chords = f'{BASE_URL}/{SONG_URL}'
    # path_chords = 'https://tabs.ultimate-guitar.com/tab/3946514'
    page = requests.get(path_chords)

    soup = BeautifulSoup(page.text, 'html.parser')

    div = soup.find("div", {'class': 'js-store'})
    s_content = div['data-content']
    # print(s_content)
    # with open('file.txt', 'w') as f:
    #     f.write(s_content)
    result = json.loads(s_content)['store']['page']['data']['tab_view']['wiki_tab']['content']

    # print(repr(result.replace('[tab]', '').replace('[/tab]', '').replace('[ch]', '<b>').replace('[/ch]', '</b>')))
    # s_song = result.replace('[tab]', '').replace('[/tab]', '')#.replace('[ch]', '<b>').replace('[/ch]', '</b>')
    # print(result)
    # o = re.search('[ch](.*)[/ch]', result)
    # print(o)
    '<span class="fciXY _Oy28" data-name="A" style="color: rgb(0, 0, 0);">A</span>'
    
    response = jsonify({'ok': True, 'data': result})
    response.status_code = 200
    return response


