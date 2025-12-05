import re;
from datetime import datetime;
from models.userservice import UserService;
from urllib.parse import quote;

class QuackUsername:
    # Sve isto kao i klasa Quack, samo što umjesto
    # id_user bilježi username
    def __init__( self, id, id_user, quack, date ):
        self.id = id;
        self.username = UserService.get_username_by_id( id_user );
        self.quack = link_hashtag( quack );
        self.date = date.strftime('%Y-%m-%d %H:%M');

    def __repr__(self):
        # Funkcija koja vraća string-reprezentaciju objekta tipa Quack.
        return f'QuackUsername(id: {self.id}, id_user: {self.username}, quack: {self.quack}, date: {self.date})';

def link_hashtag(quack_text):

    def replace_hashtag(match):
        hashtag = match.group(1);
        encoded_hashtag = quote(hashtag);
        return f'<a href="/hashtags?hashtag={encoded_hashtag}">{hashtag}</a>';

    quack_re = re.compile(r'(#[a-zA-Zа-яА-ЯÀ-ÖØ-öø-ʸ0-9(_)]+)');
    quack_text = quack_re.sub(replace_hashtag, quack_text);
    return quack_text;
