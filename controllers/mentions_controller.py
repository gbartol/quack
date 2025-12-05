from flask import render_template, session, redirect;
from models.userservice import UserService;
from models.quackservice import QuackService;

class MentionsController:
    def index(self):
        # Provjera je li korisnik ulogiran
        if( session.get( 'id' ) is None ):
            return redirect( '/login' );

        quacks = QuackService.get_quacks_by_mention( UserService.get_username_by_id( session['id'] ) );

        return render_template( 'mentions.html', quacks=quacks, msg='' );