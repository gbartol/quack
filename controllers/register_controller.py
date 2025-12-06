# Aplikacija pretpostavlja da u bazi postoji tablica imena 'users' i u njoj stupci: 
# username (VARCHAR(20)) i password_hash (VARCHAR(255)).

from flask import request, render_template, session, redirect;
from flask_mail import Mail, Message;
import pymysql;
from pymysql.err import MySQLError;
from db import get_db_connection, close_db;
from werkzeug.security import generate_password_hash, check_password_hash;
import re;
import random;
import string;

class RegisterController:
    def index(self):
        # Ako je korisnik već ulogiran, redirectaj na /myquacks.
        if( session.get('id') ):
            return redirect('/myquacks');

        if( request.method == 'POST' and request.form.get( 'register' ) ):
            # Korisnik se pokušava registrirati.
            return register_user();

        return render_template( 'register.html', msg='' )

def register_user():
    # Registracija novog korisnika u bazi podataka.
    username_form = request.form.get( 'username' );
    password_form = request.form.get( 'password' );
    email_form = request.form.get( 'email' );

    # Ovdje provjeravamo je li nekom korisniku već dan isti registration sequence
    # I ako je tada generiramo novi dok ne izgeneriramo neki koji još ne postoji
    flag = 1;
    while(flag):
        try:
            registration_sequence = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters);
            
            db = get_db_connection();
            cursor = db.cursor();

            cursor.execute(
                'SELECT * FROM dz2_users WHERE registration_sequence=%(registration_sequence)s',
                { 'registration_sequence': registration_sequence } );

            if( cursor.rowcount == 0):
                flag = 0;

        except MySQLError as err:
            cursor.close();
            return render_template( 'register.html', msg=err );

    if( not (username_form and password_form and email_form and re.match( r'^[A-Za-z]{1,20}$', username_form )) ):
        # Korisnik nije unio username ili password ili username nije niz slova.
        # Ispiši mu ponovno formu za login i poruku.
        return render_template( 'register.html', 
            msg='Molim unesite željeni username i password. Username se treba sastojati od max 20 slova.' );

    # Dakle, korisnik je unio neprazne username i password.
    # Spoji se na bazu i provjeri jel već postoji netko s istim usernameom.
    try:
        db = get_db_connection();
        cursor = db.cursor();

        # Uoči: as count -> 'count' će biti ključ unutar row kad izvršimo upit.
        cursor.execute( 
            'SELECT COUNT(*) AS count FROM dz2_users where username=%(username)s',
            {'username': username_form} );

        row = cursor.fetchone(); # Dohvati (jedini) redak kao rezultat upita.

        if( row['count'] > 0 ):
            # Već postoji korisnik s tim username-om.
            # Ispiši onda opet formu za ulogiravanje.
            cursor.close();
            return render_template( 'register.html', msg='Korisnik s tim usernameom već postoji.' );

        # Dakle, ne postoji korisnik s time username-om.
        # Spremi podatke za novog korisnika u tablicu.
        cursor.execute( 
            'INSERT INTO dz2_users (username, password_hash, email, registration_sequence, has_registered) VALUES (%(username)s, %(hash)s, %(email)s, %(registration_sequence)s, %(has_registered)s)',
            {'username': username_form, 'hash': generate_password_hash(password_form), 'email': email_form, 'registration_sequence': registration_sequence, 'has_registered': 0 } );

        # Upit je tipa INSERT -> treba i commit da bi se izvršio!
        db.commit();

        # Provjeri jel uspjelo spremanje u bazu.
        if( cursor.rowcount == 1 ):
            # Uspjelo je.
            cursor.close();
            return redirect(f'/send-mail?email={email_form}');
        else:
            # Nije uspjelo.
            cursor.close();
            return render_template( 'register.html', msg='Problem s dodavanjem novog korisnika u bazu podataka.' );
            
    except MySQLError as err:
        cursor.close();
        return render_template( 'register.html', msg=err );