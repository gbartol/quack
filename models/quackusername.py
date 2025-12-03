from datetime import datetime;
from models.userservice import UserService;

class QuackUsername:
    # Sve isto kao i klasa Quack, samo što umjesto
    # id_user bilježi username
    def __init__( self, id, id_user, quack, date ):
        self.id = id;
        self.username = UserService.get_username_by_id( id_user );
        self.quack = quack;
        self.date = date;

    def __repr__(self):
        # Funkcija koja vraća string-reprezentaciju objekta tipa Quack.
        return f'QuackUsername(id: {self.id}, id_user: {self.username}, quack: {self.quack}, date: {self.date})';
