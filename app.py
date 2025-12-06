from flask import Flask, abort, redirect, session, request;
from flask_session import Session;
from flask_mail import Mail, Message;
from pymysql.err import MySQLError;
import importlib;
from db import get_db_connection;
import db;

# --------------------------- Konfiguracija
app = Flask( __name__ );
app.config.from_pyfile( 'app.config' );
app.teardown_appcontext( db.close_db );

# --------------------------- Session
app.config['SESSION_TYPE'] = 'cachelib';
app.config['SESSION_PERMANENT'] = False;
Session(app);

# --------------------------- Mail
mail = Mail( app );  

# --------------------------- Rute
@app.route('/')
def index():
    # Korijensku rutu ćemo preusmjeriti na /login
    return redirect( '/login' );

# Popis dozvoljenih kontrolera i za svaki od njih dozvoljenih akcija.
ALLOWED_ROUTES = {
    'login': ['index'],
    'register': ['index'],
    'logout': ['index'],
    'confirm': ['index'],
    'myquacks': ['index'],
    'feed': ['index'],
    'followers': ['index'],
    'mentions': ['index'],
    'hashtags': ['index'],
    # Rute za developere, maknuti u produkcijskoj verziji:
    'db': ['create_tables', 'seed_tables'],
    'test': ['get_all_users', 'view_users_index', 'users_controller_index'],
};

@app.route( '/<controller>', defaults={'action': 'index'}, methods=['GET', 'POST'] )
@app.route( '/<controller>/', defaults={'action': 'index'} )
@app.route( '/<controller>/<action>', methods=['GET', 'POST'] )
def dispatch( controller, action ):
    if( controller not in ALLOWED_ROUTES
            or action not in ALLOWED_ROUTES[controller] ):
        abort( 404, f'Unknown controller {controller} and/or action {action}.' );
    
    try:
        # Dinamički importamo modul u kojem će se nalaziti odgovarajući kontroler.
        module = importlib.import_module( f'controllers.{controller}_controller' );
    
        # Odredimo ime klase traženog kontrolera.
        controller_classname = f'{controller.capitalize()}Controller';
        controller_class = getattr( module, controller_classname );

        # Instanciramo objekt pomoću klase spremljene u varijablu (!).
        controller_instance = controller_class();

        # Dohvatimo metodu (akciju) traženog imena iz tog objekta.
        action_handle = getattr( controller_instance, action );

        # Napokon, pozovemo tu metodu.
        return action_handle();

    except Exception as e:
        abort( 500, str(e) );

@app.route('/send-mail')
def send_mail():
    email = request.args.get( 'email' );

    try:
        db = get_db_connection();
        cursor = db.cursor();

        cursor.execute (
            'SELECT registration_sequence FROM dz2_users WHERE email=%(email)s',
            { 'email': email }
        );

        row = cursor.fetchone();
        registration_sequence = row['registration_sequence'];

        msg = Message(
            subject = 'Registracija na Quack',
            recipients = [ email ],
            body = f'Za registraciju na Quack klinkite link: http://127.0.0.1:5000/confirm?regseq={registration_sequence}'
        );
        mail.send( msg );

        cursor.close();
        return render_template( 'register.html', msg=f'Potvrdite svoj račun klikom na link koji je poslan na vaš mail.' )

    except MySQLError as err:
        cursor.close();
        return render_template( 'register.html', msg=err );