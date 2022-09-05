from typing import Dict

class SongMetaData:
    def __init__(self, votes: int, rating: float) -> None:
        self.votes = votes
        self.rating = rating
        
    def serialize(self) -> Dict:
        return {'votes': self.votes, 'rating': self.rating, 'score': int(self.votes * self.rating)}

class SearchMatch:
    def __init__(self, artist: str, song_name: str, 
                 tab_link: str, full_url: str, 
                 result_type: str, song_metadata: SongMetaData) -> None:
        self.artist = artist
        self.song_name = song_name
        self.tab_link = tab_link
        self.full_url = full_url
        self.result_type = result_type
        self.song_metadata = song_metadata
    

    def serialize(self) -> Dict:
        return {'artist': self.artist, 'song': self.song_name, 
                'tab_link': self.tab_link, 'full_url': self.full_url, 
                'meta': self.song_metadata.serialize()}


    def __str__(self) -> str:
        return f'{self.artist} - {self.song_name} url: {self.song_url}'