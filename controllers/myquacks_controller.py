from flask import render_template, request;
from datetime import datetime
from models.quackservice import QuackService;

class MyquacksController:
    def index(self):
        #TODO: dodati provjeru je li korisnik ulogiran, ako nije redirectati na /login
        quacks = QuackService.get_quacks_by_user( session['id'] );

        if( request.method == 'POST' and request.form.get( 'post_quack' ) ):
            try:
                db = get_db_connection();
                cursor = db.cursor();

                # Spremi quack u DB
                cursor.execute( 
                    'INSERT INTO quacks (id_user, quack, date) VALUES (%(id_user)s, %(quack)s, %(date)s)',
                    {'id_user': session['id'], 'quack': request.form.get( 'post_quack' ), 'date': datetime.now() } );
                db.commit();

                # Provjeri jel uspjelo spremanje u bazu.
                if( cursor.rowcount == 1 ):
                    # Uspjelo je.
                    return render_template( 'myquacks.html', quacks=quacks, msg='Objavili ste novi Quack!' )
                else:
                    # Nije uspjelo.
                    return render_template( 'myquacks.html', quacks=quacks, msg='Problem s dodavanjem quacka u bazu podataka.' );
            except MySQLError as err:
                return render_template( 'myquacks.html', quacks=quacks, msg=err );

        

        return render_template('myquacks.html', quacks=quacks msg='' );