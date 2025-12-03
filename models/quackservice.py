from db import get_db_connection;
from pymysql.err import MySQLError;
from models.user import User;
from models.quack import Quack;
from models.quackusername import QuackUsername;
import re;

class QuackService:

    @staticmethod
    def get_all_users():
        # Funkcija dohvaća sve korisnike iz tablice users u bazi podataka.
        # Vraća ih u obliku liste objekata tipa User.
        db = get_db_connection();
        cursor = db.cursor();

        cursor.execute( 'SELECT * FROM users' );

        users = [];
        for row in cursor:
            users.append( User( row['id'], row['username'], row['password_hash'], row['email'] ) ); #TODO: dodati registration_sequence, has_registered

        cursor.close();

        return users;


    @staticmethod
    def get_all_quacks():
        # Funkcija dohvaća sve quackove iz tablice quacks u bazi podataka.
        # Vraća ih u obliku liste objekata tipa Quack.
        db = get_db_connection();
        cursor = db.cursor();

        cursor.execute( 'SELECT * FROM quacks' );

        quacks = [];
        for row in cursor:
            quacks.append( QuackUsername( row['id'], row['id_user'], row['quack'], row['date'] ) );

        cursor.close();

        quacks.sort(key=comparator, reverse=True);
        return quacks;

    @staticmethod
    def get_quacks_by_user( id_user ):
        # Funkcija vraća sve quack-ove usera s id-em 'id_user'.
        # Vraća ih u obliku liste objekata tipa Quack.

        db = get_db_connection();
        cursor = db.cursor();

        cursor.execute( 
            'SELECT * FROM quacks WHERE id_user=%(id_user)s',
            {'id_user': id_user} );

        quacks = [];
        for row in cursor:
            quacks.append( QuackUsername( row['id'], row['id_user'], row['quack'], row['date'] ) );

        cursor.close();

        quacks.sort(key=comparator, reverse=True);
        return quacks;

    @staticmethod
    def get_followers_by_user( id_user ):
        # Funkcija prima ID nekog korisnika
        # Vraća listu korisnika koji prate korisnika s danim ID-om

        db = get_db_connection();
        cursor = db.cursor();

        # Nađi korisnike koji prate ulogiranog korisnika
        cursor.execute(
            'SELECT id_user FROM follows WHERE id_followed_user=%(id)s',
            { 'id': id_user } );

        # 1. Dohvatimo sve id-eve:
        rows = cursor.fetchall();
        # 2. Inicijaliziramo listu 'followers' u kojoj će se spremati imena user-a
        followers = [];
        # 3. Iteriramo po redovima koje smo našli u tablici follows
        for row in rows:
            # 4. Trazimo usernameove od tih usera
            cursor.execute(
                'SELECT username FROM users WHERE id=%(id)s',
                { 'id': row['id_user'] } );
            # 5. Fetchamo jedini red
            follower = cursor.fetchone();
            # 6. Stavimo username u listu followers
            followers.append( follower );

        cursor.close();

        return followers;

    @staticmethod
    def get_quacks_by_mention( username ):
        # Funkcija prima username nekog korisnika
        # Vraća listu Quackova gdje se spominje @username.

        db = get_db_connection();
        cursor = db.cursor();

        # Nađemo sve quackove gdje se spominje @username
        cursor.execute(
            'SELECT * FROM quacks WHERE quack LIKE CONCAT("%%@", %(username)s, "%%")',
            { 'username': username } );

        rows = cursor.fetchall();
        quacks = [];
        for row in rows:
            quacks.append( QuackUsername(row['id'], row['id_user'], row['quack'], row['date']) );
        
        cursor.close();
        #TODO: Napraviti SORT kod svih funkcija koje vraćaju Quack-ove
        quacks.sort(key=comparator, reverse=True);
        return quacks;

    @staticmethod
    def get_quacks_by_following( id_user ):
        # Funkcija prima ID nekog korisnika
        # i vraća listu Quack-ova svih korisnika koje on prati

        db = get_db_connection();
        cursor = db.cursor();

        cursor.execute( 
            'SELECT id_followed_user FROM follows WHERE id_user=%(id_user)s',
            { 'id_user': id_user } );

        quacks = [];

        rows = cursor.fetchall();
        for row in rows:
            # Dohvatimo sve quackove korisnika kojeg prati
            quacks_followed_user = QuackService.get_quacks_by_user( row['id_followed_user'] );
            # Stavimo u listu
            quacks.extend( quacks_followed_user );

        cursor.close();

        quacks.sort(key=comparator, reverse=True);
        return quacks;

    @staticmethod
    def get_quacks_by_hashtag( hashtag ):
        # Funkcija prima neki tag, npr #gospić
        # i vraća sve Quack-ove gdje se taj tag pojavljuje

        # Je li zadovoljava regexp za hashtag?
        if not( re.match( r'^#[a-zA-Z-а-яА-ЯÀ-ÖØ-öø-ʸ0-9(_)]{1,}$', hashtag ) ):
            return 'RegExpErr'; # Ne zadovoljava

        # Inače, zadovoljava:
        db = get_db_connection();
        cursor = db.cursor();

        cursor.execute(
            'SELECT * FROM quacks WHERE quack LIKE CONCAT("%", %(hashtag)s, "%")', #TODO: provjeriti je li ovo radi
            { 'hashtag': hashtag } );

        quacks = [];

        rows = cursor.fetchall();
        for row in rows:
            quacks.append( QuackUsername(row['id'], row['id_user'], row['quack'], row['date']) );

        cursor.close();

        quacks.sort(key=comparator, reverse=True);
        return quacks;



def comparator(Q):
    return Q.date;