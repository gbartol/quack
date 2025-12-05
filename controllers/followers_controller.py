from flask import render_template, session, redirect;
from models.quackservice import QuackService;

class FollowersController:
    def index(self):
        # Provjera je li korisnik ulogiran
        if( session.get( 'id' ) is None ):
            return redirect( '/login' );

        followers = QuackService.get_followers_by_user( session['id'] );

        return render_template( 'followers.html', followers=followers );