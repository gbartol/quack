# Aplikacija pretpostavlja da u bazi postoji tablica imena 'users' i u njoj stupci: 
# username (VARCHAR(20)) i password_hash (VARCHAR(255)).

from flask import request, render_template, redirect, session;
from flask_session import Session;
import pymysql;
from pymysql.err import MySQLError;
from db import get_db_connection, close_db;
from werkzeug.security import generate_password_hash, check_password_hash;
import re;

class LoginController:
    def index(self):
        # Ako je korisnik već ulogiran, redirectaj ga na /myquacks.
        if( session.get('id') ):
            return redirect('/myquacks');

        if( request.method == 'POST' and request.form.get( 'login' ) ):
            # Korisnik se pokušava ulogirati.
            # Ulogiravanje postojećeg korisnika.
            username_form = request.form.get( 'username' );
            password_form = request.form.get( 'password' );

            if( not (username_form and password_form) ):
                # Korisnik nije unio bilo username bilo password.
                # Ispiši mu ponovno formu za login i poruku.
                return render_template( 'login.html', msg='Molim unesite username i password.' );

            # Dakle, korisnik je unio neprazne username i password.
            # Spoji se na bazu i probaj ga ulogirati.
            try:
                db = get_db_connection();
                cursor = db.cursor();

                # Dohvati iz baze podatke za korisnika s username-om iz forme.
                cursor.execute(
                    'SELECT * FROM dz2_users WHERE username=%(username)s',
                    {'username': username_form} );

                # Da li postoji takav user u bazi?
                if( cursor.rowcount != 1 ):
                    # Ne postoji taj user u bazi! 
                    # (Obično ne želimo reći da ne postoji taj korisnik nego samo "Pogrešan username ili password.")
                    cursor.close();
                    return render_template( 'login.html', msg=f'Ne postoji korisnik imena {username_form}.' );

                # Da, taj user postoji:
                               
                # Dohvati njegove podatke
                row = cursor.fetchone();
                # 1. Provjeri je li potvrdio svoj account
                if( not row['has_registered'] ):
                    cursor.close();
                    return render_template( 'login.html', msg=f'Molimo potvrdite svoj račun. Mail vam je poslan na adresu {row['email']}.' );
                # 2. Provjeri password, tj. usporedi s password hashom iz baze.
                password_hash = row['password_hash'];
                if( check_password_hash( password_hash, password_form ) ):
                    # Password je ispravan. Ulogiraj usera -> sad bismo ovdje spremili podatke u tom useru u session.
                    # Spremi usera u session:
                    session['id'] = row['id'];
                    # Redirectaj na početnu stranicu
                    cursor.close();
                    return redirect('/myquacks');
                else:
                    # Password nije ispravan. Ispiši ponovno formu za login.
                    # (Obično ne želimo reći da je password pogrešan nego samo "Pogrešan username ili password.")
                    cursor.close();
                    return render_template( 'login.html', msg=f'Password nije ispravan.' );

            except MySQLError as err:
                cursor.close();
                return render_template( 'login.html', msg=err );

        # Ispiši formu za ulogiravanje.
        return render_template( 'login.html', msg='' );

