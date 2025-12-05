from flask import render_template, request, session, redirect;
from models.quackservice import QuackService;

class HashtagsController:
    def index(self):
        # Provjera je li korisnik ulogiran
        # (nije nužno za funkcionalnost)
        if( session.get( 'id' ) is None ):
            return redirect( '/login' );

        quacks = [];

        if( request.method == 'GET' and request.args.get( 'hashtag' ) ):
            hashtag = request.args.get( 'hashtag' );

            if( not hashtag.startswith('#') ):
                hashtag = '#' + hashtag; # Ako korisnik nije unio # prije taga

            quacks = QuackService.get_quacks_by_hashtag( hashtag );

            if( quacks == 'RegExpErr' ): # Ako korisnik nije unio valjani hashtag
                return render_template( 'hashtags.html', msg='Niste unjeli valjani hashtag.', quacks=[] );

        return render_template( 'hashtags.html', msg='', quacks=quacks );