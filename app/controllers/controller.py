import itertools
import json
import logging
import re
from typing import List

import requests
from app import BASE_URL_CHORDS, BASE_URL_SONGS, app
from app.dtos import Song
from app.dtos.dtos import SongChords
from app.utils.auth import authorize
from app.utils.helpers import sort_fun_tabs, sort_fun_hits
from app.utils.parsers import parse_chords_metadata_from_dict_data, parse_song_data_from_dict_data
from bs4 import BeautifulSoup
from flask import jsonify, render_template_string, request

logger = logging.getLogger(__name__)

# Todo setup logger
    

@app.route('/songs')
@authorize
def search():
    SEARCH_PHRASE = request.args.get('query', '')
    TYPES = {'chords': 300, 'tabs': 200}
    TYPE = request.args.get('type', 300)
    PAGE = request.args.get('page', 1)
    SORT = request.args.get('sortOrder', 'desc')
    ORDER = request.args.get('order', 'rating_desc') # hitstotal_desc rating_desc
    
    if SEARCH_PHRASE == '':
        path_search = f'{BASE_URL_SONGS}/top/tabs?order={ORDER}&type=chords'
        path_search = f'{BASE_URL_SONGS}/top/tabs?order={ORDER}&type=chords'
    else:
        path_search = f'{BASE_URL_SONGS}/search.php?title={SEARCH_PHRASE}&type={TYPE}&page={PAGE}'
    page = requests.get(path_search)

    soup = BeautifulSoup(page.text, 'html.parser')
    div = soup.find("div", {'class': 'js-store'})
    s_content = div['data-content']
    if SEARCH_PHRASE == '':
        results = json.loads(s_content)['store']['page']['data']['tabs']
        hits = json.loads(s_content)['store']['page']['data']['hits']
        results_sorted = results
        hits_sorted = sorted(hits, key = sort_fun_hits, reverse=True if SORT == 'desc' else False)
    else:
        results = json.loads(s_content)['store']['page']['data']['results']
        results_sorted = sorted(results, key = sort_fun_tabs, reverse=True if SORT == 'desc' else False)
        hits_sorted = []
    
    search_matches: List[Song] = []
    for result, hit in itertools.zip_longest(results_sorted, hits_sorted):
        # number_of_hits = hit.get('hits', None) if hit else None
        result_type = result.get('type', None)
        if not result_type: 
            continue
        
        song = parse_song_data_from_dict_data(result, result_type)
        search_matches.append(song)
    
    response = jsonify({'ok': True, 'data':[match.serialize() for match in search_matches]})
    response.status_code = 200
    return response
    
    
@app.route('/chords', methods=['GET'])
@authorize
def search_chords():
    TAB_URL = request.args.get('tab', None)
    if not TAB_URL:
        response = jsonify({'ok': False, 'message': 'Invalid tab url'})
        response.status_code = 400
        return response
    
    path_chords = f'{BASE_URL_CHORDS}/tab/{TAB_URL}'
    page = requests.get(path_chords)

    soup = BeautifulSoup(page.text, 'html.parser')

    div = soup.find("div", {'class': 'js-store'})
    s_content = div['data-content']
    song_result = json.loads(s_content)['store']['page']['data']['tab']   
    metadata_result = json.loads(s_content)['store']['page']['data']['tab_view']['meta'] 
    
    song: Song = parse_song_data_from_dict_data(song_result, result_type='chords')
    chords_metadata: SongChordsMetadata = parse_chords_metadata_from_dict_data(metadata_result)
     
    chords = json.loads(s_content)['store']['page']['data']['tab_view']['wiki_tab']['content']
    
    body = re.sub(r'(\r\n)+', '<br><br>', chords)
    # body = re.sub(r'(\s)+', '&nbsp;', result)
    body = re.sub(r'(\[ch\])', '<b>', body)
    body = re.sub(r'(\[/ch\])', '</b> ', body)
    
    regex = re.compile(r'(\[tab\])|(\[/tab\])', re.I)
    body = regex.sub(r'', body)
    html_page = f'<!DOCTYPE html><html><body><pre>{body}</pre></body></html>'
    html_string = render_template_string(html_page)
    song_chords = SongChords(song, html_string, chords_metadata)
    return {'ok': True, 'data': song_chords.serialize()} #render_template_string(html_page)
    return render_template_string(html_page)


