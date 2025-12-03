class User:
    # Klasa koja opisuje jednog korisnika quack-a.
    # Svaki korisnik ima id, username, password (hash), email, registration_sequence, has_registered -- točno kao u tablici u bazi podataka.
    def __init__( self, id, username, password_hash, email ):
        self.id = id;
        self.username = username;
        self.password_hash = password_hash;
        self.email = email;
        #TODO: Kasnije treba dodati konstruktor za: registration_sequence, has_registered

    def __repr__(self):
        # Funkcija koja vraća string-reprezentaciju objekta tipa User.
        return f'User(id: {self.id}, username: {self.username}, password: {self.password_hash}, email: {self.email})';
    #TODO: dodati za registration_sequence, has_registered
