from typing import Dict, Union

class SongMetaData:
    def __init__(self, votes: int, rating: float, number_of_hits: Union[int, None]) -> None:
        self.votes = votes
        self.rating = rating
        self.number_of_hits = number_of_hits
        
    def serialize(self) -> Dict:
        obj = {'votes': self.votes, 'rating': self.rating, 'score': int(self.votes * self.rating)}
        if self.number_of_hits:
            obj['hits'] = self.number_of_hits
        return obj

class SearchMatch:
    def __init__(self, artist: str, song_name: str, 
                 chords_link: str, full_url: str, 
                 result_type: str, song_metadata: SongMetaData) -> None:
        self.artist = artist
        self.song_name = song_name
        self.chords_link = chords_link
        self.full_url = full_url
        self.result_type = result_type
        self.song_metadata = song_metadata
    

    def serialize(self) -> Dict:
        return {'artist': self.artist, 'song': self.song_name, 
                'chords_link': self.chords_link, 'full_url': self.full_url, 
                'meta': self.song_metadata.serialize()}


    def __str__(self) -> str:
        return f'{self.artist} - {self.song_name} url: {self.song_url}'