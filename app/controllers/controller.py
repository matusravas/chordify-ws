import itertools
import logging
from flask import jsonify, request, render_template_string
from typing import List
import requests
from bs4 import BeautifulSoup
import json
from app.utils.helpers import *
from app import BASE_URL_TABS
from app import app
# from app import router
from app.dtos import SearchMatch
from app.dtos.dtos import SongMetaData
import re

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
        path_search = f'{BASE_URL_TABS}/top/tabs?order={ORDER}&type=chords'
        path_search = f'{BASE_URL_TABS}/top/tabs?order={ORDER}&type=chords'
    else:
        path_search = f'{BASE_URL_TABS}/search.php?title={SEARCH_PHRASE}&type={TYPE}&page={PAGE}'
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
    
    search_matches: List[SearchMatch] = []
    for result, hit in itertools.zip_longest(results_sorted, hits_sorted):
        number_of_hits = hit.get('hits', None) if hit else None
        result_type = result.get('type', None)
        if not result_type: 
            continue
        
        artist_name = result.get('artist_name', 'N/A')
        artist_id = result.get('artist_id', None)
        song_name = result.get('song_name', 'N/A')
        song_id = result.get('song_name', None)
        artist_url = result.get('artist_url', 'N/A')
        chords_link = result.get('tab_url', None)
        full_url = result.get('tab_url', None)
        
        rating = result.get('rating', None)
        votes = result.get('votes', None)
        metadata = SongMetaData(votes, rating, number_of_hits)
        
        if chords_link:
            chords_link = chords_link.split('.com')[1][5:]
        else: chords_link = 'N/A'
        
        match = SearchMatch(artist_name, song_name, chords_link, full_url, result_type, metadata)
        search_matches.append(match)
    
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
    
    path_chords = f'{BASE_URL_TABS}/{TAB_URL}'
    page = requests.get(path_chords)

    soup = BeautifulSoup(page.text, 'html.parser')

    div = soup.find("div", {'class': 'js-store'})
    s_content = div['data-content']
    result = json.loads(s_content)['store']['page']['data']['tab_view']['wiki_tab']['content']
    
    body = re.sub(r'(\r\n)+', '<br><br>', result)
    # body = re.sub(r'(\[ch\])', '', body)
    # body = re.sub(r'(\[/ch\])', '', body)
    
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
    return {'ok': True, 'data': html_page} #render_template_string(html_page)
    return render_template_string(html_page)


