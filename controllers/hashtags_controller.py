from flask import render_template, request;
from models.quackservice import QuackService;

class HashtagsController:
    def index(self):
        quacks = [];

        if( request.method == 'GET' and request.args.get( 'hashtag' ) ):
            hashtag = request.args.get( 'hashtag' );

            quacks = QuackService.get_quacks_by_hashtag( hashtag );

            if( quacks == 'RegExpErr' ): # Ako korisnik nije unio valjani hashtag
                return render_template( 'hashtags.html', msg='Niste unjeli valjani hashtag.', quacks=quacks );

        return render_template( 'hashtags.html', msg='', quacks=quacks );