from flask import request, redirect;
import db;

class ConfirmController:
    def index(self):
        try:
            regseq = request.args.get( 'regseq' );

            db = get_db_connection();
            cursor = db.cursor();

            cursor.execute (
                'SELECT COUNT(*) AS count FROM dz2_users WHERE registration_sequence=%(regseq)s',
                { 'regseq': regseq }
            );

            row = cursor.fetchone();

            if( row['count'] == 0 ):
                cursor.close();
                return redirect('/register');
            else:
                cursor.close();
                return redirect('/login');

        except MySQLError as err:
            cursor.close();
            return render_template( 'register.html', msg=err );