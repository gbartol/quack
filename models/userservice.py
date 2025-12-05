from db import get_db_connection;

class UserService:

    @staticmethod
    def get_username_by_id( id ):
        # Funkcija prima ID nekog korisnika
        # Vraća njegov username

        db = get_db_connection();
        cursor = db.cursor();

        cursor.execute(
            'SELECT username FROM dz2_users WHERE id=%(id)s',
            { 'id': id } );

        if( cursor.rowcount != 1 ):
            return "NonExistantUser"

        user = cursor.fetchone();
        cursor.close();

        return user['username'];