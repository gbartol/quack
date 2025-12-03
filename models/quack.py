from datetime import datetime

class Quack:
    # Klasa koja opisuje jedan quack.
    # Svaki quack ima id, ime usera, sam tekst i datum objave -- točno kao u tablici u bazi podataka.
    def __init__( self, id, id_user, quack, date ):
        self.id = id;
        self.id_user = id_user;
        self.quack = quack;
        self.date = date;

    def __repr__(self):
        # Funkcija koja vraća string-reprezentaciju objekta tipa User.
        return f'Quack(id: {self.id}, id_user: {self.id_user}, quack: {self.quack}, date: {self.date})';
