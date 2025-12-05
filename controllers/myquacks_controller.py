from flask import render_template, request, session, redirect;
from datetime import datetime
from db import get_db_connection;
from pymysql.err import MySQLError;
from models.quackservice import QuackService;

class MyquacksController:
    def index(self):
       
        if( session.get( 'id' ) is None ):
            return redirect( '/login' );

        quacks = QuackService.get_quacks_by_user( session['id'] );

        if( request.method == 'POST' and request.form.get( 'post_quack' ) ):

            # Spremi quack
            quack = request.form.get( 'post_quack' );
            # Provjeri je li dug više od 140 znakova
            if( len(quack) > 140 ):
                return render_template( 'myquacks.html', quacks=quacks, msg='Quack je duži od 140 znakova.' )

            try:
                db = get_db_connection();
                cursor = db.cursor();

                # Spremi quack u DB
                cursor.execute( 
                    'INSERT INTO dz2_quacks (id_user, quack, date) VALUES (%(id_user)s, %(quack)s, %(date)s)',
                    {'id_user': session['id'], 'quack': quack, 'date': datetime.now() } );
                db.commit();

                # Provjeri jel uspjelo spremanje u bazu.
                if( cursor.rowcount == 1 ):
                    # Uspjelo je.
                    return redirect('/myquacks');
                else:
                    # Nije uspjelo.
                    return render_template( 'myquacks.html', quacks=quacks, msg='Problem s dodavanjem quacka u bazu podataka.' );
            except MySQLError as err:
                return render_template( 'myquacks.html', quacks=quacks, msg=err );

        

        return render_template('myquacks.html', quacks=quacks, msg='' );