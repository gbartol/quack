from flask import g, current_app;
import pymysql;
from pymysql.err import MySQLError;
from werkzeug.security import generate_password_hash, check_password_hash;

def get_db_connection():
    if( 'db_connection' not in g ):
        g.db_connection = pymysql.connect(
            host=current_app.config['DATABASE_HOST'],
            user=current_app.config['DATABASE_USER'],
            password=current_app.config['DATABASE_PASS'],
            database=current_app.config['DATABASE_DB'],
            cursorclass=pymysql.cursors.DictCursor
        );

    return g.db_connection;


def close_db( error ):
    db = g.pop( 'db_connection', None );
    if( db is not None ):
        db.close();


def prepare_db():
    msg = '';

    try:
        if( has_tables() ):
            return 'Tablice dz2_users/dz2_follows/dz2_quacks već postoje u bazi. Obrišite ih i probajte ponovno.'
        
        # Kreiraj tablice u bazi podataka.
        msg += create_table_users() + '<br>';
        msg += create_table_follows() + '<br>';
        msg += create_table_quacks() + '<br>';

        # Popuni tablice u bazi podataka.
        msg += seed_table_users() + '<br>';
        msg += seed_table_follows() + '<br>';
        msg += seed_table_quacks() + '<br>';

    except MySQLError as err:
        return f'{msg}\nerror: {err}';

    return msg;


def has_tables():
    db = get_db_connection();
    cursor = db.cursor();

    ret = False;
    sql = 'SHOW TABLES LIKE %(tblname)s';
    
    cursor.execute( sql, {'tblname': 'dz2_users'} );
    if( cursor.rowcount > 0 ):
        ret = True;
    
    cursor.execute( sql, {'tblname': 'dz2_follows'} );
    if( cursor.rowcount > 0 ):
        ret = True;
    
    cursor.execute( sql, {'tblname': 'dz2_quacks'} );
    if( cursor.rowcount > 0 ):
        ret = True;

    cursor.close();
    return ret;


def create_table_users():
    # Stvori tablicu users.
    # Svaki user ima svoj id (automatski će se povećati za svakog novoubačenog korisnika), korisničko ime, password hash, email, 
    # slučajan niz znakova potreban za registraciju, te oznaku je li registracija uspješno dovršena.
    db = get_db_connection();
    cursor = db.cursor();

    cursor.execute( 
        'CREATE TABLE IF NOT EXISTS dz2_users (' +
        'id int NOT NULL PRIMARY KEY AUTO_INCREMENT,' +
        'username varchar(50) NOT NULL,' +
        'password_hash varchar(255) NOT NULL,' +
        'email varchar(50) NOT NULL,' +
        'registration_sequence varchar(20) NOT NULL,' +
        'has_registered int)' );

    db.commit();
    cursor.close();

    return f'create_table_users: OK';


def create_table_follows():
    # Stvori tablicu follows.
    # Za svako "praćenje" pamtimo id korisnika, te id korisnika koji ga prati.
    db = get_db_connection();
    cursor = db.cursor();

    cursor.execute( 
        'CREATE TABLE IF NOT EXISTS dz2_follows (' +
        'id_user int NOT NULL,' +
        'id_followed_user int NOT NULL)' );

    db.commit();
    cursor.close();

    return f'create_table_follows: OK';


def create_table_quacks():
    # Stvori tablicu quacks.
    # Svaki quack ima svoj id (automatski će se povećati za svaku novoubačeni quack), id korisnika koji je objavio quack,
    # samu poruku koja čini quack, te datum i vrijeme kad je quack objavljen.
    db = get_db_connection();
    cursor = db.cursor();

    cursor.execute( 
        'CREATE TABLE IF NOT EXISTS dz2_quacks (' +
        'id int NOT NULL PRIMARY KEY AUTO_INCREMENT,' +
        'id_user INT NOT NULL,' +
        'quack varchar(140) NOT NULL,' +
        'date DATETIME NOT NULL)' );

    db.commit();
    cursor.close();

    return f'create_table_quacks: OK';


def seed_table_users():
    # Ubaci neke korisnike u tablicu users.
    # Uočimo da ne treba specificirati id koji se automatski poveća kod svakog ubacivanja.
    db = get_db_connection();
    cursor = db.cursor();

    sql = 'INSERT INTO dz2_users(username, password_hash, email, registration_sequence, has_registered) VALUES (%(username)s, %(password)s, \'a@b.com\', \'abc\', \'1\')';

    cursor.execute( sql,
        {'username': 'elon', 'password': generate_password_hash( 'tesla' ) } );

    cursor.execute( sql,
        {'username': 'KingJames', 'password': generate_password_hash( 'lebron' ) } );

    cursor.execute( sql,
        {'username': 'StephenCurry30', 'password': generate_password_hash( '402' ) } );

    cursor.execute( sql,
        {'username': 'billgates', 'password': generate_password_hash( 'mirkosoft' ) } );

    db.commit();
    cursor.close();

    return f'seed_table_users: OK';


def seed_table_follows():
    # Ubaci neke followere unutra (ovo nije baš pametno ovako raditi, preko hardcodiranih id-eva usera)
    db = get_db_connection();
    cursor = db.cursor();

    sql = 'INSERT INTO dz2_follows(id_user, id_followed_user) VALUES (%(id1)s, %(id2)s)';

    cursor.execute( sql,
        {'id1': 1, 'id2': 2} ); # elon -> KingJames

    cursor.execute( sql,
        {'id1': 2, 'id2': 1} ); # KingJames -> elon

    cursor.execute( sql,
        {'id1': 3, 'id2': 1} ); # StephenCurry30 -> elon

    cursor.execute( sql,
        {'id1': 1, 'id2': 4} ); # elon -> billgates

    cursor.execute( sql,
        {'id1': 4, 'id2': 1} ); # billgates -> elon

    db.commit();
    cursor.close();

    return f'seed_table_follows: OK';


def seed_table_quacks():
    # Ubaci neke quackove unutra (ovo nije baš pametno ovako raditi, preko hardcodiranih id-eva usera)
    db = get_db_connection();
    cursor = db.cursor();

    sql = 'INSERT INTO dz2_quacks(id_user, quack, date) VALUES (%(id_user)s, %(quack)s, %(date)s)';

    cursor.execute( sql,
        {'id_user': 1, 'quack': 'Congrats to @KingJames for his record and to @StephenCurry30 for scoring 49 points! Big fan of both #Lakers and #Warriors!', 'date': '2025-11-17 19:45:00' } );

    cursor.execute( sql,
        {'id_user': 1, 'quack': 'Thank you for the kind words, @billgates. #quack is so much better indeed...', 'date': '2025-11-18 17:45:00' } );

    cursor.execute( sql,
        {'id_user': 2, 'quack': 'I am finally back in action in the #NBA! 23rd season!', 'date': '2025-11-17 17:45:00' } );

    cursor.execute( sql,
        {'id_user': 2, 'quack': 'Big win over #UtahJazz! I wish I could have played vs @StephenCurry30 and the #Warriors...', 'date': '2025-11-18 23:23:23' } );

    cursor.execute( sql,
        {'id_user': 3, 'quack': 'Congrats to @KingJames of the #Lakers for his record 23rd season! #seeyousoon', 'date': '2025-11-19 03:30:30' } );

    cursor.execute( sql,
        {'id_user': 3, 'quack': 'Practising some 3-pointers for the upcoming game vs #UtahJazz!', 'date': '2025-11-18 12:32:45' } );

    cursor.execute( sql,
        {'id_user': 4, 'quack': 'I am a big fan of @elon! Driving my #tesla every day! But I prefer #quack :)', 'date': '2025-11-17 23:55:00' } );

    cursor.execute( sql,
        {'id_user': 4, 'quack': 'Well done @StephenCurry30! Good luck vs #UtahJazz #NBA', 'date': '2025-11-18 22:10:00' } );

    cursor.execute( sql,
        {'id_user': 3, 'quack': 'I\'m very happy to use #quack! Sorry, @elon, but #quack is perfect!', 'date': '2025-11-17 12:00:05' } );

    cursor.execute( sql,
        {'id_user': 3, 'quack': 'Best day ever vs #Spurs! Almost #50points', 'date': '2025-11-16 12:00:00' } );

    db.commit();
    cursor.close();

    return f'seed_table_quacks: OK';
