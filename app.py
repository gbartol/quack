from flask import Flask, abort, redirect, session;
from flask_session import Session;
import importlib;
import db;

# --------------------------- Konfiguracija
app = Flask( __name__ );
app.config.from_pyfile( 'app.config' );
app.teardown_appcontext( db.close_db );

# --------------------------- Session
app.config['SESSION_TYPE'] = 'cachelib';
app.config['SESSION_PERMANENT'] = False;
Session(app);

# --------------------------- Rute
@app.route('/')
def index():
    # Korijensku rutu ćemo preusmjeriti na /login
    return redirect( '/login' );

# Popis dozvoljenih kontrolera i za svaki od njih dozvoljenih akcija.
ALLOWED_ROUTES = {
    'login': ['index'],
    'register': ['index'],
    'myquacks': ['index'],
    'feed': ['index'],
    'followers': ['index'],
    'mentions': ['index'],
    'hashtags': ['index'],
    # Rute za developere, maknuti u produkcijskoj verziji:
    'db': ['create_tables', 'seed_tables'],
    'test': ['get_all_users', 'view_users_index', 'users_controller_index'],
};

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
