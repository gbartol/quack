from flask import render_template, request, session;
from datetime import datetime;
from db import get_db_connection;
from pymysql.err import MySQLError;
from models.quackservice import QuackService;

class FeedController:
    def index(self):
        #TODO: dodati provjeru je li korisnik ulogiran, ako nije redirectati na /login
        quacks = QuackService.get_quacks_by_following( session['id'] );

        if( request.method == 'POST' and request.form.get( 'username' ) ): # TODO: Dodati i za micanje korisnika
            # Dohvatimo uneseni username
            username = request.form.get( 'username' );
            try:
                db = get_db_connection();
                cursor = db.cursor();

                # Nađi id usera s imenom unesenom u formu:
                cursor.execute(
                    'SELECT id FROM users WHERE username=%(username)s',
                    { 'username': username } );
                # Da li postoji takav user u bazi?
                if( cursor.rowcount != 1 ):
                    # Ne postoji taj user u bazi! 
                    return render_template( 'feed.html', quacks=quacks, msg=f'Ne postoji korisnik imena {username}.' );

                # Taj user postoji,
                # 1. spremi njegov ID:
                row = cursor.fetchone();
                id_followed_user = row['id'];
                # 2. spremi to u DB tablicu follows(id_user, id_followed_user)
                cursor.execute( 
                    'INSERT INTO follows (id_user, id_followed_user) VALUES (%(id_user)s, %(id_followed_user)s)',
                    {'id_user': session['id'], 'id_followed_user': id_followed_user } );
                db.commit();

                # Provjeri jel uspjelo spremanje u bazu.
                if( cursor.rowcount == 1 ):
                    # Uspjelo je.
                    return render_template( 'feed.html', quacks=quacks, msg=f'Sada pratite korisnika {username}!' )
                else:
                    # Nije uspjelo.
                    return render_template( 'feed.html', quacks=quacks, msg='Problem s dodavanjem quacka u bazu podataka.' );
            except MySQLError as err:
                return render_template( 'feed.html', quacks=quacks, msg=err );

        

        return render_template('feed.html', quacks=quacks, msg='' );