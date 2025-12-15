from flask import request, redirect, render_template;
from pymysql.err import MySQLError;
from db import get_db_connection;

class ConfirmController:
    def index(self):
        try:
            regseq = request.args.get( 'regseq' );

            db = get_db_connection();
            cursor = db.cursor();

            cursor.execute (
                'SELECT id FROM dz2_users WHERE registration_sequence=%(regseq)s',
                { 'regseq': regseq }
            );


            if( cursor.rowcount == 0 ):
                cursor.close();
                return render_template( 'register.html', msg='Molimo kliknite na link za potvrdu koji smo vam poslali na mail.'  );

            else:
                row = cursor.fetchone();
                id_user = row['id'];

                cursor.execute(
                    'UPDATE dz2_users SET has_registered=1 WHERE id=%(id)s',
                    { 'id': id_user }
                )
                db.commit();

                cursor.close();

                if(cursor.rowcount == 0):
                    return render_template( 'register.html', msg='Verifikacija maila nije uspjela.' )
                else:
                    cursor.close();
                    return redirect('/login');

        except MySQLError as err:
            cursor.close();
            return render_template( 'register.html', msg=err );
