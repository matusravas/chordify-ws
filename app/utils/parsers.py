from typing import Dict

from app.dtos.dtos import Song, SongChordsMetadata, SongMetadata


def parse_chords_metadata_from_dict_data(data: Dict) -> SongChordsMetadata:
    capo = data.get('capo', None)
    tonality = data.get('tonality', None)
    tuning_obj = data.get('tuning', {})
    tuning_name = tuning_obj.get('name', None)
    tuning_values = tuning_obj.get('value', None)
    song_chords_metadata = SongChordsMetadata(capo, tonality, tuning_name, tuning_values)
    return song_chords_metadata
    
    
def parse_song_data_from_dict_data(data: Dict, result_type: str) -> Song:
    artist_name = data.get('artist_name', 'N/A')
    artist_id = data.get('artist_id', None)
    song_name = data.get('song_name', 'N/A')
    song_id = data.get('song_name', None)
    artist_url = data.get('artist_url', 'N/A')
    chords_link = data.get('tab_url', None)
    full_url = data.get('tab_url', None)
    
    rating = data.get('rating', None)
    votes = data.get('votes', None)
    
    if chords_link:
        chords_link = chords_link.split('.com')[1][5:]
    else: chords_link = 'N/A'
    
    metadata = SongMetadata(votes, rating)
    song = Song(artist_name, song_name, chords_link, full_url, result_type, metadata)
    return song 