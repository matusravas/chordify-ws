from typing import Dict


class SearchMatch:
    def __init__(self, artist: str, song_name: str, song_url: str, result_type: str) -> None:
        self.artist = artist
        self.song_name = song_name
        self.song_url = song_url
        self.result_type = result_type
    

    def serialize(self) -> Dict:
        return {'artist': self.artist, 'song': self.song_name, 'song_url': self.song_url}


    def __str__(self) -> str:
        return f'{self.artist} - {self.song_name} url: {self.song_url}'