from typing import Dict, List, Union

class SongMetadata:
    # def __init__(self, votes: int, rating: float, number_of_hits: Union[int, None]) -> None:
    def __init__(self, votes: int, rating: float) -> None:
        self.votes = votes
        self.rating = rating
        # self.number_of_hits = number_of_hits
        
    def serialize(self) -> Dict:
        return {'votes': self.votes, 'rating': self.rating, 'score': int(self.votes * self.rating)}
        # obj = {'votes': self.votes, 'rating': self.rating, 'score': int(self.votes * self.rating)}
        # if self.number_of_hits:
        #     obj['hits'] = self.number_of_hits
        # return obj

class Song:
    def __init__(self, artist: str, song_name: str, 
                 chords_link: str, full_url: str, 
                 result_type: str, song_metadata: SongMetadata) -> None:
        self.artist = artist
        self.song_name = song_name
        self.chords_link = chords_link
        self.full_url = full_url
        self.result_type = result_type
        self.song_metadata = song_metadata
    

    def serialize(self) -> Dict:
        return {'id': hash(self.chords_link), 'artist': self.artist, 'song': self.song_name, 
                'chords_link': self.chords_link, 'full_url': self.full_url, 
                'meta': self.song_metadata.serialize()}


    def __str__(self) -> str:
        return f'{self.artist} - {self.song_name} url: {self.song_url}'


class SongChordsMetadata:
    def __init__(self, capo: Union[str, None], tonality: Union[str, None], tuning: Union[str, None], tuning_values: Union[List[str], None]) -> None:
        self.capo = capo
        self.tonality = tonality
        self.tuning = tuning
        self.tuning_values = tuning_values
        
        
    def serialize(self) -> Dict:
        return {'capo': self.capo, 'tonality': self.tonality, 'tuning': self.tuning, 'tuning_values': self.tuning_values}

    
class SongChords:
    def __init__(self, song: Song, chords_html_string: str, chords_metadata: SongChordsMetadata) -> None:
        self.song = song
        self.chords_html_string = chords_html_string
        self.chords_metadata = chords_metadata
        
        
    def serialize(self) -> Dict:
        return {'song': self.song.serialize(), 
                'chords': self.chords_html_string, 
                'meta': self.chords_metadata.serialize()}